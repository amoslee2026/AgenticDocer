"""RBAC 判定（§3 M10 权限矩阵；**S5 形式化**）。

**角色 = 硬上限**：``role_permits(role, perm)`` 必须为真——``reader`` 即使被授予
``write`` grant 也永远 403（越权 grant 在**授予与判定两处**均拒）。

**grant = 范围收窄器**（ADR-007 §5）：角色决定「能做什么」，grant 决定「在哪些文档上」。
判定式：

.. code-block:: text

    role_permits(user.role, perm)                            # (1) 角色硬上限
      AND ( target is None                                   # (2) 无目标 → 角色作用域
            OR narrowing(user, perm) 为空                    #     该权限无 grant → 角色作用域
            OR ∃ g ∈ narrowing(user, perm) 覆盖 target )      #     收窄：必须落在 grant 范围内

``narrowing(user, perm)`` = 该用户**覆盖请求权限**的 grant 集合（覆盖关系见
:data:`PERMISSION_IMPLIES`）。**按权限分别收窄**是刻意的：只读 grant（``read``）只收窄读，
不连带锁死写/审批维度——``grant_matches`` 的 ``perm`` 形参即此语义。

**权限蕴含**（grant 的 permission → 可满足的请求权限）：

===========  ==================================
grant        可满足的请求
===========  ==================================
``read``     ``read``
``write``    ``read``、``write``（不能写看不见的文档）
``review``   ``read``、``review``（reviewer 不改正文，故不蕴含 ``write``）
===========  ==================================

**scope**（S5：``repo`` 已删除——docs/nodes 无 repo 字段，属悬空概念）：

* ``doc_type``：值为 doc_type（``standard``/``lang``/``tool-manual``/``product``/``safety``）；
* ``doc``：值为 ``doc_id``。

:class:`~agenticdocer.model.DocTarget` 只带 ``doc_id``；调用方若已解析出文档类型，应经
``doc_type=`` 形参传入，否则 ``doc_type`` 范围的 grant 无法命中该目标（fail-closed）。
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Final

from agenticdocer.model import Grant, GrantPermission, GrantTarget, RoleName, User
from agenticdocer.store import ForbiddenError, ValidationError

__all__ = [
    "GRANT_PERMISSIONS",
    "GRANT_SCOPES",
    "MANAGE_USERS",
    "PERMISSIONS",
    "PERMISSION_IMPLIES",
    "ROLE_PERMISSIONS",
    "applicable_grants",
    "authorize",
    "grant_matches",
    "grant_target_matches",
    "permission_implies",
    "role_permits",
    "validate_grant",
    "validate_permission",
]

MANAGE_USERS: Final = "manage_users"

PERMISSIONS: Final = ("read", "write", "review", MANAGE_USERS)
"""完整权限词表（角色上限判定用）。"""

GRANT_PERMISSIONS: Final = ("read", "write", "review")
"""grant 可用的权限（**S5：无 ``admin``/``manage_users``，不可经 grant 提权**）。"""

GRANT_SCOPES: Final = ("doc_type", "doc")
"""grant 作用域（S5：``repo`` 已删除）。"""

ROLE_PERMISSIONS: Final[dict[RoleName, frozenset[str]]] = {
    "admin": frozenset({"read", "write", "review", MANAGE_USERS}),
    "editor": frozenset({"read", "write", "review"}),
    "reviewer": frozenset({"read", "review"}),
    "reader": frozenset({"read"}),
}
"""§3 M10 权限矩阵的四角色基线权限（单一判定口径）。"""

PERMISSION_IMPLIES: Final[dict[str, frozenset[str]]] = {
    "read": frozenset({"read"}),
    "write": frozenset({"read", "write"}),
    "review": frozenset({"read", "review"}),
}
"""grant 权限 → 可满足的请求权限集（见模块文档的表）。"""


def validate_permission(perm: str) -> str:
    """权限词表校验（未知权限 → 422）。"""
    if perm not in PERMISSIONS:
        raise ValidationError(
            f"unknown permission {perm!r}; expected one of {list(PERMISSIONS)}", entity="auth"
        )
    return perm


def role_permits(role: RoleName, perm: str) -> bool:
    """角色硬上限：该角色是否**原则上**拥有该权限（与 grant 无关）。"""
    return perm in ROLE_PERMISSIONS.get(role, frozenset())


def permission_implies(grant_permission: GrantPermission, perm: str) -> bool:
    """grant 的权限是否覆盖请求权限（见模块文档的蕴含表）。"""
    return perm in PERMISSION_IMPLIES.get(grant_permission, frozenset())


def grant_target_matches(
    grant: Grant, target: GrantTarget, *, doc_type: str | None = None
) -> bool:
    """grant 的作用域是否覆盖目标（``doc_type`` 范围可覆盖同类型的文档目标）。"""
    if grant.scope == "doc":
        return target.kind == "doc" and grant.value == target.value
    if grant.scope == "doc_type":
        if target.kind == "doc_type":
            return grant.value == target.value
        return doc_type is not None and grant.value == doc_type
    return False  # pragma: no cover - DDL CHECK 已限定取值域


def applicable_grants(grants: Iterable[Grant], perm: str) -> list[Grant]:
    """收窄集：覆盖请求权限的 grant（该权限维度上用户被限定在此范围内）。"""
    return [g for g in grants if permission_implies(g.permission, perm)]


def grant_matches(
    user: User,
    perm: str,
    target: GrantTarget,
    *,
    grants: Sequence[Grant] = (),
    doc_type: str | None = None,
) -> bool:
    """该用户的 grant 中是否存在一条**覆盖 ``perm`` 且覆盖 ``target``** 的授权。

    ``grants`` 由调用方提供（通常取 :func:`agenticdocer.auth.users.load_grants` 的结果）；
    省略/为空 → ``False``（fail-closed）。
    """
    validate_permission(perm)
    return any(
        grant_target_matches(g, target, doc_type=doc_type)
        for g in applicable_grants(grants, perm)
    )


def authorize(
    user: User,
    perm: str,
    target: GrantTarget | None = None,
    *,
    grants: Sequence[Grant] = (),
    doc_type: str | None = None,
) -> None:
    """判定式（S5）：违规抛 :class:`~agenticdocer.store.ForbiddenError`（403）。

    纯函数、无 I/O——需要读取 grant 并落审计事件的调用方用
    :func:`agenticdocer.auth.users.authorize_user`。
    """
    validate_permission(perm)
    if not role_permits(user.role, perm):
        raise ForbiddenError(
            f"role {user.role!r} does not permit {perm!r}（角色是硬上限，grant 不可提权）",
            entity="auth",
            entity_id=str(user.user_id),
        )
    if target is None:
        return
    narrowing = applicable_grants(grants, perm)
    if not narrowing:
        return
    if any(grant_target_matches(g, target, doc_type=doc_type) for g in narrowing):
        return
    raise ForbiddenError(
        f"{perm!r} on {target.kind}:{target.value} is outside the granted scope of user "
        f"{user.user_id}"
        f"（收窄 grant：{[(g.scope, g.value, g.permission) for g in narrowing]}）",
        entity="auth",
        entity_id=str(user.user_id),
    )


def validate_grant(role: RoleName, scope: str, value: str, permission: str) -> None:
    """**授予侧**校验（S5：越权 grant 在授予时即拒）。

    ``scope``/``permission`` 超出取值域，或 ``role_permits(role, permission)`` 为假
    （如给 ``reader`` 授 ``write``）→ :class:`~agenticdocer.store.ValidationError`（422）。
    """
    if scope not in GRANT_SCOPES:
        raise ValidationError(
            f"unknown grant scope {scope!r}; expected one of {list(GRANT_SCOPES)}", entity="auth"
        )
    if permission not in GRANT_PERMISSIONS:
        raise ValidationError(
            f"grant permission must be one of {list(GRANT_PERMISSIONS)}"
            f"（S5：无 admin，不可经 grant 提权）；got {permission!r}",
            entity="auth",
        )
    if not str(value).strip():
        raise ValidationError("grant value must be non-empty", entity="auth")
    if not role_permits(role, permission):
        raise ValidationError(
            f"role {role!r} does not permit {permission!r}；越权 grant 在授予时即拒（S5）",
            entity="auth",
        )
