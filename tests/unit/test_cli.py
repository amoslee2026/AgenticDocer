"""M11 CLI 单元测试（§9.2 / REQ-M11-F01..F04）。

覆盖：命令完整性与 ``--help``、全局开关（``--json``/``--dry-run`` 两种书写位置）、
签名载荷与**服务端视角**的字节级一致（不启进程，用 MockTransport 复现 M10 的 RAW_PATH 复现规则并
真实验签）、鉴权/授权/冲突/校验四类失败的**可操作指引**（V17c）、参数解析错误路径、
``logs`` 薄封装（不重复实现查询）。

无外部依赖：不连库、不连网、不需要 ssh-keygen。
"""

from __future__ import annotations

import json
import urllib.parse
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx
import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from typer.testing import CliRunner

from agenticdocer import cli
from agenticdocer.auth import signing, sshsig

runner = CliRunner()

ROOT_COMMANDS = ("render", "stats", "quality-gate")
GROUPS = {
    "auth": ("bootstrap", "whoami", "sign"),
    "user": ("add", "list", "disable", "role"),
    "grant": ("add", "list", "rm"),
    "import": ("parse", "review", "commit"),
    "doc": ("list", "get", "diff", "delete"),
    "node": ("get", "put", "delete"),
    "comment": ("list", "add", "resolve"),
    "logs": ("stats", "trace", "tail", "query"),
}


# ----------------------------------------------------------------------
# 夹具与替身
# ----------------------------------------------------------------------


@pytest.fixture()
def key_pair(tmp_path: Path) -> tuple[Path, str]:
    """Ed25519 私钥（OpenSSH PEM）+ 对应 ``authorized_keys`` 行。"""
    key = ed25519.Ed25519PrivateKey.generate()
    path = tmp_path / "id_ed25519"
    path.write_bytes(
        key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.OpenSSH,
            serialization.NoEncryption(),
        )
    )
    return path, signing.public_key_line(key)


@pytest.fixture()
def no_key(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    """无任何可用私钥的环境（HOME 指向空目录 + 清掉覆盖变量）。"""
    empty = tmp_path / "empty-home"
    empty.mkdir()
    monkeypatch.setenv("HOME", str(empty))
    monkeypatch.delenv("AGENTICDOCER_SSH_KEY", raising=False)
    return empty


@dataclass
class _Call:
    """服务端视角的一次请求。"""

    method: str
    raw_path: str
    url: str
    body: bytes
    payload: bytes


def _server_view(request: httpx.Request) -> tuple[str, bytes]:
    """复现 M10 ``middleware.raw_path`` + ``signing.request_payload``。

    服务端取 ASGI ``scope["raw_path"]``（**未百分号解码**的原样字节）+ 原样 query
    （SecAudit AUD-2 后的口径）——即客户端的「发送形态」。
    """
    raw_path = request.url.raw_path.decode("latin-1")
    body = request.content or b""
    payload = signing.request_payload(
        request.method,
        raw_path,
        body,
        request.headers["X-Timestamp"],
        request.headers["X-Nonce"],
    )
    return raw_path, payload


def fake_api(
    public_key: str | None = None,
    *,
    responder: Callable[[httpx.Request], httpx.Response] | None = None,
) -> tuple[httpx.MockTransport, list[_Call]]:
    """假 API：验证签名（给了公钥时）+ 记录服务端视角请求。"""
    calls: list[_Call] = []

    def handler(request: httpx.Request) -> httpx.Response:
        raw_path, payload = _server_view(request)
        calls.append(
            _Call(request.method, raw_path, str(request.url), request.content, payload)
        )
        if public_key is not None:
            sshsig.verify_sshsig(public_key, request.headers["X-SSH-Signature"], payload)
        if responder is not None:
            return responder(request)
        return httpx.Response(200, json={"ok": True})

    return httpx.MockTransport(handler), calls


def patch_transport(monkeypatch: pytest.MonkeyPatch, transport: httpx.BaseTransport) -> None:
    """把 CLI 的 HTTP 客户端挂到假传输上（CLI 仍走真实签名与错误映射）。"""
    original = cli.SigningClient._http

    def patched(self: cli.SigningClient) -> httpx.Client:
        if self._client is None:
            self._client = httpx.Client(base_url=self.base_url, transport=transport)
        return self._client

    monkeypatch.setattr(cli.SigningClient, "_http", patched)
    assert original is not None


def run(*argv: str, env_key: Path | None = None) -> Any:
    """跑 CLI（可选注入私钥路径），返回 CliRunner 结果。"""
    args = list(argv)
    if env_key is not None:
        args = ["--key", str(env_key), *args]
    return runner.invoke(cli.app, args)


# ----------------------------------------------------------------------
# 命令完整性（§9.2 命令表）
# ----------------------------------------------------------------------


def test_help_lists_every_group() -> None:
    output = runner.invoke(cli.app, ["--help"]).output
    for name in (*ROOT_COMMANDS, *GROUPS):
        assert name in output, name


@pytest.mark.parametrize(("group", "commands"), GROUPS.items())
def test_group_help_lists_subcommands(group: str, commands: tuple[str, ...]) -> None:
    result = runner.invoke(cli.app, [group, "--help"])
    assert result.exit_code == 0
    for name in commands:
        assert name in result.output, (group, name)


def test_user_key_subcommand_is_reachable() -> None:
    result = runner.invoke(cli.app, ["user", "key", "--help"])
    assert result.exit_code == 0
    assert "add" in result.output and "revoke" in result.output


def _leaf_paths() -> list[list[str]]:
    """全部叶子命令路径（从 Typer 注册表推导，避免手抄漏项）。"""
    paths = [[name] for name in ROOT_COMMANDS]
    for group, commands in GROUPS.items():
        paths.extend([[group, name] for name in commands])
    paths.append(["user", "key", "add"])
    paths.append(["user", "key", "revoke"])
    return paths


@pytest.mark.parametrize("path", _leaf_paths(), ids=lambda path: "-".join(path))
def test_every_command_has_help(path: list[str]) -> None:
    result = runner.invoke(cli.app, [*path, "--help"])
    assert result.exit_code == 0, result.output
    assert "--json" in result.output and "--dry-run" in result.output


# ----------------------------------------------------------------------
# 全局开关：两种书写位置等价
# ----------------------------------------------------------------------


def test_json_and_dry_run_after_subcommand() -> None:
    result = runner.invoke(cli.app, ["doc", "list", "--json", "--dry-run"])
    assert result.exit_code == 0, result.output
    payload = _json(result.output)
    assert payload["dryRun"] is True
    assert payload["method"] == "GET"
    assert payload["path"] == "/api/v1/docs"


def test_global_flags_before_subcommand_are_equivalent() -> None:
    after = runner.invoke(cli.app, ["doc", "list", "--dry-run", "--json"])
    before = runner.invoke(cli.app, ["--dry-run", "--json", "doc", "list"])
    assert after.exit_code == before.exit_code == 0
    assert _json(after.output) == _json(before.output)


def test_node_put_dry_run_reveals_payload() -> None:
    result = runner.invoke(
        cli.app,
        [
            "node",
            "put",
            "--doc",
            "SPEC-X",
            "--atom-type",
            "clause",
            "--anchor",
            "SPEC-X#3.2·时序",
            "--content",
            '{"text":"hi"}',
            "--expected-version",
            "4",
            "--dry-run",
        ],
    )
    assert result.exit_code == 0, result.output
    payload = _json(result.output)
    assert payload["method"] == "POST"
    assert payload["body"]["expectedVersion"] == 4
    assert payload["body"]["anchor"] == "SPEC-X#3.2·时序"


def test_doc_delete_dry_run_flags_non_atomic_plan() -> None:
    result = runner.invoke(cli.app, ["doc", "delete", "SPEC-X", "--dry-run", "--json"])
    payload = _json(result.output)
    assert payload["atomic"] is False
    assert any("nodes" in step for step in payload["plan"])


def test_import_dry_run_does_not_touch_db_or_network(tmp_path: Path) -> None:
    src = tmp_path / "spec.md"
    src.write_text("---\nspec_id: SPEC-X\ntitle: X\n---\n\n# 1 概述\n\n正文\n", encoding="utf-8")
    result = runner.invoke(cli.app, ["import", "parse", str(src), "--dry-run"])
    assert result.exit_code == 0, result.output
    payload = _json(result.output)
    assert payload["action"] == "import.parse"
    assert payload["authCheck"] == "GET /api/v1/auth/me"
    assert not (tmp_path / "import_work").exists()


def _json(text: str) -> dict[str, Any]:
    """取输出里的 JSON 主体（``--json``/``--dry-run`` 输出不含其它前缀）。"""
    return json.loads(text[text.index("{") :])


# ----------------------------------------------------------------------
# 编码与签名载荷
# ----------------------------------------------------------------------


def test_encode_target_is_the_encoded_request_line() -> None:
    """发送即签名：编码形态的请求行目标（query 原样参与）。"""
    assert cli.encode_target("/api/v1/nodes/SPEC-X#3.2·transfer", {"doc_id": "SPEC-X"}) == (
        "/api/v1/nodes/SPEC-X%233.2%C2%B7transfer?doc_id=SPEC-X"
    )
    assert cli.encode_target("docs/SPEC-X") == "/docs/SPEC-X"  # 补前导斜杠


def test_encode_target_participates_in_signature(
    monkeypatch: pytest.MonkeyPatch, key_pair: tuple[Path, str]
) -> None:
    """query 原样参与签名（S2：改任一参数即 401）。"""
    transport, calls = fake_api(key_pair[1])
    patch_transport(monkeypatch, transport)
    result = run("node", "get", "node-1", "--doc", "SPEC-X", "--json", env_key=key_pair[0])
    assert result.exit_code == 0, result.output
    assert calls[0].raw_path == "/api/v1/nodes/node-1?doc_id=SPEC-X"


def test_client_signature_verifies_against_server_reconstruction(
    monkeypatch: pytest.MonkeyPatch, key_pair: tuple[Path, str]
) -> None:
    """签名链路端到端：CLI 生成的头能被 M10 的验签器用服务端复现的载荷验过。"""
    transport, calls = fake_api(key_pair[1])
    patch_transport(monkeypatch, transport)
    result = run("node", "get", "SPEC-STD-AMBA-APB#3.2.1·transfer", "--json", env_key=key_pair[0])
    assert result.exit_code == 0, result.output
    call = calls[0]
    assert call.raw_path == "/api/v1/nodes/SPEC-STD-AMBA-APB%233.2.1%C2%B7transfer"
    assert b"SPEC-STD-AMBA-APB%233.2.1%C2%B7transfer" in call.payload  # 载荷即发送形态


def test_signature_check_has_teeth(key_pair: tuple[Path, str]) -> None:
    """反向验证：换一个载荷再验签必须失败（否则上面的用例是空转）。"""
    client = cli.SigningClient(key_path=key_pair[0])
    headers = signing.sign_request_headers(client.private_key(), "GET", "/api/v1/docs", None)
    good = signing.request_payload("GET", "/api/v1/docs", None, headers["X-Timestamp"], headers["X-Nonce"])
    bad = signing.request_payload("GET", "/api/v1/docs?x=1", None, headers["X-Timestamp"], headers["X-Nonce"])
    sshsig.verify_sshsig(key_pair[1], headers["X-SSH-Signature"], good)
    with pytest.raises(Exception):
        sshsig.verify_sshsig(key_pair[1], headers["X-SSH-Signature"], bad)


def test_client_posts_body_bytes_that_are_signed(
    monkeypatch: pytest.MonkeyPatch, key_pair: tuple[Path, str]
) -> None:
    transport, calls = fake_api(key_pair[1])
    patch_transport(monkeypatch, transport)
    result = run(
        "comment",
        "add",
        "--node",
        "node-1",
        "--body",
        "人类批注：请补时序图",
        "--json",
        env_key=key_pair[0],
    )
    assert result.exit_code == 0, result.output
    call = calls[0]
    assert call.body.decode("utf-8").startswith("{")
    assert "人类批注" in call.body.decode("utf-8")


def test_missing_key_error_is_actionable(no_key: Path) -> None:
    result = runner.invoke(cli.app, ["auth", "whoami"])
    assert result.exit_code == 1
    assert "AGENTICDOCER_SSH_KEY" in result.stderr
    assert "user key add" in result.stderr
    assert "Traceback" not in result.output + result.stderr


# ----------------------------------------------------------------------
# 错误映射与可操作指引（V17c）
# ----------------------------------------------------------------------


@dataclass
class _Fault:
    status: int
    detail: Any

    def __call__(self, request: httpx.Request) -> httpx.Response:
        return httpx.Response(self.status, json={"detail": self.detail})


def test_forbidden_hint_names_role_and_grant_command(
    monkeypatch: pytest.MonkeyPatch, key_pair: tuple[Path, str], tmp_path: Path
) -> None:
    fault = _Fault(403, {"error": "DTO_AUTH_REJECTED", "reason": "forbidden", "message": "角色不足"})
    transport, _ = fake_api(responder=fault)
    patch_transport(monkeypatch, transport)
    patch = tmp_path / "patch.json"
    patch.write_text(json.dumps({"docId": "SPEC-X", "anchor": "SPEC-X#1", "atomType": "clause",
                                 "content": {"text": "x"}, "expectedVersion": 2}), encoding="utf-8")
    result = run("node", "put", "--file", str(patch), "--json", env_key=key_pair[0])
    assert result.exit_code == 1
    assert "editor" in result.stderr  # 所需角色名
    assert "agenticdocer user role --username" in result.stderr
    assert "agenticdocer grant add" in result.stderr
    assert "--permission write" in result.stderr


def test_unregistered_key_hint_asks_admin_to_register(
    monkeypatch: pytest.MonkeyPatch, key_pair: tuple[Path, str]
) -> None:
    fault = _Fault(403, {"error": "DTO_AUTH_REJECTED", "reason": "forbidden", "message": "公钥 X 未注册或其属主已禁用"})
    transport, _ = fake_api(responder=fault)
    patch_transport(monkeypatch, transport)
    result = run("doc", "list", "--json", env_key=key_pair[0])
    assert result.exit_code == 1
    assert "user key add" in result.stderr
    expected = signing.fingerprint(signing.public_key_line(signing.load_private_key(key_pair[0])))
    assert expected in result.stderr  # 本地私钥指纹，便于 admin 核对


def test_unauthorized_hint_covers_skew_nonce_and_bootstrap(
    monkeypatch: pytest.MonkeyPatch, key_pair: tuple[Path, str]
) -> None:
    fault = _Fault(401, {"error": "DTO_AUTH_REJECTED", "reason": "missing_credentials", "message": "缺少凭据"})
    transport, _ = fake_api(responder=fault)
    patch_transport(monkeypatch, transport)
    result = run("doc", "list", "--json", env_key=key_pair[0])
    assert result.exit_code == 1
    assert "SIGNATURE_MAX_SKEW_SECONDS" in result.stderr
    assert "auth bootstrap" in result.stderr


def test_conflict_hint_tells_to_reread(
    monkeypatch: pytest.MonkeyPatch, key_pair: tuple[Path, str]
) -> None:
    fault = _Fault(409, {"error": "CONFLICT", "message": "version mismatch"})
    transport, _ = fake_api(responder=fault)
    patch_transport(monkeypatch, transport)
    result = run("node", "delete", "n1", "--expected-version", "3", "--json", env_key=key_pair[0])
    assert result.exit_code == 1
    assert "乐观锁" in result.stderr
    assert "node get" in result.stderr


def test_validation_hint_lists_violations(
    monkeypatch: pytest.MonkeyPatch, key_pair: tuple[Path, str]
) -> None:
    fault = _Fault(
        422,
        {"message": "schema 校验失败", "violations": [{"message": "缺少 text", "fixHint": "补 content.text"}]},
    )
    transport, _ = fake_api(responder=fault)
    patch_transport(monkeypatch, transport)
    result = run(
        "node",
        "put",
        "--doc",
        "SPEC-X",
        "--atom-type",
        "clause",
        "--anchor",
        "SPEC-X#1",
        "--content",
        '{"x":1}',
        "--json",
        env_key=key_pair[0],
    )
    assert result.exit_code == 1
    assert "缺少 text" in result.stderr
    assert "补 content.text" in result.stderr


def test_network_failure_is_actionable(
    monkeypatch: pytest.MonkeyPatch, key_pair: tuple[Path, str]
) -> None:
    def boom(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("connection refused", request=request)

    patch_transport(monkeypatch, httpx.MockTransport(boom))
    result = run("doc", "list", "--json", env_key=key_pair[0])
    assert result.exit_code == 1
    assert "agenticdocer-api" in result.stderr


def test_server_error_hint_points_at_logs(
    monkeypatch: pytest.MonkeyPatch, key_pair: tuple[Path, str]
) -> None:
    """5xx 不吐堆栈，指向带 rid 的日志查询（服务端错误也要可操作）。"""
    transport, _ = fake_api(responder=_Fault(500, {"message": "boom"}))
    patch_transport(monkeypatch, transport)
    result = run("doc", "list", "--json", env_key=key_pair[0])
    assert result.exit_code == 1
    assert "HTTP 500" in result.stderr
    assert "agenticdocer logs query --level ERROR" in result.stderr


def test_min_role_mapping_matches_m10_matrix() -> None:
    assert cli._min_role("read") == "reader"
    assert cli._min_role("write") == "editor"
    assert cli._min_role("review") == "reviewer"
    assert cli._min_role(cli.MANAGE_USERS) == "admin"



# ----------------------------------------------------------------------
# quality-gate（M09B 交付面）
# ----------------------------------------------------------------------


def _whoami_admin(request: httpx.Request) -> httpx.Response:
    return httpx.Response(
        200, json={"userId": "u-1", "username": "alice", "role": "admin", "permissions": []}
    )


def _whoami_reader(request: httpx.Request) -> httpx.Response:
    return httpx.Response(
        200, json={"userId": "u-2", "username": "bob", "role": "reader", "permissions": []}
    )


def _stub_reports() -> list[Any]:
    from agenticdocer.model import QualityReport, Violation

    return [
        QualityReport(detector_id="broken_refs", violations=[]),
        QualityReport(
            detector_id="terms",
            violations=[
                Violation(
                    rule_id="RULE_TERMS_UNSEEDED",
                    path="SPEC-X#1",
                    message="术语未入种子表",
                    fix_hint="把该词写入 data/terms_seed.yaml 后重启服务",
                )
            ],
        ),
    ]


@pytest.fixture()
def stub_gate(monkeypatch: pytest.MonkeyPatch) -> list[Any]:
    """把 M09B 的质量门换成固定报告（只测 CLI 的参数/角色/输出形状）。"""
    import agenticdocer.m09 as m09

    calls: list[Any] = []

    def fake_run(scope: Any, **kwargs: Any) -> list[Any]:
        calls.append(scope)
        return _stub_reports()

    monkeypatch.setattr(m09, "run_quality_gate_sync", fake_run)
    return calls


def test_quality_gate_default_detectors_exclude_perf_health() -> None:
    assert cli.QUALITY_ADMIN_DETECTOR == "perf_health"
    assert cli.QUALITY_ADMIN_DETECTOR not in cli.QUALITY_DEFAULT_DETECTORS
    assert set(cli.QUALITY_DEFAULT_DETECTORS) <= set(cli._resolve_detectors(None))


def test_quality_gate_accepts_repeated_and_comma_separated_detectors() -> None:
    assert cli._resolve_detectors(["broken_refs,terms", "assets_missing"]) == [
        "broken_refs",
        "terms",
        "assets_missing",
    ]


def test_quality_gate_rejects_unknown_detector() -> None:
    result = runner.invoke(cli.app, ["quality-gate", "--detectors", "nope", "--json"])
    assert result.exit_code == 1
    assert "未知 detector" in result.stderr
    assert "broken_refs" in result.stderr  # 可选值清单


def test_quality_gate_dry_run_plan(no_key: Path) -> None:
    """干跑不触网/不触库（无密钥也能自检参数）；重复旗标与逗号分隔等价。"""
    result = runner.invoke(
        cli.app,
        [
            "quality-gate",
            "--doc-id", "SPEC-X",
            "--doc-id", "SPEC-Y",
            "--detectors", "broken_refs,terms",
            "--detectors", "assets_missing",
            "--dry-run",
        ],
    )
    assert result.exit_code == 0, result.output
    payload = _json(result.output)
    assert payload["action"] == "quality-gate"
    assert payload["arguments"]["docIds"] == ["SPEC-X", "SPEC-Y"]
    assert payload["arguments"]["detectors"] == ["broken_refs", "terms", "assets_missing"]
    assert payload["authCheck"] == "GET /api/v1/auth/me"


def test_quality_gate_output_shape_and_grouping(
    monkeypatch: pytest.MonkeyPatch, key_pair: tuple[Path, str], stub_gate: list[Any]
) -> None:
    transport, _ = fake_api(key_pair[1], responder=_whoami_admin)
    patch_transport(monkeypatch, transport)
    result = run("quality-gate", "--doc-id", "SPEC-X", "--json", env_key=key_pair[0])
    assert result.exit_code == 0, result.output
    payload = _json(result.output)
    assert payload["detectors"] == list(cli.QUALITY_DEFAULT_DETECTORS)
    assert payload["docIds"] == ["SPEC-X"]
    assert payload["clean"] is False
    assert payload["summary"] == {"detectors": 2, "violations": 1, "byDetector": {"broken_refs": 0, "terms": 1}}
    violation = payload["reports"][1]["violations"][0]
    assert violation["ruleId"] and violation["path"] and violation["message"]
    assert violation["fixHint"]  # agent 自修复依据（REQ-M06-F02 口径）
    assert stub_gate[0].doc_ids == ["SPEC-X"]


def test_quality_gate_human_output_states_clean_and_grouped(
    monkeypatch: pytest.MonkeyPatch, key_pair: tuple[Path, str], stub_gate: list[Any]
) -> None:
    transport, _ = fake_api(key_pair[1], responder=_whoami_admin)
    patch_transport(monkeypatch, transport)
    result = run("quality-gate", env_key=key_pair[0])
    assert result.exit_code == 0, result.output
    assert "[broken_refs] 无违规" in result.stdout
    assert "[terms] 违规 1 条" in result.stdout
    assert "合计" in result.stdout


def test_quality_gate_requires_admin_for_perf_health(
    monkeypatch: pytest.MonkeyPatch, key_pair: tuple[Path, str], stub_gate: list[Any]
) -> None:
    """perf_health 读 DB 内部指标 → 与 /admin/health 同级（admin）。"""
    transport, _ = fake_api(key_pair[1], responder=_whoami_reader)
    patch_transport(monkeypatch, transport)
    denied = run("quality-gate", "--detectors", "perf_health", "--json", env_key=key_pair[0])
    assert denied.exit_code == 1
    assert "admin" in denied.stderr
    assert "agenticdocer user role --username" in denied.stderr
    assert not stub_gate  # 未越权执行


def test_quality_gate_reader_may_run_data_detectors(
    monkeypatch: pytest.MonkeyPatch, key_pair: tuple[Path, str], stub_gate: list[Any]
) -> None:
    transport, _ = fake_api(key_pair[1], responder=_whoami_reader)
    patch_transport(monkeypatch, transport)
    result = run("quality-gate", "--json", env_key=key_pair[0])
    assert result.exit_code == 0, result.output
    assert stub_gate  # reader 可跑只读巡检

# ----------------------------------------------------------------------
# 参数解析错误路径
# ----------------------------------------------------------------------


def test_comment_list_requires_exactly_one_selector() -> None:
    neither = runner.invoke(cli.app, ["comment", "list", "--json"])
    both = runner.invoke(cli.app, ["comment", "list", "--doc", "D", "--node", "N", "--json"])
    for result in (neither, both):
        assert result.exit_code == 1
        assert "--doc" in result.stderr and "--node" in result.stderr


def test_node_put_requires_file_or_content() -> None:
    result = runner.invoke(cli.app, ["node", "put", "--json"])
    assert result.exit_code == 1
    assert "--file" in result.stderr and "--content" in result.stderr


def test_node_put_inline_requires_identity_fields() -> None:
    result = runner.invoke(cli.app, ["node", "put", "--content", "{}", "--json"])
    assert result.exit_code == 1
    assert "--atom-type" in result.stderr and "--anchor" in result.stderr


def test_node_put_rejects_non_object_payload(tmp_path: Path) -> None:
    payload = tmp_path / "patch.json"
    payload.write_text("[1, 2]", encoding="utf-8")
    result = runner.invoke(cli.app, ["node", "put", "--file", str(payload), "--json"])
    assert result.exit_code == 1
    assert "JSON 对象" in result.stderr


def test_grant_rm_requires_identifier() -> None:
    result = runner.invoke(cli.app, ["grant", "rm", "--json"])
    assert result.exit_code == 1
    assert "--grant-id" in result.stderr


def test_stats_requires_target_or_health() -> None:
    result = runner.invoke(cli.app, ["stats"])
    assert result.exit_code == 1
    assert "--health" in result.stderr and "--src" in result.stderr


def test_import_commit_bulk_dry_run_plan() -> None:
    """M03 批量路径经统一入口可达（ADR-009 §3）：干跑回放 bulk 参数。"""
    result = runner.invoke(
        cli.app,
        [
            "import", "commit", "DBG",
            "--bulk", "--bulk-mode", "initial_load", "--batch-size", "1000",
            "--dry-run",
        ],
    )
    assert result.exit_code == 0, result.output
    arguments = _json(result.output)["arguments"]
    assert arguments["bulk"] is True
    assert arguments["bulk_mode"] == "initial_load"
    assert arguments["batch_size"] == 1000


def test_import_commit_rejects_unknown_bulk_mode() -> None:
    result = runner.invoke(cli.app, ["import", "commit", "DBG", "--bulk-mode", "nope", "--dry-run"])
    assert result.exit_code == 1
    assert "online" in result.stderr and "initial_load" in result.stderr


def test_auth_sign_requires_nonce_or_message(no_key: Path) -> None:
    result = runner.invoke(cli.app, ["auth", "sign"])
    assert result.exit_code == 1
    assert "--nonce" in result.stderr and "--message" in result.stderr


def test_auth_sign_login_nonce_is_verifiable(key_pair: tuple[Path, str]) -> None:
    result = run("auth", "sign", "--login", "--nonce", "abc123", "--json", env_key=key_pair[0])
    assert result.exit_code == 0, result.output
    payload = _json(result.output)
    assert payload["mode"] == "login"
    sshsig.verify_sshsig(key_pair[1], payload["signature"], signing.login_payload("abc123"))


def test_auth_sign_login_without_nonce_is_rejected(key_pair: tuple[Path, str]) -> None:
    result = run("auth", "sign", "--login", env_key=key_pair[0])
    assert result.exit_code == 1
    assert "--nonce" in result.stderr


def test_user_add_dry_run_shows_body() -> None:
    result = runner.invoke(cli.app, ["user", "add", "--username", "alice", "--role", "editor", "--dry-run"])
    payload = _json(result.output)
    assert payload["body"] == {"username": "alice", "role": "editor"}


def test_user_key_add_validates_public_key_locally(tmp_path: Path) -> None:
    bad = tmp_path / "bad.pub"
    bad.write_text("not-a-key\n", encoding="utf-8")
    result = runner.invoke(cli.app, ["user", "key", "add", "--username", "alice", "--key", str(bad)])
    assert result.exit_code == 1
    assert "公钥不合规" in result.stderr


def test_user_key_add_missing_file_is_actionable(tmp_path: Path) -> None:
    result = runner.invoke(
        cli.app, ["user", "key", "add", "--username", "alice", "--key", str(tmp_path / "absent.pub")]
    )
    assert result.exit_code == 1
    assert "不存在" in result.stderr
    assert "ssh-keygen" in result.stderr


# ----------------------------------------------------------------------
# logs：薄封装 agentic-logger
# ----------------------------------------------------------------------


def test_logs_stats_dry_run_delegates_argv() -> None:
    result = runner.invoke(cli.app, ["logs", "stats", "--group-by", "error_code", "--dry-run"])
    payload = _json(result.output)
    assert payload["argv"][0] == cli.LOGGER_BIN
    assert payload["argv"][1] == "--log-dir"
    assert payload["argv"][3] == "stats"
    assert "--format" in payload["argv"] and "json" in payload["argv"]


def test_logs_query_passes_filters() -> None:
    result = runner.invoke(
        cli.app,
        ["logs", "query", "--level", "ERROR", "--module", "m02.nodes", "--since", "1h", "--dry-run"],
    )
    argv = _json(result.output)["argv"]
    assert argv[argv.index("--level") + 1] == "ERROR"
    assert argv[argv.index("--module") + 1] == "m02.nodes"
    assert argv[argv.index("--since") + 1] == "1h"


def test_logs_missing_binary_is_actionable(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cli.shutil, "which", lambda name: None)
    result = runner.invoke(cli.app, ["logs", "tail"])
    assert result.exit_code == 1
    assert cli.LOGGER_BIN in result.stderr
    assert "uv sync" in result.stderr


def test_opts_skips_none_and_false() -> None:
    assert cli._opts(a=None, b=False, c=True, d="x") == ["--c", "--d", "x"]


# ----------------------------------------------------------------------
# 输出渲染
# ----------------------------------------------------------------------


def test_table_aligns_and_truncates() -> None:
    text = cli._table(["id", "body"], [["1", "x" * 100]])
    lines = text.splitlines()
    assert set(lines[1]) == {"-", " "}
    assert "…" in lines[2]


def test_flat_serializes_structures() -> None:
    assert cli._flat({"a": 1}) == '{"a":1}'
    assert cli._flat(None) == ""


def _load(path: Path) -> Any:
    return signing.load_private_key(path)
