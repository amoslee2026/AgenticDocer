"""SSHSIG 验签器（§3 M10 / ADR-007 §2；S11「签名格式统一」）。

本模块**自行解析 SSHSIG 帧**（OpenSSH ``PROTOCOL.sshsig``，不引入新依赖），密码学
运算交给 ``cryptography``。

**帧格式**

.. code-block:: text

    armor:  -----BEGIN SSH SIGNATURE-----
            base64(blob)（70 列折行）
            -----END SSH SIGNATURE-----
    blob:   "SSHSIG" || uint32(version=1)
            || string(publickey)       # 完整 ssh 公钥 wire 格式（首字段为 keytype）
            || string(namespace)
            || string(reserved)        # 空串
            || string(hash_algorithm)  # "sha256" | "sha512"
            || string(signature)       # string(sig_alg) || string(sig_blob)

**被签名数据**（``MAGIC_PREAUTH`` 即 ``SSHSIG``）——签名对该字节串直接计算
（Ed25519 不再二次哈希；RSA 的哈希由 ``sig_alg`` 决定）：

.. code-block:: text

    signed = "SSHSIG" || string(namespace) || string(reserved)
             || string(hash_algorithm) || string(H(message))

**算法策略**（ADR-007 §1 / S11）

* ``ssh-ed25519``：首选；签名数据直接验签，帧内哈希算法默认 ``sha512``（同 ``ssh-keygen``）；
* ``ssh-rsa`` + ``rsa-sha2-512`` / ``rsa-sha2-256``：优先 **PSS**（S11 明文要求），
  失败后回落 **PKCS#1 v1.5**——本机 OpenSSH 8.0p1 实测对 ``rsa-sha2-512`` 输出 v1.5
  （其 ``-Y sign`` 产物用 PSS 验签失败、用 v1.5 通过），要满足「与真实 ``ssh-keygen``
  互操作」就必须接受两者；``AUTH_RSA_REQUIRE_PSS=1`` 可关闭回落（严格 PSS 部署）；
* DSA / ECDSA / ``ssh-rsa``(SHA-1) 与 SHA-1 摘要一律拒绝（ADR-007 §1 拒绝弱曲线；
  RSA 模数 < 2048 位拒绝）。
"""

from __future__ import annotations

import base64
import binascii
import hashlib
import hmac
import os
import struct
from dataclasses import dataclass
from typing import Any, Final

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ed25519, padding, rsa

from .errors import SignatureFormatError, SignatureVerificationError

__all__ = [
    "ARMOR_BEGIN",
    "ARMOR_END",
    "MAGIC",
    "MIN_RSA_BITS",
    "NAMESPACE",
    "RECOMMENDED_RSA_BITS",
    "SUPPORTED_KEY_TYPES",
    "VERSION",
    "PublicKeyInfo",
    "SshSig",
    "armor",
    "dearmor",
    "fingerprint_of_blob",
    "key_blob_from_line",
    "key_type_for",
    "parse_sshsig",
    "public_key_line_from_blob",
    "signed_data",
    "validate_public_key",
    "verify_sshsig",
]

MAGIC: Final = b"SSHSIG"
VERSION: Final = 1
ARMOR_BEGIN: Final = "-----BEGIN SSH SIGNATURE-----"
ARMOR_END: Final = "-----END SSH SIGNATURE-----"

NAMESPACE: Final = "agenticdocer@auth"
"""固定 namespace（S11：CLI 与登录页共用同一验签器，namespace 不可协商）。"""

MIN_RSA_BITS: Final = 2048
"""RSA 模数下界（低于此拒绝；ADR-007 §1「拒绝 DSA/ECDSA-P256 以下强度」的同精神下限）。"""

RECOMMENDED_RSA_BITS: Final = 3072
"""ADR-007 §1 推荐强度；低于此**接受但告警**（见 `verify_sshsig`）。"""

SUPPORTED_KEY_TYPES: Final = ("ssh-ed25519", "ssh-rsa")
"""支持的密钥族；DB 侧 ``ssh_keys.key_type`` 取值域见 M01 ``SshKeyType``。"""

_HASHES: Final[dict[str, Any]] = {"sha256": hashlib.sha256, "sha512": hashlib.sha512}

_RSA_SIG_ALGS: Final[dict[str, Any]] = {
    "rsa-sha2-512": hashes.SHA512,
    "rsa-sha2-256": hashes.SHA256,
}
"""RSA 签名算法 → 摘要；不接受 ``ssh-rsa``（SHA-1，已破）。"""


# --------------------------------------------------------------------- 帧读写


def _u32(value: int) -> bytes:
    return struct.pack(">I", value)


def _string(value: bytes) -> bytes:
    return _u32(len(value)) + value


class _Reader:
    """SSH wire 格式读取器（``uint32`` 长度前缀的 ``string``）。"""

    __slots__ = ("_buf", "pos")

    def __init__(self, buf: bytes) -> None:
        self._buf = buf
        self.pos = 0

    @property
    def rest(self) -> bytes:
        return self._buf[self.pos:]

    def u32(self) -> int:
        if len(self._buf) - self.pos < 4:
            raise SignatureFormatError("SSHSIG 帧被截断：缺少 uint32", reason="truncated")
        (value,) = struct.unpack_from(">I", self._buf, self.pos)
        self.pos += 4
        return value

    def string(self) -> bytes:
        size = self.u32()
        if len(self._buf) - self.pos < size:
            raise SignatureFormatError("SSHSIG 帧被截断：字符串长度越界", reason="truncated")
        value = self._buf[self.pos:self.pos + size]
        self.pos += size
        return value


@dataclass(frozen=True, slots=True)
class SshSig:
    """解析后的 SSHSIG 帧（不可变）。"""

    version: int
    public_key_blob: bytes
    """内嵌公钥的 wire 字节（含 keytype），用于与登记公钥逐字节比对。"""

    key_type: str
    namespace: str
    reserved: bytes
    hash_algorithm: str
    signature_algorithm: str
    """内层签名算法名（``ssh-ed25519`` / ``rsa-sha2-512`` / ``rsa-sha2-256``）。"""

    signature: bytes


def armor(blob: bytes) -> str:
    """raw SSHSIG → PEM 风格 armor（与 ``ssh-keygen -Y sign`` 产物同形，70 列折行）。"""
    encoded = base64.b64encode(blob).decode("ascii")
    body = "\n".join(encoded[i:i + 70] for i in range(0, len(encoded), 70))
    return f"{ARMOR_BEGIN}\n{body}\n{ARMOR_END}\n"


def dearmor(data: str | bytes) -> bytes:
    """armor / 裸 base64 / 二进制 blob → raw SSHSIG 字节。

    容忍 HTTP 头场景（换行被折叠）与文件场景（多行 armor）；不改变任何字节语义。
    """
    text = data.encode("ascii", "ignore") if isinstance(data, str) else bytes(data)
    text = text.strip()
    if text.startswith(MAGIC):
        return text
    cleaned = text.replace(ARMOR_BEGIN.encode(), b"").replace(ARMOR_END.encode(), b"")
    cleaned = b"".join(cleaned.split())
    if not cleaned:
        raise SignatureFormatError("空的 SSHSIG 签名", reason="empty_signature")
    padded = cleaned + b"=" * (-len(cleaned) % 4)
    try:
        blob = base64.b64decode(padded, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise SignatureFormatError(
            f"SSHSIG base64 解码失败：{exc}", reason="bad_base64"
        ) from exc
    if not blob.startswith(MAGIC):
        raise SignatureFormatError("SSHSIG 帧缺少 magic", reason="bad_magic")
    return blob


def parse_sshsig(data: str | bytes) -> SshSig:
    """严格解析 SSHSIG（自研帧解析；任何结构异常 → :class:`SignatureFormatError`）。"""
    blob = dearmor(data)
    reader = _Reader(blob)
    reader.pos = len(MAGIC)
    version = reader.u32()
    if version != VERSION:
        raise SignatureFormatError(
            f"不支持的 SSHSIG 版本 {version}（期望 {VERSION}）", reason="unsupported_version"
        )
    public_key_blob = reader.string()
    namespace = reader.string()
    reserved = reader.string()
    hash_algorithm = reader.string()
    signature_field = reader.string()
    if reader.rest:
        raise SignatureFormatError("SSHSIG 帧尾部有多余字节", reason="trailing_bytes")
    if not public_key_blob or not signature_field:
        raise SignatureFormatError("SSHSIG 帧缺少公钥或签名", reason="truncated")

    key_type = _Reader(public_key_blob).string().decode("ascii", "replace")
    inner = _Reader(signature_field)
    signature_algorithm = inner.string().decode("ascii", "replace")
    signature = inner.string()
    if inner.rest:
        raise SignatureFormatError("SSHSIG 签名域尾部有多余字节", reason="trailing_bytes")
    try:
        namespace_str = namespace.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SignatureFormatError("SSHSIG namespace 非 UTF-8", reason="bad_namespace") from exc
    hash_name = hash_algorithm.decode("ascii", "replace")
    if hash_name not in _HASHES:
        raise SignatureFormatError(
            f"不支持的哈希算法 {hash_name!r}（支持 {sorted(_HASHES)}）",
            reason="unsupported_hash_algorithm",
        )
    return SshSig(
        version=version,
        public_key_blob=public_key_blob,
        key_type=key_type,
        namespace=namespace_str,
        reserved=reserved,
        hash_algorithm=hash_name,
        signature_algorithm=signature_algorithm,
        signature=signature,
    )


def signed_data(sig: SshSig, message: bytes) -> bytes:
    """被签名数据：``SSHSIG`` || namespace || reserved || hash_algorithm || H(message)。"""
    digest = _HASHES[sig.hash_algorithm](message).digest()
    return (
        MAGIC
        + _string(sig.namespace.encode("utf-8"))
        + _string(sig.reserved)
        + _string(sig.hash_algorithm.encode("ascii"))
        + _string(digest)
    )


# ------------------------------------------------------------------ 公钥操作


def key_blob_from_line(public_key_line: str) -> tuple[str, bytes]:
    """``authorized_keys`` 行 → ``(key_type, wire blob)``；非法行 → 格式错误。"""
    parts = public_key_line.strip().split()
    if len(parts) < 2:
        raise SignatureFormatError(
            "公钥行格式非法（期望 `key_type base64 [comment]`）", reason="bad_public_key"
        )
    key_type, encoded = parts[0], parts[1]
    try:
        blob = base64.b64decode(encoded + "=" * (-len(encoded) % 4), validate=True)
    except (binascii.Error, ValueError) as exc:
        raise SignatureFormatError(
            f"公钥 base64 解码失败：{exc}", reason="bad_public_key"
        ) from exc
    declared = _Reader(blob).string().decode("ascii", "replace") if blob else ""
    if declared != key_type:
        raise SignatureFormatError("公钥声明类型与 wire 内容不一致", reason="bad_public_key")
    return key_type, blob


@dataclass(frozen=True, slots=True)
class PublicKeyInfo:
    """登记前的公钥体检结果（类型 / 强度 / 指纹）。"""

    key_type: str
    """wire 类型（``ssh-ed25519`` / ``ssh-rsa``）。"""

    ssh_key_type: str
    """``ssh_keys.key_type`` 列取值（DDL 取值域：``ssh-ed25519`` / ``rsa-sha2-512`` / ``rsa-sha2-256``）。"""

    blob: bytes
    bits: int | None
    """RSA 模数位长；Ed25519 为 ``None``。"""

    @property
    def fingerprint(self) -> str:
        return fingerprint_of_blob(self.blob)


def validate_public_key(public_key_line: str) -> PublicKeyInfo:
    """登记时体检：类型/表单/强度不合规 → :class:`SignatureFormatError`。

    策略（ADR-007 §1）：仅接受 Ed25519 与 RSA（``ssh-rsa`` 行按 ``rsa-sha2-512`` 登记，
    签名算法由 SSHSIG 帧内的 ``sig_alg`` 决定）；RSA 模数 < :data:`MIN_RSA_BITS` 拒绝，
    低于 :data:`RECOMMENDED_RSA_BITS` 记录告警（沿用调用方日志）。
    """
    key_type, blob = key_blob_from_line(public_key_line)
    if key_type not in SUPPORTED_KEY_TYPES:
        raise SignatureFormatError(
            f"不支持的公钥类型 {key_type!r}（仅 {list(SUPPORTED_KEY_TYPES)}；"
            "DSA/ECDSA 与 SHA-1 一律拒绝，见 ADR-007 §1）",
            reason="unsupported_key_type",
        )
    key = _load_public_key(key_type, blob)
    bits: int | None = None
    if isinstance(key, rsa.RSAPublicKey):
        bits = _rmp_bits(key)
        if bits < MIN_RSA_BITS:
            raise SignatureFormatError(
                f"RSA 强度不足：{bits} 位 < {MIN_RSA_BITS} 位", reason="weak_key"
            )
        return PublicKeyInfo(key_type, "rsa-sha2-512", blob, bits)
    if not isinstance(key, ed25519.Ed25519PublicKey) or len(key.public_bytes_raw()) != 32:
        raise SignatureFormatError("Ed25519 公钥长度非法", reason="bad_public_key")
    return PublicKeyInfo(key_type, "ssh-ed25519", blob, bits)


def key_type_for(public_key_line: str) -> str:
    """公钥行 → ``ssh_keys.key_type`` 取值（登记与读取共用的唯一映射）。"""
    return validate_public_key(public_key_line).ssh_key_type


def public_key_line_from_blob(key_type: str, blob: bytes) -> str:
    """``(key_type, wire blob)`` → ``authorized_keys`` 行（不含注释）。"""
    return f"{key_type} {base64.b64encode(blob).decode('ascii')}"


def fingerprint_of_blob(blob: bytes) -> str:
    """``SHA256:<base64 无填充>``（与 ``ssh-keygen -lf`` 输出一致）。"""
    digest = hashlib.sha256(blob).digest()
    return "SHA256:" + base64.b64encode(digest).decode("ascii").rstrip("=")


def _load_public_key(key_type: str, blob: bytes) -> Any:
    """wire blob → ``cryptography`` 公钥对象（经文本行加载，避免二进制解析差异）。"""
    line = public_key_line_from_blob(key_type, blob).encode("ascii")
    try:
        return serialization.load_ssh_public_key(line)
    except (ValueError, TypeError) as exc:
        raise SignatureFormatError(
            f"公钥无法解析（{key_type}）：{exc}", reason="bad_public_key"
        ) from exc


def _rmp_bits(key: Any) -> int:
    return key.public_numbers().n.bit_length()


def _normalize_rsa_signature(signature: bytes, size_bytes: int) -> bytes:
    """RSA 签名值归一到模长：剥离前导 0 或左侧补 0（不同实现在 mpint/string 上不一致）。"""
    trimmed = signature.lstrip(b"\x00") or b"\x00"
    if len(trimmed) > size_bytes:
        return trimmed[-size_bytes:]
    return trimmed.rjust(size_bytes, b"\x00")


def _require_pss() -> bool:
    """``AUTH_RSA_REQUIRE_PSS=1`` 时禁用 PKCS#1 v1.5 回落（严格 PSS 部署）。"""
    return os.environ.get("AUTH_RSA_REQUIRE_PSS", "0") not in ("0", "", "false", "False")


# --------------------------------------------------------------------- 验签


def verify_sshsig(
    public_key_line: str,
    signature: str | bytes,
    message: bytes,
    *,
    namespace: str = NAMESPACE,
    require_pss: bool | None = None,
) -> SshSig:
    """用**已登记公钥**校验 SSHSIG，返回解析出的帧（失败抛 401 族异常）。

    ``public_key_line`` 必须来自库内 ``ssh_keys`` 行（``active``）；帧内嵌公钥需与之
    **逐字节一致**（防「用 B 的签名冒充 A 的 key_id」这类混淆）。
    """
    sig = parse_sshsig(signature)
    if not hmac.compare_digest(sig.namespace.encode("utf-8"), namespace.encode("utf-8")):
        raise SignatureFormatError(
            f"namespace 不匹配（期望 {namespace!r}）", reason="namespace_mismatch"
        )
    key_type, blob = key_blob_from_line(public_key_line)
    if key_type != sig.key_type or blob != sig.public_key_blob:
        raise SignatureVerificationError(
            "签名所用公钥与登记的 key_id 不一致", reason="public_key_mismatch"
        )
    public_key = _load_public_key(key_type, blob)
    data = signed_data(sig, message)

    if key_type == "ssh-ed25519":
        if not isinstance(public_key, ed25519.Ed25519PublicKey) or len(sig.signature) != 64:
            raise SignatureFormatError("Ed25519 签名长度非法", reason="bad_signature_length")
        try:
            public_key.verify(sig.signature, data)
        except Exception as exc:  # noqa: BLE001 - InvalidSignature 归一到 401
            raise SignatureVerificationError("Ed25519 验签失败", reason="bad_signature") from exc
        return sig

    if key_type == "ssh-rsa":
        return _verify_rsa(public_key, sig, data, require_pss=require_pss)

    raise SignatureFormatError(
        f"不支持的密钥类型 {key_type!r}（支持 {list(SUPPORTED_KEY_TYPES)}）",
        reason="unsupported_key_type",
    )


def _verify_rsa(key: Any, sig: SshSig, data: bytes, *, require_pss: bool | None) -> SshSig:
    """RSA：PSS 优先（S11），按需回落 PKCS#1 v1.5（本机 OpenSSH 8.0p1 互操作）。"""
    if not isinstance(key, rsa.RSAPublicKey):
        raise SignatureFormatError("RSA 公钥无法加载", reason="bad_public_key")
    bits = _rmp_bits(key)
    if bits < MIN_RSA_BITS:
        raise SignatureFormatError(
            f"RSA 强度不足：{bits} 位 < {MIN_RSA_BITS} 位", reason="weak_key"
        )
    alg = sig.signature_algorithm
    if alg not in _RSA_SIG_ALGS:
        raise SignatureFormatError(
            f"不支持的 RSA 签名算法 {alg!r}（支持 {sorted(_RSA_SIG_ALGS)}；`ssh-rsa`=SHA-1 已禁用）",
            reason="unsupported_signature_algorithm",
        )
    hash_cls = _RSA_SIG_ALGS[alg]
    if sig.hash_algorithm != hash_cls.name:
        raise SignatureFormatError(
            f"签名算法 {alg} 与帧内哈希算法 {sig.hash_algorithm} 不一致",
            reason="hash_algorithm_mismatch",
        )
    signature = _normalize_rsa_signature(sig.signature, (bits + 7) // 8)
    strict = _require_pss() if require_pss is None else require_pss
    attempts: list[tuple[str, Any]] = [
        ("pss-digest", padding.PSS(mgf=padding.MGF1(hash_cls()), salt_length=hash_cls.digest_size)),
        ("pss-auto", padding.PSS(mgf=padding.MGF1(hash_cls()), salt_length=padding.PSS.AUTO)),
    ]
    if not strict:
        attempts.append(("pkcs1v15", padding.PKCS1v15()))
    for label, scheme in attempts:
        try:
            key.verify(signature, data, scheme, hash_cls())
        except Exception:  # noqa: BLE001 - 逐个候选方案试错，全失败才对调用方 401
            continue
        if label == "pkcs1v15":
            _log_legacy_padding(alg, bits)
        return sig
    raise SignatureVerificationError(
        f"RSA({alg}) 验签失败（PSS 与 PKCS#1 v1.5 均未通过）", reason="bad_signature"
    )


def _log_legacy_padding(alg: str, bits: int) -> None:
    """PKCS#1 v1.5 回落是互操作妥协，需留痕（否则「静默降级」不可审计）。"""
    from agenticdocer.observability import get_logger  # 局部导入：保持本模块纯密码学

    get_logger("m10.sshsig").warn(
        "RSA 签名使用 PKCS#1 v1.5（本机 OpenSSH 对 rsa-sha2-* 的实际填充）",
        op="verify_signature",
        sig_alg=alg,
        rsa_bits=bits,
        padding="pkcs1v15",
    )
