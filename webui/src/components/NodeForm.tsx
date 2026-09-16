import { useMemo, useState } from "react";
import Form from "@rjsf/core";
import validator from "@rjsf/validator-ajv8";
import type { RJSFSchema, UiSchema } from "@rjsf/utils";
import type { NodeDTO, SchemaDTO } from "../api/types";
import { ApiError } from "../api/client";
import { nodeApi } from "../api/endpoints";

/** 通用 uiSchema（不针对任何原子类型）：长文本字段给 textarea，其余走 RJSF 默认控件。 */
function uiSchemaFor(schema: RJSFSchema): UiSchema {
  const ui: UiSchema = {};
  const properties = (schema.properties ?? {}) as Record<string, RJSFSchema>;
  for (const [name, property] of Object.entries(properties)) {
    const isLong =
      name === "fragment" ||
      (typeof property.maxLength === "number" && property.maxLength > 80) ||
      property.format === "textarea";
    if (isLong) {
      ui[name] = { "ui:widget": "textarea" };
    } else if (property.format === "uri") {
      ui[name] = { "ui:widget": "uri" };
    }
  }
  return ui;
}

interface Props {
  schemas: SchemaDTO[];
  docId: string;
  /** 编辑既有节点时传入；新建时不传。 */
  node?: NodeDTO;
  /** 可选父节点候选（树中任意 active 节点）。 */
  parentCandidates: Array<{ nodeId: string; anchor: string }>;
  defaultParentId: string | null;
  nextOrdinal: number;
  onSaved: (node: NodeDTO) => void;
  onCancel: () => void;
}

/**
 * schema 驱动表单（REQ-M08-F01「零手写 UI」）。
 * 表单体 = `GET /schemas/{atom_type}` 返回的 jsonSchema 原样交给 RJSF；
 * 新增 atom_type 无需改本组件任何一行——下拉项与表单体都来自 schemas 端点。
 */
export function NodeForm({
  schemas,
  docId,
  node,
  parentCandidates,
  defaultParentId,
  nextOrdinal,
  onSaved,
  onCancel,
}: Props) {
  const [atomType, setAtomType] = useState(node?.atomType ?? schemas[0]?.typeName ?? "");
  const [anchor, setAnchor] = useState(node?.anchor ?? "");
  const [ordinal, setOrdinal] = useState(node?.ordinal ?? nextOrdinal);
  const [parentNodeId, setParentNodeId] = useState<string | null>(
    node?.parentNodeId ?? defaultParentId,
  );
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<ApiError | null>(null);

  const schemaEntry = useMemo(
    () => schemas.find((entry) => entry.typeName === atomType) ?? null,
    [schemas, atomType],
  );

  const rjsfSchema = useMemo<RJSFSchema>(
    () => ((schemaEntry?.jsonSchema ?? {}) as RJSFSchema) ?? {},
    [schemaEntry],
  );
  const uiSchema = useMemo(() => uiSchemaFor(rjsfSchema), [rjsfSchema]);

  const [formData, setFormData] = useState<Record<string, unknown>>(node?.content ?? {});

  async function submit() {
    if (!schemaEntry || !anchor.trim()) {
      return;
    }
    setBusy(true);
    setError(null);
    try {
      const payload: Record<string, unknown> = {
        nodeId: node?.nodeId ?? null,
        docId,
        atomType,
        format: node?.format ?? "md",
        anchor: anchor.trim(),
        ordinal,
        parentNodeId,
        level: node?.level ?? null,
        content: formData,
      };
      if (node) {
        payload.expectedVersion = node.version;
      }
      const saved = await nodeApi.create(payload);
      onSaved(saved);
    } catch (exc) {
      setError(exc instanceof ApiError ? exc : new ApiError(0, String(exc), null, []));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div>
      {error ? (
        <div className="notice error">
          {error.message}
          {error.violations.length > 0 ? (
            <div className="violations">
              {error.violations.map((violation, index) => (
                <div className="v" key={index}>
                  <span className="rule">{violation.ruleId}</span>{" "}
                  <span className="path">@{violation.path}</span> {violation.message}
                  {violation.fixHint ? <span className="hint"> → {violation.fixHint}</span> : null}
                </div>
              ))}
            </div>
          ) : null}
        </div>
      ) : null}

      <label className="field">
        <span>原子类型（来自 /schemas——新增类型无需改前端）</span>
        <select value={atomType} onChange={(e) => setAtomType(e.target.value)}>
          {schemas.map((entry) => (
            <option key={entry.typeName} value={entry.typeName}>
              {entry.typeName}（v{entry.version}）
            </option>
          ))}
        </select>
      </label>

      <div className="row">
        <label className="field" style={{ flex: 2 }}>
          <span>锚（anchor）</span>
          <input type="text" value={anchor} onChange={(e) => setAnchor(e.target.value)} />
        </label>
        <label className="field" style={{ flex: 1 }}>
          <span>ordinal</span>
          <input
            type="number"
            min={0}
            value={ordinal}
            onChange={(e) => setOrdinal(Number(e.target.value))}
          />
        </label>
      </div>

      <label className="field">
        <span>父节点（可空 = 顶层）</span>
        <select
          value={parentNodeId ?? ""}
          onChange={(e) => setParentNodeId(e.target.value === "" ? null : e.target.value)}
        >
          <option value="">（无父节点）</option>
          {parentCandidates
            .filter((candidate) => candidate.nodeId !== node?.nodeId)
            .map((candidate) => (
              <option key={candidate.nodeId} value={candidate.nodeId}>
                {candidate.anchor}
              </option>
            ))}
        </select>
      </label>

      <div className="section-label">content（{atomType || "未选类型"} schema 实时渲染）</div>
      {schemaEntry ? (
        <Form
          schema={rjsfSchema}
          uiSchema={uiSchema}
          formData={formData}
          validator={validator}
          onChange={(event) => setFormData((event.formData ?? {}) as Record<string, unknown>)}
        >
          {/* 表单提交按钮由下方统一渲染 */}
          <span />
        </Form>
      ) : (
        <div className="empty">该类型没有可用 schema。</div>
      )}

      <div className="row end" style={{ marginTop: "var(--sp-3)" }}>
        <button onClick={onCancel}>取消</button>
        <button
          className="primary"
          onClick={() => void submit()}
          disabled={busy || !schemaEntry || !anchor.trim()}
        >
          {busy ? "提交中…" : node ? `保存（乐观锁 v${node.version}）` : "创建节点"}
        </button>
      </div>
    </div>
  );
}
