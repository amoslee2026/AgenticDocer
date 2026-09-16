import { useMemo, useState } from "react";
import type { NodeDTO, TableEditPayload } from "../api/types";
import { ApiError } from "../api/client";
import { nodeApi } from "../api/endpoints";

const REGISTER_FIELD_COLUMNS = ["field", "bits", "access", "reset", "description"];
/** 与服务端 TABLE_ATOMS 对齐（render/editable.py）。 */
const TABLE_ATOMS = new Set(["table", "table.register_field"]);

/** 客户端镜像 content_to_grid：fields 优先，其次 HTML 片段（首行 <th> → header）。 */
function gridFromNode(node: NodeDTO): { rows: string[][]; header: boolean; headerNames: string[]; registerName: string | null } {
  const content = node.content ?? {};
  const fields = content.fields;
  if (Array.isArray(fields) && fields.length > 0) {
    const rows = fields
      .filter((item): item is Record<string, unknown> => typeof item === "object" && item !== null)
      .map((item) => REGISTER_FIELD_COLUMNS.map((name) => String(item[name] ?? "")));
    return {
      rows,
      header: true,
      headerNames: [...REGISTER_FIELD_COLUMNS],
      registerName: typeof content.register === "string" ? content.register : null,
    };
  }
  const fragment = content.fragment;
  if (typeof fragment === "string" && fragment.trim()) {
    const doc = new DOMParser().parseFromString(fragment, "text/html");
    const rows: string[][] = [];
    let header = false;
    for (const tr of Array.from(doc.querySelectorAll("tr"))) {
      const cells = Array.from(tr.querySelectorAll("td, th")).map((cell) =>
        (cell.textContent ?? "").trim(),
      );
      if (cells.length > 0) {
        rows.push(cells);
      }
      if (tr.querySelector("th")) {
        header = true;
      }
    }
    return { rows, header, headerNames: [], registerName: null };
  }
  return { rows: [], header: true, headerNames: [], registerName: null };
}

interface Props {
  node: NodeDTO;
  onSaved: (node: NodeDTO) => void;
}

/** 可编辑表格（REQ-M08-F05）：行列增删 + 单元格编辑 → PATCH /nodes/{id}/table。 */
export function TableGridEditor({ node, onSaved }: Props) {
  const initial = useMemo(() => gridFromNode(node), [node]);
  const [rows, setRows] = useState<string[][]>(initial.rows);
  const [header, setHeader] = useState(initial.header);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!TABLE_ATOMS.has(node.atomType)) {
    return <div className="notice error">原子 {node.atomType} 不是表格类，不可行列编辑。</div>;
  }

  function setCell(rowIdx: number, colIdx: number, value: string) {
    setRows((current) =>
      current.map((row, i) => (i === rowIdx ? row.map((cell, j) => (j === colIdx ? value : cell)) : row)),
    );
  }

  function addRow(at: number) {
    setRows((current) => {
      const width = current[0]?.length ?? 1;
      const blank = Array.from({ length: width }, () => "");
      const next = [...current];
      next.splice(at, 0, blank);
      return next;
    });
  }

  function removeRow(at: number) {
    setRows((current) => current.filter((_, i) => i !== at));
  }

  function addColumn() {
    setRows((current) => current.map((row) => [...row, ""]));
  }

  function removeColumn() {
    setRows((current) =>
      current.map((row) => (row.length > 1 ? row.slice(0, row.length - 1) : row)),
    );
  }

  async function submit() {
    setSaving(true);
    setError(null);
    try {
      const payload: TableEditPayload = {
        rows,
        expectedVersion: node.version,
        header,
        headerNames: initial.headerNames,
        registerName: initial.registerName,
      };
      const updated = await nodeApi.patchTable(node.nodeId, payload);
      onSaved(updated);
    } catch (exc) {
      setError(exc instanceof ApiError ? `${exc.message}${exc.code ? `（${exc.code}）` : ""}` : String(exc));
    } finally {
      setSaving(false);
    }
  }

  const columnCount = rows[0]?.length ?? 0;

  return (
    <div className="grid-editor">
      {error ? <div className="notice error">{error}</div> : null}
      <table>
        <tbody>
          {rows.map((row, i) => (
            <tr key={i}>
              {row.map((cell, j) =>
                header && i === 0 ? (
                  <th key={j}>
                    <input value={cell} onChange={(e) => setCell(i, j, e.target.value)} />
                  </th>
                ) : (
                  <td key={j}>
                    <input value={cell} onChange={(e) => setCell(i, j, e.target.value)} />
                  </td>
                ),
              )}
              <td className="row-actions">
                <button className="ghost" title="在此行下方插入一行" onClick={() => addRow(i + 1)}>
                  ＋
                </button>
                <button className="ghost danger" title="删除本行" onClick={() => removeRow(i)}>
                  ✕
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="row" style={{ marginTop: "var(--sp-2)" }}>
        <button onClick={addColumn}>加一列</button>
        <button onClick={removeColumn} disabled={columnCount <= 1}>
          减一列
        </button>
        <button onClick={() => addRow(rows.length)}>末尾加一行</button>
        <label className="row" style={{ gap: "var(--sp-1)", fontSize: "var(--fs-1)", color: "var(--ink-2)" }}>
          <input type="checkbox" checked={header} onChange={(e) => setHeader(e.target.checked)} />
          首行为表头
        </label>
        <div className="spacer" />
        <button className="primary" onClick={() => void submit()} disabled={saving}>
          {saving ? "提交中…" : `提交（乐观锁 v${node.version}）`}
        </button>
      </div>
      {initial.registerName ? (
        <div className="notice" style={{ marginTop: "var(--sp-3)" }}>
          该表为寄存器表（register: <span className="chip">{initial.registerName}</span>），提交将同步回写
          content.fields。
        </div>
      ) : null}
    </div>
  );
}
