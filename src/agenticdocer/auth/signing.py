"""SSHSIG 签名生成与密钥/指纹工具（S11：客户端侧，M11 CLI 与登录页共用）。

与 :mod:`agenticdocer.auth.sshsig` 构成一对：**同一帧格式、同一 namespace、同一验签器**。
签名侧固定用 PSS（S11 明文），验签侧额外接受 PKCS#1 v1.5（本机 OpenSSH 互操作，
见 ``sshsig`` 模块文档）。

**请求载荷（S2 修复，字节级精确）**——本模块是载荷公式的**唯一定义点**：

.. code-block:: text

    payload = METHOD + "\n" + RAW_PATH + "\n" + SHA256(body).hexdigest() + "\n"
              + TIMESTAMP + "\n" + NONCE

``RAW_PATH`` = 请求行中路径 + ``?`` + query 的**原样字节**（不百分号解码、不去点段、
不增删尾部斜杠）；**query 参与签名**。服务端必须用**收到的原始头文本**拼载荷
（不可把 ``X-Timestamp`` 重新格式化，否则与客户端不一致）。
"""

from __future__ import annotations

import base64
import hashlib
import os
import secrets
import struct
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Final

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ed25519, padding, rsa

from .sshsig import (
    NAMESPACE,
    armor,
    fingerprint_of_blob,
    key_blob_from_line,
    key_type_for,
    public_key_line_from_blob,
)

__all__ = [
    "KEY_ID_PREFIX",
    "RSA_PADDING",
    "SigningError",
    "build_sshsig",
    "default_key_path",
    "fingerprint",
    "key_type_for",
    "load_private_key",
    "login_payload",
    "new_nonce",
    "normalize_key_id",
    "public_key_line",
    "request_payload",
    "sign_message",
    "sign_message_armored",
    "sign_request_headers",
    "timestamp_now",
]

KEY_ID_PREFIX: Final = "SHA256:"
"""``key_id`` 前缀（与 ``ssh-keygen -lf`` 一致）。"""

RSA_PADDING: Final = "pss"
"""签名侧固定 PSS（S11 明文）；验签侧兼容 PKCS#1 v1.5，见 ``sshsig`` 模块文档。"""

_HASHES: Final[dict[str, Any]] = {"sha256": hashes.SHA256, "sha512": hashes.SHA512}


class SigningError(ValueError):
    """客户端签名失败（私钥不可读 / 类型不支持）——不跨 HTTP，故用 ``ValueError`` 语义。"""


def _frame(value: bytes) -> bytes:
    """SSH wire ``string``（uint32 长度前缀）。"""
    return struct.pack(">I", len(value)) + value


def default_key_path() -> Path:
    """私钥查找：``AGENTICDOCER_SSH_KEY`` → ``~/.ssh/id_ed25519`` → ``~/.ssh/id_rsa``。"""
    configured = os.environ.get("AGENTICDOCER_SSH_KEY")
    if configured:
        return Path(configured).expanduser()
    home = Path("~/.ssh").expanduser()
    ed25519 = home / "id_ed25519"
    return ed25519 if ed25519.exists() else home / "id_rsa"


def load_private_key(path: Path | str | None = None, password: str | None = None) -> Any:
    """读取 OpenSSH 私钥（Ed25519 / RSA）；不可读或加密未给口令 → :class:`SigningError`。"""
    target = Path(path) if path is not None else default_key_path()
    try:
        data = target.read_bytes()
    except OSError as exc:
        raise SigningError(f"私钥不可读：{target}（{exc.strerror or exc}）") from exc
    try:
        key = serialization.load_ssh_private_key(
            data, password=password.encode() if password else None
        )
    except TypeError as exc:
        raise SigningError(f"私钥已加密，需提供口令：{target}") from exc
    except ValueError as exc:
        raise SigningError(f"私钥解析失败：{target}（{exc}）") from exc
    if not isinstance(key, (ed25519.Ed25519PrivateKey, rsa.RSAPrivateKey)):
        raise SigningError(f"不支持的私钥类型：{type(key).__name__}（仅 Ed25519 / RSA）")
    return key


def public_key_line(key: Any) -> str:
    """公钥（或私钥的公开部分）→ ``authorized_keys`` 行（不含注释）。"""
    public = (
        key.public_key()
        if isinstance(key, (ed25519.Ed25519PrivateKey, rsa.RSAPrivateKey))
        else key
    )
    raw = public.public_bytes(
        serialization.Encoding.OpenSSH, serialization.PublicFormat.OpenSSH
    ).decode("ascii")
    key_type = raw.split()[0]
    _, blob = key_blob_from_line(raw)
    return public_key_line_from_blob(key_type, blob)


def fingerprint(public_key_line: str) -> str:
    """公钥行 → ``SHA256:<base64>``（与 ``ssh-keygen -lf`` 逐字一致，用作 ``key_id``）。"""
    _, blob = key_blob_from_line(public_key_line)
    return fingerprint_of_blob(blob)


def normalize_key_id(key_id: str) -> str:
    """归一 ``key_id``：容忍客户端省略 ``SHA256:`` 前缀（前缀大小写不敏感）。"""
    stripped = key_id.strip()
    if stripped.lower().startswith(KEY_ID_PREFIX.lower()):
        return KEY_ID_PREFIX + stripped[len(KEY_ID_PREFIX):]
    return KEY_ID_PREFIX + stripped



def timestamp_now(moment: datetime | None = None) -> str:
    """``X-Timestamp`` 文本（ISO 8601 UTC 秒级；服务端原样参与载荷）。"""
    return (moment or datetime.now(timezone.utc)).astimezone(timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


def new_nonce() -> str:
    """``X-Nonce``（``secrets.token_urlsafe(32)``，256 位 CSPRNG）。"""
    return secrets.token_urlsafe(32)


def _signed_data(namespace: str, hash_algorithm: str, message: bytes) -> bytes:
    """SSHSIG 被签名数据（与验签侧 :func:`sshsig.signed_data` 同构）。"""
    digest = _HASHES[hash_algorithm](message).digest()
    return (
        b"SSHSIG"
        + _frame(namespace.encode("utf-8"))
        + _frame(b"")
        + _frame(hash_algorithm.encode("ascii"))
        + _frame(digest)
    )


def build_sshsig(
    private_key: Any,
    message: bytes,
    *,
    namespace: str = NAMESPACE,
    hash_algorithm: str = "sha512",
) -> bytes:
    """生成 SSHSIG **raw blob**（Ed25519 直签；RSA 用 PSS + 同名摘要，S11）。"""
    line = public_key_line(private_key)
    key_type, blob = key_blob_from_line(line)
    data = _signed_data(namespace, hash_algorithm, message)
    if key_type == "ssh-ed25519":
        signature_algorithm = "ssh-ed25519"
        signature = private_key.sign(data)
    elif key_type == "ssh-rsa":
        hash_cls = _HASHES[hash_algorithm]
        signature_algorithm = f"rsa-sha2-{hash_cls.digest_size * 8}"
        signature = private_key.sign(
            data,
            padding.PSS(mgf=padding.MGF1(hash_cls()), salt_length=hash_cls.digest_size),
            hash_cls(),
        )
    else:
        raise SigningError(f"不支持的私钥类型：{key_type}（仅 ssh-ed25519 / ssh-rsa）")

    signature_field = _frame(signature_algorithm.encode("ascii")) + _frame(signature)
    return (
        b"SSHSIG"
        + struct.pack(">I", 1)
        + _frame(blob)
        + _frame(namespace.encode("utf-8"))
        + _frame(b"")
        + _frame(hash_algorithm.encode("ascii"))
        + _frame(signature_field)
    )


def sign_message(
    key: Any,
    message: bytes,
    *,
    namespace: str = NAMESPACE,
    hash_algorithm: str = "sha512",
) -> str:
    """签名 → **单行 base64**（可直接放进 HTTP 头 / JSON 体）。"""
    return base64.b64encode(
        build_sshsig(key, message, namespace=namespace, hash_algorithm=hash_algorithm)
    ).decode("ascii")


def sign_message_armored(key: Any, message: bytes, **kwargs: Any) -> str:
    """签名 → armor 形态（与 ``ssh-keygen -Y sign`` 产物同形，供「上传签名文件」路径）。"""
    blob = build_sshsig(key, message, **kwargs)
    return armor(blob)


def request_payload(
    method: str,
    raw_path: str,
    body: bytes | None,
    timestamp: str,
    nonce: str,
) -> bytes:
    """S2 载荷（唯一定义点）：``METHOD\\nRAW_PATH\\nSHA256(body)\\nTIMESTAMP\\nNONCE``。"""
    digest = hashlib.sha256(body or b"").hexdigest()
    return f"{method.upper()}\n{raw_path}\n{digest}\n{timestamp}\n{nonce}".encode("utf-8")


def login_payload(nonce: str) -> bytes:
    """登录签名载荷 = **nonce 的原样字节**（无换行；CLI `auth sign --login` 与登录页共用）。"""
    return nonce.encode("utf-8")


def sign_request_headers(
    key: Any,
    method: str,
    raw_path: str,
    body: bytes | None = None,
    *,
    timestamp: str | None = None,
    nonce: str | None = None,
    namespace: str = NAMESPACE,
) -> dict[str, str]:
    """按 §3 M06 生成四个签名头（M11 ``SigningClient`` 与测试共用）。"""
    stamp = timestamp or timestamp_now()
    token = nonce or new_nonce()
    payload = request_payload(method, raw_path, body, stamp, token)
    return {
        "X-SSH-Key-Id": fingerprint(public_key_line(key)),
        "X-SSH-Signature": sign_message(key, payload, namespace=namespace),
        "X-Timestamp": stamp,
        "X-Nonce": token,
    }
