"""业务错误码（`DTO_*`）——ADR-010 §1「字段映射」、§3 M12「错误码扩展」。

AgenticLogger 的 `error_code` 字段承载本项目的业务错误码，供
`agentic-logger stats --group-by error_code` 聚合。SDK 自带的 `ErrorCode`
（`PARSE_*`/`IO_*`/`AUTH_*`…）继续用于通用错误；`DTO_*` 表示 **本系统语义** 的错误。

| 码 | 场景 |
|---|---|
| `DTO_PERF_EXCEEDED` | 单次耗时超指标（§1.4；`timer` 越预算时自动写入） |
| `DTO_ANCHOR_CONFLICT` | 锚冲突（映射 M09 `Violation.rule_id`） |
| `DTO_AUTH_REJECTED` | 鉴权拒绝（401/403） |
| `DTO_REF_BROKEN` | 引用断链（M09B `broken_refs`） |
| `DTO_PARTITION_MISSING` | 分区缺失（`events` 未来月份未建） |

`DtoErrorCode` 继承 :class:`enum.StrEnum`，因此 `str(code) == code.value`，
可直接传给 AgenticLogger（SDK 内部对 error_code 做 `str()`）。
"""

from __future__ import annotations

from enum import StrEnum


class DtoErrorCode(StrEnum):
    """AgenticSpec 业务错误码（`DTO_` 前缀）。"""

    DTO_PERF_EXCEEDED = "DTO_PERF_EXCEEDED"
    DTO_ANCHOR_CONFLICT = "DTO_ANCHOR_CONFLICT"
    DTO_AUTH_REJECTED = "DTO_AUTH_REJECTED"
    DTO_REF_BROKEN = "DTO_REF_BROKEN"
    DTO_PARTITION_MISSING = "DTO_PARTITION_MISSING"


DTO_PERF_EXCEEDED = DtoErrorCode.DTO_PERF_EXCEEDED
DTO_ANCHOR_CONFLICT = DtoErrorCode.DTO_ANCHOR_CONFLICT
DTO_AUTH_REJECTED = DtoErrorCode.DTO_AUTH_REJECTED
DTO_REF_BROKEN = DtoErrorCode.DTO_REF_BROKEN
DTO_PARTITION_MISSING = DtoErrorCode.DTO_PARTITION_MISSING

#: `Violation.rule_id` → `DTO_*`（ADR-010 §1：校验违规映射为 error_code）。
#: 仅登记规范中已明确的一对；M09 其余 rule_id 由调用方原样透传（见
#: :func:`error_code_for_rule`），避免在此臆造 M09 的规则命名空间。
VIOLATION_RULE_ERROR_CODES: dict[str, DtoErrorCode] = {
    "RULE_ANCHOR_DUP": DTO_ANCHOR_CONFLICT,
}


def error_code_for_rule(rule_id: str) -> str:
    """把 M09 `Violation.rule_id` 映射为日志 `error_code`。

    已知映射返回 `DTO_*`；未登记的 rule_id 原样透传（日志中仍可按规则名聚合）。
    """
    return VIOLATION_RULE_ERROR_CODES.get(rule_id, rule_id)
