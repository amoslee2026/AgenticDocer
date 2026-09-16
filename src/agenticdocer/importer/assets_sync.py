"""M03 图片资产同步（A6/A7、REQ-M03-F05）：两类引用取件 → sha256 校验 → 写 `assets`。

覆盖面（§3 M03 接口 + design_doc §5.2）：

- **md 形式** `![alt](images/<sha256>.jpg)`（语料 1,019 处，全部独占一行）；
- **HTML 形式** `<img src="images/<sha256>.jpg">`（语料 80 处，全部位于 `<table>` 片段内——
  P4 零改写下随片段原样保留，仅在渲染期由 M04 重写 src）。

行为契约：

- **缺失不阻断**（design_doc §5.2）：取不到的引用进 :attr:`AssetSyncReport.missing`，
  导入继续；清单供 M09B `assets_missing` 判据与 M04 渲染期标注消费；
- **哈希校验**：引用文件名即 sha256（内容寻址），取件后重算 sha256，不一致或缺失 → 记 missing
  （不写入「名字与字节不符」的资产）；
- **幂等**：字节落 `ASSET_STORE_DIR` CAS、元数据行按 `asset_id` 去重（M02 `put_asset`）。

`source_root` 语义：**引用路径的解析根**，即「包含 `images/` 的目录」。语料实物不在本仓库
（design_doc §5.2：位于 GigaRAG `corpus/02_converted/specifications/*/auto/images/`），
故默认取源 md 所在目录，可由 `IMPORT_SOURCE_ROOT` 覆盖（§5 环境变量族）。
"""

from __future__ import annotations

import asyncio
import hashlib
import mimetypes
import os
import re
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, Literal

from agenticdocer.model import AssetSyncReport
from agenticdocer.observability import get_logger

__all__ = [
    "MD_IMAGE_RE",
    "HTML_IMAGE_RE",
    "SHA256_RE",
    "AssetRef",
    "AssetBytes",
    "source_root_for",
    "iter_refs",
    "collect_refs",
    "unique_refs",
    "ref_counts",
    "resolve_asset",
    "fetch_assets",
    "sync_assets",
    "mime_for",
]

log = get_logger("m03.assets")

MD_IMAGE_RE: Final = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<src>[^)\s]+)(?:[ \t]+\"[^\"]*\")?\)")
HTML_IMAGE_RE: Final = re.compile(
    r"<img\b[^>]*?\bsrc\s*=\s*[\"']?(?P<src>[^\"'\s>]+)[\"']?", re.IGNORECASE
)
SHA256_RE: Final = re.compile(r"(?P<sha>[0-9a-f]{64})(?:\.(?P<ext>[A-Za-z0-9]+))?$")

_EXTENSION_MIME: Final[dict[str, str]] = {
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "jpe": "image/jpeg",
    "png": "image/png",
    "gif": "image/gif",
    "svg": "image/svg+xml",
    "webp": "image/webp",
    "bmp": "image/bmp",
    "tif": "image/tiff",
    "tiff": "image/tiff",
    "emf": "image/emf",
    "wmf": "image/wmf",
    "ico": "image/x-icon",
    "pdf": "application/pdf",
}


@dataclass(frozen=True)
class AssetRef:
    """一处图片引用（出现即一条；`raw` 为源文档中的原始路径）。"""

    raw: str
    form: Literal["md", "html"]
    sha256: str | None
    """文件名里编码的 sha256（内容寻址约定）；非该形态为 ``None``。"""

    extension: str | None

    @property
    def basename(self) -> str:
        return self.raw.rsplit("/", 1)[-1]


@dataclass(frozen=True)
class AssetBytes:
    """取件结果（已校验大小写一致的 sha256）。"""

    ref: str
    sha256: str
    data: bytes
    mime: str
    origin: str


def source_root_for(source_path: Path | str | None) -> Path:
    """引用解析根：`IMPORT_SOURCE_ROOT` → 源 md 所在目录 → 当前目录。"""
    override = os.environ.get("IMPORT_SOURCE_ROOT")
    if override:
        return Path(override)
    if source_path is None:
        return Path.cwd()
    return Path(source_path).parent


def _classify(raw: str, form: Literal["md", "html"]) -> AssetRef:
    basename = raw.rsplit("/", 1)[-1].split("?")[0].split("#")[0]
    match = SHA256_RE.search(basename)
    if match is None:
        extension = basename.rsplit(".", 1)[-1].lower() if "." in basename else None
        return AssetRef(raw=raw, form=form, sha256=None, extension=extension)
    return AssetRef(
        raw=raw,
        form=form,
        sha256=match.group("sha"),
        extension=(match.group("ext") or "").lower() or None,
    )


def iter_refs(text: str, *, form: Literal["md", "html", "both"] = "both") -> Iterator[AssetRef]:
    """按文档序迭代**全部**引用出现（HTML 与 md 混排时按出现位置归并）。"""
    hits: list[tuple[int, Literal["md", "html"], str]] = []
    if form in ("md", "both"):
        hits.extend((match.start(), "md", match.group("src")) for match in MD_IMAGE_RE.finditer(text))
    if form in ("html", "both"):
        hits.extend((match.start(), "html", match.group("src")) for match in HTML_IMAGE_RE.finditer(text))
    for _, kind, src in sorted(hits, key=lambda item: item[0]):
        yield _classify(src, kind)


def collect_refs(text: str, *, form: Literal["md", "html", "both"] = "both") -> list[AssetRef]:
    """全部引用出现（含重复；REQ-M03-F05「1,099 处引用」= 本函数的长度）。"""
    return list(iter_refs(text, form=form))


def unique_refs(refs: Iterable[AssetRef | str]) -> list[str]:
    """按原始路径去重（保序）——取件单位（同一图片被多处引用只取一次）。"""
    seen: dict[str, None] = {}
    for ref in refs:
        raw = ref if isinstance(ref, str) else ref.raw
        seen.setdefault(raw, None)
    return list(seen)


def ref_counts(refs: Iterable[AssetRef]) -> dict[str, int]:
    """引用计数报告（`total` / `md` / `html` / `unique` / `content_addressed`）。"""
    items = list(refs)
    return {
        "total": len(items),
        "md": sum(1 for item in items if item.form == "md"),
        "html": sum(1 for item in items if item.form == "html"),
        "unique": len(unique_refs(items)),
        "content_addressed": sum(1 for item in items if item.sha256 is not None),
    }


def mime_for(extension: str | None, raw: str) -> str:
    """扩展名 → MIME（未知回退 `application/octet-stream`）。"""
    if extension:
        mime = _EXTENSION_MIME.get(extension.lower())
        if mime:
            return mime
    guessed, _ = mimetypes.guess_type(raw)
    return guessed or "application/octet-stream"


def _local_path(ref: AssetRef, source_root: Path) -> Path | None:
    """引用 → 本地路径；URL/绝对外层引用不支持（返回 ``None``，计入 missing）。"""
    raw = ref.raw
    if "://" in raw or raw.startswith("data:"):
        return None
    candidate = Path(raw)
    if candidate.is_absolute():
        # 绝对路径：仅当 source_root 为其前缀之外的隔离目录内才接受（防越界读）
        try:
            candidate.resolve().relative_to(source_root.resolve())
        except (OSError, ValueError):
            return None
        return candidate
    resolved = (source_root / candidate).resolve()
    try:
        resolved.relative_to(source_root.resolve())
    except (OSError, ValueError):
        return None
    return resolved


@dataclass(frozen=True)
class _Fetched:
    ref: str
    sha256: str
    data: bytes
    extension: str | None


def _read(ref: AssetRef, source_root: Path) -> _Fetched | None | str:
    """同步取件：返回 `_Fetched` | `None`（文件不存在）| 字符串（校验失败原因）。"""
    path = _local_path(ref, source_root)
    if path is None:
        return "不支持的引用形态（URL/绝对越界路径）"
    if not path.is_file():
        return None
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if ref.sha256 is not None and digest != ref.sha256:
        return f"sha256 不匹配：文件名 {ref.sha256[:12]}… 实际 {digest[:12]}…"
    return _Fetched(ref=ref.raw, sha256=digest, data=data, extension=ref.extension)


async def resolve_asset(ref: AssetRef, source_root: Path) -> AssetBytes | None:
    """单个引用取件 + 校验；取不到或校验失败 → ``None``（并记日志），从不抛出。"""
    outcome = await asyncio.to_thread(_read, ref, source_root)
    if outcome is None:
        log.info("asset missing", ref=ref.raw, source_root=str(source_root))
        return None
    if isinstance(outcome, str):
        log.warn("asset rejected", ref=ref.raw, reason=outcome)
        return None
    return AssetBytes(
        ref=outcome.ref,
        sha256=outcome.sha256,
        data=outcome.data,
        mime=mime_for(outcome.extension, outcome.ref),
        origin=outcome.ref,
    )


async def _fetch(refs: Sequence[AssetRef | str], source_root: Path) -> tuple[list[AssetBytes], list[str], int]:
    """去重取件 → ``(已取件列表, 缺失清单, 引用总数)``。"""
    items = [ref if isinstance(ref, AssetRef) else _classify(str(ref), "md") for ref in refs]
    unique = unique_refs(items)
    by_raw = {ref.raw: ref for ref in items}
    fetched: list[AssetBytes] = []
    missing: list[str] = []
    for raw in unique:
        resolved = await resolve_asset(by_raw[raw], source_root)
        if resolved is None:
            missing.append(raw)
        else:
            fetched.append(resolved)
    return fetched, missing, len(items)


def fetch_assets(refs: list[str], source_root: Path) -> AssetSyncReport:
    """§3 M03 接口：按引用取件并校验哈希（**不写库**）。

    `total_refs` = 传入引用数（含重复出现）；`fetched`/`missing` 按**去重后的引用路径**计。
    缺失/校验失败**不阻断**（REQ-M03-F05）；写库路径见 :func:`sync_assets`。
    """
    fetched, missing, total = asyncio.run(_fetch([_classify(str(ref), "md") for ref in refs], source_root))
    if missing:
        log.warn(
            "assets missing",
            missing=len(missing),
            fetched=len(fetched),
            total_refs=total,
            source_root=str(source_root),
        )
    else:
        log.info("assets fetched", fetched=len(fetched), total_refs=total)
    return AssetSyncReport(fetched=len(fetched), missing=missing, total_refs=total)


async def sync_assets(
    refs: Sequence[AssetRef | str],
    source_root: Path,
    storage: Any,
) -> AssetSyncReport:
    """取件 + 校验 + 写 `assets`（M02 `put_asset`，内容寻址、幂等去重）。

    只有**校验通过**的字节入 CAS；缺失与校验失败进 `missing`，导入继续（REQ-M03-F05）。
    `storage` 为 :class:`agenticdocer.store.Storage`（duck typing：需 `put_asset`）。
    """
    fetched, missing, total = await _fetch(refs, source_root)
    for asset in fetched:
        await storage.put_asset(asset.data, asset.mime, origin=asset.origin)
    if missing:
        log.warn(
            "assets missing",
            missing=len(missing),
            fetched=len(fetched),
            total_refs=total,
            source_root=str(source_root),
        )
    else:
        log.info("assets synced", fetched=len(fetched), total_refs=total)
    return AssetSyncReport(fetched=len(fetched), missing=missing, total_refs=total)
