"""M10 RBAC 单测（S5 形式化：角色硬上限 + grant 收窄；REQ-M10-F04 a–f）。

纯函数，不需要 PG；DB 侧（授予时 422、判定时 403 的**两处均拒**）在集成测试覆盖。
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from agenticdocer.auth import rbac
from agenticdocer.model import DocTarget, DocTypeTarget, Grant, User, new_uuid7
from agenticdocer.store import ForbiddenError, ValidationError

NOW = datetime(2026, 9, 16, tzinfo=timezone.utc)


def _user(role: str) -> User:
    return User(
        user_id=new_uuid7(),
        username=f"u-{role}",
        role=role,
        status="active",
        created_at=NOW,
        updated_at=NOW,
    )


def _grant(user: User, scope: str, value: str, permission: str) -> Grant:
    return Grant(
        grant_id=new_uuid7(),
        user_id=user.user_id,
        scope=scope,
        value=value,
        permission=permission,
        granted_by=None,
        granted_at=NOW,
    )


# ------------------------------------------------------------------ 角色矩阵


def test_role_permissions_are_the_four_role_matrix() -> None:
    assert rbac.ROLE_PERMISSIONS == {
        "admin": frozenset({"read", "write", "review", "manage_users"}),
        "editor": frozenset({"read", "write", "review"}),
        "reviewer": frozenset({"read", "review"}),
        "reader": frozenset({"read"}),
    }
    assert rbac.GRANT_PERMISSIONS == ("read", "write", "review")
    assert rbac.GRANT_SCOPES == ("doc_type", "doc")  # S5：repo 已删除
    assert "admin" not in rbac.GRANT_PERMISSIONS  # grant 不可提权


@pytest.mark.parametrize(
    ("role", "perm", "expected"),
    [
        ("admin", "read", True),
        ("admin", "write", True),
        ("admin", "review", True),
        ("admin", "manage_users", True),
        ("editor", "write", True),
        ("editor", "review", True),
        ("editor", "manage_users", False),
        ("reviewer", "review", True),
        ("reviewer", "write", False),
        ("reviewer", "manage_users", False),
        ("reader", "read", True),
        ("reader", "write", False),
        ("reader", "review", False),
        ("reader", "manage_users", False),
        ("reader", "unknown", False),
    ],
)
def test_role_permits_matrix(role: str, perm: str, expected: bool) -> None:
    assert rbac.role_permits(role, perm) is expected  # type: ignore[arg-type]


def test_authorize_without_target_is_role_scoped() -> None:
    rbac.authorize(_user("editor"), "write")
    rbac.authorize(_user("admin"), "manage_users")
    with pytest.raises(ForbiddenError) as excinfo:
        rbac.authorize(_user("reader"), "write")
    assert excinfo.value.status_code == 403


def test_authorize_rejects_unknown_permission() -> None:
    with pytest.raises(ValidationError):
        rbac.authorize(_user("admin"), "sudo")


# ------------------------------------------------ S5：角色硬上限（授予与判定两处）


def test_reader_write_grant_rejected_at_grant_time() -> None:
    with pytest.raises(ValidationError) as excinfo:
        rbac.validate_grant("reader", "doc", "SPEC-A", "write")
    assert excinfo.value.status_code == 422


def test_reader_write_grant_still_forbidden_at_decision_time() -> None:
    # 即便绕过授予侧校验把 write grant 写进库，判定时仍被角色硬上限拦下（REQ-M10-F04e）
    reader = _user("reader")
    smuggled = _grant(reader, "doc", "SPEC-A", "write")
    for target in (None, DocTarget(value="SPEC-A")):
        with pytest.raises(ForbiddenError):
            rbac.authorize(reader, "write", target, grants=[smuggled])


def test_validate_grant_rejects_bad_scope_permission_and_value() -> None:
    for scope, permission in (("repo", "read"), ("doc_type", "admin"), ("doc", "manage_users")):
        with pytest.raises(ValidationError):
            rbac.validate_grant("admin", scope, "SPEC-A", permission)
    with pytest.raises(ValidationError):
        rbac.validate_grant("admin", "doc", "   ", "read")
    # 合法组合不抛
    rbac.validate_grant("editor", "doc_type", "product", "write")
    rbac.validate_grant("reviewer", "doc", "SPEC-A", "review")


# ------------------------------------------------------------------ grant 收窄


def test_grants_absent_means_role_scope() -> None:
    editor = _user("editor")
    rbac.authorize(editor, "write", DocTarget(value="SPEC-OTHER"))
    assert rbac.grant_matches(editor, "write", DocTarget(value="SPEC-OTHER")) is False


def test_doc_scope_grant_narrows_that_permission() -> None:
    editor = _user("editor")
    grants = [_grant(editor, "doc", "SPEC-A", "write")]

    rbac.authorize(editor, "write", DocTarget(value="SPEC-A"), grants=grants)
    with pytest.raises(ForbiddenError):
        rbac.authorize(editor, "write", DocTarget(value="SPEC-B"), grants=grants)

    assert rbac.grant_matches(editor, "write", DocTarget(value="SPEC-A"), grants=grants) is True
    assert rbac.grant_matches(editor, "write", DocTarget(value="SPEC-B"), grants=grants) is False


def test_doc_type_grant_covers_same_type_documents_only() -> None:
    editor = _user("editor")
    grants = [_grant(editor, "doc_type", "product", "write")]

    # 「editor 仅在 product 类型上可写」（§3 M10 判定式示例）
    rbac.authorize(
        editor, "write", DocTarget(value="SPEC-A"), grants=grants, doc_type="product"
    )
    rbac.authorize(editor, "write", DocTypeTarget(value="product"), grants=grants)
    with pytest.raises(ForbiddenError):
        rbac.authorize(
            editor, "write", DocTarget(value="SPEC-B"), grants=grants, doc_type="standard"
        )
    with pytest.raises(ForbiddenError):
        rbac.authorize(editor, "write", DocTypeTarget(value="standard"), grants=grants)
    # doc_type 未知时 doc_type 范围 grant 无法命中 → fail-closed
    with pytest.raises(ForbiddenError):
        rbac.authorize(editor, "write", DocTarget(value="SPEC-A"), grants=grants)


def test_doc_type_grant_does_not_match_a_doc_scope_target_of_other_scope() -> None:
    editor = _user("editor")
    grants = [_grant(editor, "doc", "SPEC-A", "write")]
    # doc 范围 grant 不覆盖 doc_type 目标（scope 不可互相冒充）
    with pytest.raises(ForbiddenError):
        rbac.authorize(editor, "write", DocTypeTarget(value="product"), grants=grants)


def test_narrowing_is_per_permission() -> None:
    """只读 grant 只收窄读；写/审批维度不受该 grant 影响（``grant_matches`` 的 perm 语义）。"""
    editor = _user("editor")
    grants = [_grant(editor, "doc", "SPEC-A", "read")]

    rbac.authorize(editor, "read", DocTarget(value="SPEC-A"), grants=grants)
    with pytest.raises(ForbiddenError):
        rbac.authorize(editor, "read", DocTarget(value="SPEC-B"), grants=grants)
    # read 不蕴含 write → write 维度无收窄 grant → 仍按角色作用域
    rbac.authorize(editor, "write", DocTarget(value="SPEC-B"), grants=grants)


def test_write_grant_implies_read_but_review_does_not_imply_write() -> None:
    editor = _user("editor")
    write_grant = [_grant(editor, "doc", "SPEC-A", "write")]
    # write ⇒ read：能写就能读（且读也被收窄到 SPEC-A）
    rbac.authorize(editor, "read", DocTarget(value="SPEC-A"), grants=write_grant)
    with pytest.raises(ForbiddenError):
        rbac.authorize(editor, "read", DocTarget(value="SPEC-B"), grants=write_grant)

    review_grant = [_grant(editor, "doc", "SPEC-A", "review")]
    # review ⇏ write：批注权限不扩到正文修改
    assert rbac.permission_implies("review", "write") is False
    rbac.authorize(editor, "write", DocTarget(value="SPEC-B"), grants=review_grant)
    rbac.authorize(editor, "review", DocTarget(value="SPEC-A"), grants=review_grant)
    with pytest.raises(ForbiddenError):
        rbac.authorize(editor, "review", DocTarget(value="SPEC-B"), grants=review_grant)


def test_applicable_grants_filters_by_permission() -> None:
    editor = _user("editor")
    grants = [
        _grant(editor, "doc", "SPEC-A", "read"),
        _grant(editor, "doc_type", "product", "write"),
    ]
    assert rbac.applicable_grants(grants, "read") == grants  # write 蕴含 read
    assert [g.scope for g in rbac.applicable_grants(grants, "write")] == ["doc_type"]
    assert rbac.applicable_grants(grants, "review") == []


def test_grant_target_matches_supports_both_scope_kinds() -> None:
    editor = _user("editor")
    doc_grant = _grant(editor, "doc", "SPEC-A", "read")
    type_grant = _grant(editor, "doc_type", "standard", "read")

    assert rbac.grant_target_matches(doc_grant, DocTarget(value="SPEC-A")) is True
    assert rbac.grant_target_matches(doc_grant, DocTypeTarget(value="standard")) is False
    assert rbac.grant_target_matches(type_grant, DocTypeTarget(value="standard")) is True
    assert rbac.grant_target_matches(type_grant, DocTarget(value="SPEC-A"), doc_type="standard")
    assert not rbac.grant_target_matches(
        type_grant, DocTarget(value="SPEC-A"), doc_type="product"
    )
