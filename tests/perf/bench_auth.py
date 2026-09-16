"""`bench_auth` — 鉴权开销（ADR-010 §3.2；指标 §1.4：**验签 + 会话校验 P95 <10ms**）。

§1.4 的测量口径为「Ed25519 验签 + PG 会话查（≥1000 次）」，M10 有**两条**鉴权路径，
本基准分别测量（同为「一次鉴权」的真实成本）：

| 场景 | 路径 | 内容 |
|---|---|---|
| `auth.verify_signature` | **agent**（SSHSIG 签名） | 时间窗 → 公钥查表（`revoked_at IS NULL` + 属主 active）→ SSHSIG 验签 → nonce 入库（S7） |
| `auth.resolve_session` | **WebUI**（会话 Cookie） | `SHA256(token)` 查 `sessions JOIN users` + 滑动续期（S8/S13/S15） |
| `auth.sshsig_crypto` | 纯密码学 | 仅 `verify_sshsig`（Ed25519 验签）——归因用：证明瓶颈不在密码学 |

**客户端签名不计入服务端耗时**（签名在计时区外完成，只测服务端）。
每次迭代都用**新 nonce + 新签名**（S7 一次性 nonce，重放必须 401）。

运行：

    uv run python tests/perf/bench_auth.py --dsn <dsn> [--iterations 1000] [--compare] [--json]
"""

from __future__ import annotations

import argparse
import asyncio
import secrets
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import pytest  # noqa: E402

from _common import (  # noqa: E402
    TARGET_AUTH_P95_MS,
    Bench,
    Stopwatch,
    add_common_args,
    configure_dsn,
    default_args,
    environment,
    execute,
    metric,
    open_storage,
    reachable,
    render_table,
    save,
    timing_stats,
)

pytestmark = pytest.mark.perf

NAME = "auth"
TITLE = "鉴权开销（§1.4：验签 + 会话校验 P95 <10ms）"

USERNAME = "perf-bench-agent"
RAW_PATH = "/api/v1/nodes/00000000-0000-7000-8000-000000000000?doc_id=SPEC-PERF"
METHOD = "GET"
BODY = b""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="M10 鉴权开销基准（签名路径 + 会话路径）")
    add_common_args(parser)
    parser.add_argument("--iterations", type=int, default=1000, help="签名路径迭代数（§1.4 要求 ≥1000）")
    parser.add_argument("--session-iterations", type=int, default=1000, help="会话路径迭代数")
    parser.add_argument("--crypto-iterations", type=int, default=2000, help="纯验签迭代数（归因）")
    return parser


async def _identity(db) -> dict:
    """自建基准身份：稳定用户名 + **每次运行新生成**的 Ed25519 密钥（不复用固定密钥）。

    ADR-007 §1：同一公钥全局唯一归属，故「每运行新密钥」既避免与自举/其他测试的
    密钥冲突，也避免跨运行的状态依赖（M06/M07 在同源缺陷上踩过的坑）。
    """
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

    from agenticdocer.auth import add_ssh_key, create_user, find_user_by_username
    from agenticdocer.auth.signing import fingerprint, public_key_line

    key = Ed25519PrivateKey.generate()
    public_line = public_key_line(key)
    key_id = fingerprint(public_line)

    user = await find_user_by_username(USERNAME, db=db)
    if user is None:
        user = await create_user(USERNAME, "reader", actor="perf-bench", db=db)
    await add_ssh_key(user.user_id, public_line, actor="perf-bench", db=db)
    return {"key": key, "public_line": public_line, "key_id": key_id, "user": user}


async def run_bench(args: argparse.Namespace) -> Bench:
    from agenticdocer.auth import resolve_session, verify_signature
    from agenticdocer.auth.middleware import SshSigHeaders
    from agenticdocer.auth.sessions import create_challenge, login
    from agenticdocer.auth.signing import (
        login_payload,
        new_nonce,
        request_payload,
        sign_message,
        timestamp_now,
    )
    from agenticdocer.auth.sshsig import verify_sshsig

    storage = open_storage(args.dsn)
    db = storage.db
    bench = Bench(name=NAME, title=TITLE, environment=environment())
    try:
        identity = await _identity(db)
        key, key_id = identity["key"], identity["key_id"]

        # 前置正确性校验：一次真实调用必须成功（测不到真东西的基准毫无意义）
        probe_nonce = new_nonce()
        probe_stamp = timestamp_now()
        probe_payload = request_payload(METHOD, RAW_PATH, BODY, probe_stamp, probe_nonce)
        context = await verify_signature(
            METHOD, RAW_PATH, BODY,
            SshSigHeaders(
                signature=sign_message(key, probe_payload),
                key_id=key_id,
                timestamp=probe_stamp,
                nonce=probe_nonce,
            ),
            db=db,
        )
        assert context.key_fingerprint == key_id, "验签返回的 key_id 不符"

        # ① 签名路径（agent）：每次新 nonce + 新签名
        signature_samples: list[int] = []
        sign_us: list[int] = []
        for _ in range(args.iterations):
            nonce = new_nonce()
            stamp = timestamp_now()
            payload = request_payload(METHOD, RAW_PATH, BODY, stamp, nonce)
            sign_watch = Stopwatch()
            signature = sign_message(key, payload)
            sign_us.append(sign_watch.elapsed_us())  # 客户端成本（不计入服务端指标）
            headers = SshSigHeaders(signature=signature, key_id=key_id, timestamp=stamp, nonce=nonce)
            watch = Stopwatch()
            await verify_signature(METHOD, RAW_PATH, BODY, headers, db=db)
            signature_samples.append(watch.elapsed_us())

        # ② 会话路径（WebUI）：真实挑战-响应换 token，再重复解析会话
        # 限流桶按 IP 计：用**每次运行唯一**的桶，避免与其他运行/测试互相挤占（S7）
        rate_ip = f"perf-bench-{secrets.token_hex(4)}"
        challenge = await create_challenge(rate_ip, db=db)
        session = await login(
            key_id, challenge.nonce, sign_message(key, login_payload(challenge.nonce)),
            db=db, ip=rate_ip,
        )
        session_samples: list[int] = []
        for _ in range(args.session_iterations):
            watch = Stopwatch()
            user = await resolve_session(session.token, db=db)
            session_samples.append(watch.elapsed_us())
        assert user is not None and user.username == USERNAME, "会话解析失败"

        # ③ 纯密码学（归因）：固定消息 + 固定签名，无时间/库开销
        crypto_stamp = timestamp_now()
        crypto_nonce = new_nonce()
        crypto_payload = request_payload(METHOD, RAW_PATH, BODY, crypto_stamp, crypto_nonce)
        crypto_signature = sign_message(key, crypto_payload)
        crypto_samples: list[int] = []
        for _ in range(args.crypto_iterations):
            watch = Stopwatch()
            verify_sshsig(identity["public_line"], crypto_signature, crypto_payload)
            crypto_samples.append(watch.elapsed_us())

        signature_stats = timing_stats(signature_samples)
        session_stats = timing_stats(session_samples)
        crypto_stats = timing_stats(crypto_samples)
        client_sign_stats = timing_stats(sign_us)

        print("\n样本明细（服务端口径；客户端签名在计时区外）：")
        print(render_table(
            ["场景", "路径", "P50ms", "P95ms", "P99ms", "最大ms", "样本数"],
            [
                ["verify_signature", "agent（签名+非ce 入库）", f"{signature_stats['p50_ms']:.3f}",
                 f"{signature_stats['p95_ms']:.3f}", f"{signature_stats['p99_ms']:.3f}",
                 f"{signature_stats['max_ms']:.3f}", signature_stats["n"]],
                ["resolve_session", "webui（会话查+续期）", f"{session_stats['p50_ms']:.3f}",
                 f"{session_stats['p95_ms']:.3f}", f"{session_stats['p99_ms']:.3f}",
                 f"{session_stats['max_ms']:.3f}", session_stats["n"]],
                ["sshsig_crypto", "纯 Ed25519 验签", f"{crypto_stats['p50_ms']:.3f}",
                 f"{crypto_stats['p95_ms']:.3f}", f"{crypto_stats['p99_ms']:.3f}",
                 f"{crypto_stats['max_ms']:.3f}", crypto_stats["n"]],
                ["client_sign", "客户端签名（参考）", f"{client_sign_stats['p50_ms']:.3f}",
                 f"{client_sign_stats['p95_ms']:.3f}", f"{client_sign_stats['p99_ms']:.3f}",
                 f"{client_sign_stats['max_ms']:.3f}", client_sign_stats["n"]],
            ],
        ))

        bench.counters.update({
            "iterations": args.iterations,
            "session_iterations": args.session_iterations,
            "crypto_iterations": args.crypto_iterations,
            "user": USERNAME,
            "role": identity["user"].role,
            "key_id": key_id,
            "raw_path": RAW_PATH,
            "nonces_written": args.iterations,  # 每次验签成功写 1 行 nonce（S7）
        })

        bench.add(
            metric("auth.verify_signature.p50_ms", signature_stats["p50_ms"], unit="ms"),
            metric("auth.verify_signature.p95_ms", signature_stats["p95_ms"], unit="ms",
                   target=TARGET_AUTH_P95_MS,
                   note="§1.4 鉴权开销 P95（agent 路径：验签 + 公钥/属主查表 + nonce 入库）"),
            metric("auth.verify_signature.p99_ms", signature_stats["p99_ms"], unit="ms"),
            metric("auth.verify_signature.max_ms", signature_stats["max_ms"], unit="ms"),
            metric("auth.resolve_session.p50_ms", session_stats["p50_ms"], unit="ms"),
            metric("auth.resolve_session.p95_ms", session_stats["p95_ms"], unit="ms",
                   target=TARGET_AUTH_P95_MS,
                   note="§1.4 鉴权开销 P95（webui 路径：会话查 + users JOIN + 滑动续期）"),
            metric("auth.resolve_session.p99_ms", session_stats["p99_ms"], unit="ms"),
            metric("auth.resolve_session.max_ms", session_stats["max_ms"], unit="ms"),
            metric("auth.sshsig_crypto.p50_ms", crypto_stats["p50_ms"], unit="ms",
                   note="归因：纯 Ed25519 验签成本（应远低于 10ms）"),
            metric("auth.sshsig_crypto.p95_ms", crypto_stats["p95_ms"], unit="ms"),
            metric("auth.client_sign.p50_ms", client_sign_stats["p50_ms"], unit="ms",
                   note="参考值：客户端签名（不计入服务端指标）"),
        )

        bench.notes.append(
            f"每次迭代均为**新 nonce + 新签名**（S7 一次性 nonce；重放必须 401），"
            f"共写入 {args.iterations} 行 `nonces`（生产由 `purge_expired` 清理）"
        )
        bench.notes.append(
            "计时**含** M12 日志落盘（`verify_signature` 的 `log.timer` 在退出时写 JSONL）；"
            "ADR-010「代价」将日志写入列在 <10ms 预算之外 ⇒ 本口径偏保守"
        )
        bench.notes.append(
            "两条路径分别判定（§1.4 的口径「验签 + 会话校验」在 M10 落为两条独立路径，"
            "单个请求只会走其中一条）"
        )
        ratio = signature_stats["p50_ms"] / crypto_stats["p50_ms"] if crypto_stats["p50_ms"] else 0.0
        bench.notes.append(
            f"归因：签名路径 P50 是纯验签的 {ratio:.1f}×，其余为公钥/属主两次查表 + nonce 事务提交"
        )
    finally:
        await db.dispose()
    return bench


def test_auth_benchmark() -> None:
    """`pytest -m perf` 路径：断言 1000 次鉴权全部成功且指标齐全（判定由报告呈现）。"""
    args = default_args(build_parser())
    if not reachable(args.dsn):
        pytest.skip(f"基准库不可达：{configure_dsn(args.dsn)}")
    bench = asyncio.run(run_bench(args))
    save(bench, args.out)
    for name in ("auth.verify_signature.p95_ms", "auth.resolve_session.p95_ms"):
        item = bench.get(name)
        assert item is not None and item.value > 0, f"指标缺失或非正：{name}"
    assert bench.counters["iterations"] >= 1000, "迭代数低于 §1.4 要求的 1000 次"


if __name__ == "__main__":
    sys.exit(execute(build_parser(), run_bench))
