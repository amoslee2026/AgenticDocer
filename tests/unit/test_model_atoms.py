"""M01 原子 Schema 与 content.text 派生测试（REQ-M01-F01、A10/R5）。"""

from __future__ import annotations

import json

import pytest

from agenticdocer.model import (
    ATOM_SCHEMAS,
    ATOM_TYPES,
    ATOM_VARIANTS,
    SchemaDef,
    UnknownAtomTypeError,
    derive_text,
    get_atom_schema,
    html_to_text,
)
from agenticdocer.model.atoms import TABLE_ATOMS

HTML_TABLE = (
    "<table><tr><td>D0</td><td>7:0</td></tr>"
    "<tr><td>D1</td><td>15:8</td></tr></table>"
)


def test_atom_type_and_variant_domains():
    assert ATOM_TYPES == ("clause", "definition", "table", "figure", "code", "example", "note", "cross_ref")
    assert ATOM_VARIANTS == (
        "table.register_field",
        "figure.state_machine",
        "table.failure_mode",
        "table.coverage_matrix",
    )
    assert set(ATOM_SCHEMAS) == set(ATOM_TYPES) | set(ATOM_VARIANTS)
    assert len(ATOM_SCHEMAS) == 12


@pytest.mark.parametrize("type_name", sorted(ATOM_SCHEMAS))
def test_every_schema_is_well_formed_and_requires_text(type_name: str):
    schema = ATOM_SCHEMAS[type_name]

    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["type"] == "object"
    assert schema["additionalProperties"] is False  # 等价于 pydantic extra="forbid"
    assert "text" in schema["required"]
    assert set(schema["required"]) <= set(schema["properties"])
    assert get_atom_schema(type_name) is schema
    json.dumps(schema)  # 必须可落 schemas.json_schema（JSONB）


def test_nested_table_meta_schema_is_closed_and_typed():
    meta = ATOM_SCHEMAS["table"]["properties"]["meta"]

    assert meta["required"] == ["rows", "cols", "cells", "max_colspan"]
    assert set(meta["properties"]) == {"rows", "cols", "cells", "max_colspan"}
    assert meta["additionalProperties"] is False
    assert ATOM_SCHEMAS["table.register_field"]["required"] == ["text", "fragment", "meta", "register", "fields"]


def test_state_machine_variant_requires_states():
    schema = ATOM_SCHEMAS["figure.state_machine"]

    assert schema["required"] == ["text", "states"]
    assert schema["properties"]["states"]["minItems"] == 1
    assert schema["properties"]["transitions"]["items"]["required"] == ["from", "to"]


def test_cross_ref_variant_enumerates_ref_kinds():
    schema = ATOM_SCHEMAS["cross_ref"]

    assert schema["properties"]["ref_kind"]["enum"] == ["traces_to", "see_also", "composes_from", "source_ref"]
    assert set(schema["required"]) == {"text", "ref_kind", "target_doc_id"}


def test_unknown_atom_type_is_rejected():
    with pytest.raises(UnknownAtomTypeError) as excinfo:
        get_atom_schema("clause.x")

    assert "clause.x" in str(excinfo.value)
    assert "table.register_field" in str(excinfo.value)


def test_schemas_can_seed_the_schemas_table():
    for type_name, schema in ATOM_SCHEMAS.items():
        row = SchemaDef(type_name=type_name, json_schema=schema, version=1)
        assert row.type_name == type_name


# ── html_to_text / derive_text（A10：content.text 为 FTS 唯一来源）────────


def test_html_to_text_strips_tags_and_keeps_row_order():
    assert html_to_text(HTML_TABLE) == "D0 7:0\nD1 15:8"
    assert html_to_text("<p>para one</p><p>para two</p>") == "para one\npara two"
    assert html_to_text("a<br>b &amp; c") == "a b & c"
    assert html_to_text("<div><td>x<sup>2</sup></td></div>") == "x2"


def test_derive_text_for_table_concatenates_cells_in_row_order():
    text = derive_text("table", {"fragment": HTML_TABLE, "meta": {"rows": 2, "cols": 2, "cells": 4, "max_colspan": 1}})

    assert text == "D0 7:0\nD1 15:8"


def test_derive_text_for_register_field_table_uses_fragment():
    text = derive_text(
        "table.register_field",
        {"fragment": HTML_TABLE, "meta": {"rows": 2, "cols": 2, "cells": 4, "max_colspan": 1}, "register": "CTRL", "fields": []},
    )

    assert text == "D0 7:0\nD1 15:8"


def test_derive_text_passes_markdown_and_text_atoms_through():
    assert derive_text("clause", {"text": "**Bold** 条款原文"}) == "**Bold** 条款原文"
    assert derive_text("code", {"text": "reg [7:0] data;"}) == "reg [7:0] data;"
    assert derive_text("note", {"fragment": "plain md text"}) == "plain md text"


def test_derive_text_strips_html_fragments_when_text_absent():
    assert derive_text("note", {"fragment": "<div>目录</div>"}) == "目录"
    assert derive_text("example", {"fragment": "<span>示例</span>"}) == "示例"


def test_derive_text_for_cross_ref_prefers_visible_text():
    assert derive_text("cross_ref", {"text": "§3.2", "ref_kind": "see_also", "target_doc_id": "SPEC-X"}) == "§3.2"
    assert derive_text("cross_ref", {"ref_kind": "source_ref", "target_doc_id": "EXT:https://x"}) == "EXT:https://x"


def test_derive_text_for_state_machine_synthesizes_from_states_and_transitions():
    text = derive_text(
        "figure.state_machine",
        {
            "states": ["IDLE", "BUSY"],
            "transitions": [{"from": "IDLE", "to": "BUSY", "event": "start"}],
        },
    )

    assert text == "IDLE BUSY IDLE->BUSY"


def test_derive_text_is_idempotent_and_rejects_empty_result():
    content = {"text": "条款", "fragment": "<p>条款</p>"}
    derived = derive_text("clause", content)

    assert derive_text("clause", {**content, "text": derived}) == derived
    with pytest.raises(ValueError):
        derive_text("clause", {})
    with pytest.raises(ValueError):
        derive_text("table", {"fragment": "<table></table>"})
    with pytest.raises(ValueError):
        derive_text("clause", {"text": "   "})


def test_derive_text_rejects_unregistered_atom_type():
    with pytest.raises(UnknownAtomTypeError):
        derive_text("clause.typo", {"text": "x"})


def test_table_atoms_set_matches_variant_registration():
    assert TABLE_ATOMS == {"table", "table.register_field", "table.failure_mode", "table.coverage_matrix"}
    assert TABLE_ATOMS <= set(ATOM_SCHEMAS)
