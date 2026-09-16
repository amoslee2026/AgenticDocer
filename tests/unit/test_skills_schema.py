"""skills/ 契约机检（REQ-M11-F05/F06/F07 的 V17 判据）。

三件事：

1. **四字段齐备且过 JSON Schema**（``skills/skill.schema.json``，``additionalProperties: false``）；
2. **底层命令可达**：``command`` 字段里出现的 ``agenticdocer <group> <sub>`` 必须真实注册在 Typer app 上；
3. **前置角色与 M10 权限矩阵一致**：skill 声明的最低角色 = 由底层命令推导出的权限所需的最低角色；
   另校验正文含封装语义小节（何时用/前置角色/底层命令/失败与重试/权限不足补救）。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Final

import jsonschema
import pytest
import yaml

from agenticdocer import cli

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / "skills"
SCHEMA_PATH = SKILLS / "skill.schema.json"
FIELDS: Final = ("name", "description", "role", "command")
EXPECTED_SKILLS: Final = (
    "docer-annotations",
    "docer-diff",
    "docer-import",
    "docer-read",
    "docer-render",
    "docer-write",
)
REQUIRED_SECTIONS: Final = ("何时用", "前置角色", "底层命令", "失败与重试", "权限不足补救")

#: 底层命令片段 → 所需权限（与 M10 权限矩阵同源；顺序即强度）。
_PERMISSION_TOKENS: Final[tuple[tuple[str, str], ...]] = (
    ("user ", cli.MANAGE_USERS),
    ("grant ", cli.MANAGE_USERS),
    ("node put", "write"),
    ("node delete", "write"),
    ("doc delete", "write"),
    ("import commit", "write"),
    ("comment add", "review"),
    ("comment resolve", "review"),
)


def _schema() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _frontmatter(path: Path) -> dict[str, Any]:
    """``SKILL.md`` 的 YAML frontmatter（``---`` 包裹的第一块）。"""
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"{path} 缺少 frontmatter"
    body = text.split("\n---\n", 1)[0][len("---\n") :]
    loaded = yaml.safe_load(body)
    assert isinstance(loaded, dict), f"{path} frontmatter 不是映射"
    return loaded


def _skill_paths() -> list[Path]:
    return sorted(SKILLS.glob("*/SKILL.md"))


def test_schema_itself_is_valid() -> None:
    jsonschema.Draft202012Validator.check_schema(_schema())


def test_exactly_the_six_spec_skills_exist() -> None:
    found = tuple(sorted(path.parent.name for path in _skill_paths()))
    assert found == EXPECTED_SKILLS


@pytest.mark.parametrize("path", _skill_paths(), ids=lambda path: path.parent.name)
def test_skill_declares_exactly_the_four_fields(path: Path) -> None:
    """V17(a)：``name``/``description``/前置角色/底层命令四字段，且可被 JSON Schema 校验通过。"""
    data = _frontmatter(path)
    assert tuple(sorted(data)) == tuple(sorted(FIELDS)), sorted(data)
    jsonschema.validate(instance=data, schema=_schema())
    assert data["name"] == path.parent.name
    assert data["role"] in ("reader", "reviewer", "editor", "admin")
    assert "agenticdocer" in data["command"]


def test_schema_rejects_missing_field_and_extra_field() -> None:
    """判据必须**有牙齿**：缺字段、多字段、越界角色都要被拒。"""
    validator = jsonschema.Draft202012Validator(_schema())
    base = {"name": "docer-x", "description": "d" * 20, "role": "reader", "command": "agenticdocer doc list"}
    assert not list(validator.iter_errors(base))
    for broken in (
        {key: value for key, value in base.items() if key != "role"},
        {key: value for key, value in base.items() if key != "command"},
        {**base, "extra": 1},
        {**base, "role": "root"},
        {**base, "name": "import"},
        {**base, "description": "too short"},
    ):
        assert list(validator.iter_errors(broken)), broken


def _registered_paths() -> set[tuple[str, ...]]:
    """Typer 注册表里的叶子命令路径（``(group, name)`` / ``("user", "key", "add")``）。"""
    paths: set[tuple[str, ...]] = set()

    def walk(application: Any, prefix: tuple[str, ...], seen: frozenset[int]) -> None:
        registered = {id(application)}
        for info in application.registered_commands:
            name = info.name or (info.callback.__name__ if info.callback else "")
            paths.add((*prefix, name.replace("_", "-")))
        for info in application.registered_groups:
            child = info.typer_instance
            if child is None or id(child) in registered:
                continue
            walk(child, (*prefix, info.name or ""), seen | frozenset({id(child)}))

    walk(cli.app, (), frozenset())
    return paths


@pytest.mark.parametrize("path", _skill_paths(), ids=lambda path: path.parent.name)
def test_skill_commands_are_reachable(path: Path) -> None:
    """skill 声明的底层命令必须真实存在（防文档漂移）。"""
    registered = _registered_paths()
    tokens = [token.strip() for token in _frontmatter(path)["command"].split("|") if token.strip()]
    matched = 0
    for token in tokens:
        parts = token.split()
        assert parts[0] == "agenticdocer", token
        candidates = [tuple(part.replace("|", "") for part in parts[1 : index + 1]) for index in range(1, len(parts))]
        if any(candidate in registered for candidate in candidates):
            matched += 1
    assert matched == len(tokens), (path, tokens, sorted(registered))


@pytest.mark.parametrize("path", _skill_paths(), ids=lambda path: path.parent.name)
def test_skill_role_matches_permission_matrix(path: Path) -> None:
    """前置角色 = 底层命令所需的**最低**角色（M10 权限矩阵；防止 skill 低报权限）。"""
    data = _frontmatter(path)
    required = "read"
    for token, permission in _PERMISSION_TOKENS:
        if token in data["command"] and permission != "read":
            required = permission if required == "read" else required
            if permission == cli.MANAGE_USERS:
                required = cli.MANAGE_USERS
    assert data["role"] == cli._min_role(required), (data["command"], required)


@pytest.mark.parametrize("path", _skill_paths(), ids=lambda path: path.parent.name)
def test_skill_body_covers_wrapping_semantics(path: Path) -> None:
    """REQ-M11-F05：封装「何时用、如何解读输出、失败重试、所需角色」。"""
    text = path.read_text(encoding="utf-8")
    for section in REQUIRED_SECTIONS:
        assert section in text, (path, section)
    assert "--json" in text and "--dry-run" in text


def test_readme_lists_every_skill() -> None:
    readme = (SKILLS / "README.md").read_text(encoding="utf-8")
    for name in EXPECTED_SKILLS:
        assert name in readme, name
    assert "skill.schema.json" in readme
