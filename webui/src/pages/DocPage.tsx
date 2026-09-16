import { useCallback, useEffect, useMemo, useState } from "react";
import { useParams } from "react-router-dom";
import type { DocDTO, NodeDTO, RenderOutputDTO, SchemaDTO, SectionDTO } from "../api/types";
import { ApiError } from "../api/client";
import { docApi, nodeApi, schemaApi } from "../api/endpoints";
import { roleAtLeast } from "../api/roles";
import { useAuth } from "../auth/AuthContext";
import { useFetch } from "../api/useFetch";
import { MarkdownView } from "../components/MarkdownView";
import { NodeTree } from "../components/NodeTree";
import { CommentsPanel } from "../components/CommentsPanel";
import { DiffView } from "../components/DiffView";
import { HistoryPanel } from "../components/HistoryPanel";
import { NodeDetailPanel } from "../components/NodeDetailPanel";
import { NodeForm } from "../components/NodeForm";

type RightTab = "node" | "comments" | "history" | "diff";
type LeftTab = "sections" | "tree";

const NEXT_STATUS: Record<string, string | null> = {
  draft: "reviewed",
  reviewed: "approved",
  approved: null,
};

/** 文档工作台：章节懒加载（B10）+ 节点树 + 批注 + 历史 + diff。 */
export function DocPage() {
  const { docId = "" } = useParams();
  const { session } = useAuth();
  const [leftTab, setLeftTab] = useState<LeftTab>("sections");
  const [rightTab, setRightTab] = useState<RightTab>("node");
  const [selectedNode, setSelectedNode] = useState<NodeDTO | null>(null);
  const [currentSection, setCurrentSection] = useState<string | null>(null);
  const [renderCache, setRenderCache] = useState<Map<string, RenderOutputDTO>>(new Map());
  const [renderLoading, setRenderLoading] = useState(false);
  const [renderError, setRenderError] = useState<string | null>(null);
  const [showCreate, setShowCreate] = useState(false);
  const [notice, setNotice] = useState<string | null>(null);

  const docState = useFetch(() => docApi.get(docId), [docId]);
  const nodesState = useFetch(() => nodeApi.listByDoc(docId), [docId]);
  const sectionsState = useFetch(() => nodeApi.sections(docId), [docId]);
  const schemasState = useFetch(() => schemaApi.list(), [docId]);

  const doc: DocDTO | null = docState.data;
  const nodes = nodesState.data ?? [];
  const sections: SectionDTO[] = sectionsState.data ?? [];
  const schemas: SchemaDTO[] = schemasState.data ?? [];

  // B10：进入文档只取章节清单；首个章节按需渲染。
  useEffect(() => {
    if (sections.length === 0 || currentSection !== null) {
      return;
    }
    setCurrentSection(sections[0].anchor);
  }, [sections, currentSection]);

  const loadSection = useCallback(
    async (section: string | null, force = false) => {
      const key = section ?? "<full>";
      setRenderError(null);
      if (!force && renderCache.has(key)) {
        return;
      }
      setRenderLoading(true);
      try {
        const output = await nodeApi.render(docId, section ?? undefined);
        setRenderCache((current) => new Map(current).set(key, output));
      } catch (exc) {
        setRenderError(exc instanceof ApiError ? exc.message : String(exc));
      } finally {
        setRenderLoading(false);
      }
    },
    [docId, renderCache],
  );

  useEffect(() => {
    if (currentSection !== null) {
      void loadSection(currentSection);
    }
  }, [currentSection, loadSection]);


  const nodesById = useMemo(() => {
    const map = new Map<string, NodeDTO>();
    for (const node of nodes) {
      map.set(node.nodeId, node);
    }
    return map;
  }, [nodes]);

  const rendered = renderCache.get(currentSection ?? "<full>") ?? null;
  useEffect(() => {
    if (selectedNode || nodes.length === 0) {
      return;
    }
    const sectionNode = sections[0] ? nodesById.get(sections[0].nodeId) : undefined;
    if (sectionNode) {
      setSelectedNode(sectionNode);
    }
  }, [nodes, nodesById, sections, selectedNode]);

  async function advanceStatus() {
    if (!doc) {
      return;
    }
    const next = NEXT_STATUS[doc.status];
    if (!next) {
      return;
    }
    setNotice(null);
    try {
      await docApi.setStatus(doc.docId, next, doc.version);
      await docState.reload();
      setNotice(`状态已流转为 ${next}。`);
    } catch (exc) {
      setNotice(exc instanceof ApiError ? exc.message : String(exc));
    }
  }

  if (docState.loading) {
    return <div className="page"><div className="loading">载入文档…</div></div>;
  }
  if (docState.error || !doc) {
    return (
      <div className="page">
        <div className="notice error">{docState.error?.message ?? "文档不存在"}</div>
      </div>
    );
  }

  const sessionRole = session?.role ?? "reader";
  const canReview = roleAtLeast(sessionRole, "reviewer");
  const canWrite = roleAtLeast(sessionRole, "editor");
  const nextStatus = NEXT_STATUS[doc.status];
  if (!session) {
    return null;
  }

  return (
    <div className="page">
      <div className="page-head">
        <div>
          <h1 className="doc-title">{doc.title}</h1>
          <div className="doc-sub">
            {doc.docId} · {doc.docType} · v{doc.version} · 更新 {doc.updatedAt.replace("T", " ").slice(0, 16)}
            {doc.meta.editable_tables === true ? " · editable_tables" : ""}
          </div>
        </div>
        <div className="row">
          <span className={`badge ${doc.status}`}>{doc.status}</span>
          {canReview && nextStatus ? (
            <button onClick={() => void advanceStatus()}>流转 → {nextStatus}</button>
          ) : null}
          {canWrite ? (
            <button className="primary" onClick={() => setShowCreate(true)}>
              新建节点（schema 表单）
            </button>
          ) : null}
        </div>
        <div className="card">
          <div className="card-head">
            <div className="tabs" style={{ margin: 0, borderBottom: "none" }}>
              <button className={leftTab === "sections" ? "current" : ""} onClick={() => setLeftTab("sections")}>
                章节
              </button>
              <button className={leftTab === "tree" ? "current" : ""} onClick={() => setLeftTab("tree")}>
                节点树
              </button>
            </div>
          </div>
          <div style={{ maxHeight: 640, overflowY: "auto" }}>
            {leftTab === "sections" ? (
              sectionsState.loading ? (
                <div className="loading">载入章节清单…</div>
              ) : (
                <ul className="section-list">
                  {sections.map((section) => (
                    <li key={section.nodeId}>
                      <button
                        className={section.anchor === currentSection ? "current" : ""}
                        style={{ paddingLeft: `calc(var(--sp-2) + ${(section.level - 1) * 14}px)` }}
                        onClick={() => setCurrentSection(section.anchor)}
                      >
                        <span className="sec-anchor">{section.anchor}</span>
                        {section.title}
                        <span className="sec-kids">{section.childCount}</span>
                      </button>
                    </li>
                  ))}
                </ul>
              )
            ) : (
              <div style={{ padding: "var(--sp-2)" }}>
                <NodeTree
                  nodes={nodes}
                  selectedId={selectedNode?.nodeId ?? null}
                  onSelect={(node) => {
                    setSelectedNode(node);
                    setRightTab("node");
                  }}
                />
              </div>
            )}
          </div>
        </div>

        <div className="card">
          <div className="card-head">
            <h2>{currentSection === null ? "整档渲染" : `章节渲染：${currentSection}`}</h2>
            <div className="row">
              <button
                className={currentSection === null ? "ghost" : ""}
                onClick={() => setCurrentSection(null)}
              >
                整档
              </button>
              <button
                className="ghost"
                onClick={() => {
                  setRenderCache((current) => {
                    const next = new Map(current);
                    next.delete(currentSection ?? "<full>");
                    return next;
                  });
                  void loadSection(currentSection, true);
                }}
              >
                重新渲染
              </button>
            </div>
          </div>
          <div className="card-body">
            {renderError ? <div className="notice error">{renderError}</div> : null}
            {renderLoading ? <div className="loading">渲染章节中…（目标 &lt;1s）</div> : null}
            {rendered ? <MarkdownView markdown={rendered.markdown} /> : null}
            {!rendered && !renderLoading ? (
              <div className="empty">选择左侧章节按需渲染（B10：分章节加载）。</div>
            ) : null}
          </div>
        </div>

        <div className="card right-pane">
          <div className="card-head">
            <div className="tabs" style={{ margin: 0, borderBottom: "none" }}>
              <button className={rightTab === "node" ? "current" : ""} onClick={() => setRightTab("node")}>
                节点
              </button>
              <button className={rightTab === "comments" ? "current" : ""} onClick={() => setRightTab("comments")}>
                批注
              </button>
              <button className={rightTab === "history" ? "current" : ""} onClick={() => setRightTab("history")}>
                历史
              </button>
              <button className={rightTab === "diff" ? "current" : ""} onClick={() => setRightTab("diff")}>
                Diff
              </button>
            </div>
          </div>
          <div className="card-body" style={{ maxHeight: 640, overflowY: "auto" }}>
            {rightTab === "node" ? (
              selectedNode ? (
                <NodeDetailPanel
                  doc={doc}
                  schemas={schemas}
                  nodes={nodes}
                  session={session}
                  node={selectedNode}
                  onNodeChanged={async (saved) => {
                    setSelectedNode(saved);
                    await Promise.all([nodesState.reload(), docState.reload()]);
                    if (currentSection !== null) {
                      setRenderCache((current) => {
                        const next = new Map(current);
                        next.delete(currentSection);
                        next.delete("<full>");
                        return next;
                      });
                      void loadSection(currentSection);
                    }
                  }}
                  onDocRefresh={() => void nodesState.reload()}
                  onDeleted={() => void Promise.all([nodesState.reload(), sectionsState.reload()])}
                />
              ) : (
                <div className="empty">在节点树中选择一个节点。</div>
              )
            ) : null}
            {rightTab === "comments" ? (
              <CommentsPanel
                docId={doc.docId}
                nodes={nodes}
                selectedNode={selectedNode}
                canReview={canReview}
                onNodeJump={(node) => {
                  setSelectedNode(node);
                  setRightTab("node");
                }}
                onChanged={() => void nodesState.reload()}
              />
            ) : null}
            {rightTab === "history" ? (
              selectedNode ? (
                <HistoryPanel node={selectedNode} />
              ) : (
                <div className="empty">选择节点后查看其版本历史。</div>
              )
            ) : null}
            {rightTab === "diff" ? <DiffView docId={doc.docId} /> : null}
          </div>
        </div>
      </div>

      {showCreate ? (
        <div className="modal-backdrop" onClick={() => setShowCreate(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="card-head">
              <h2>新建节点</h2>
              <button className="ghost" onClick={() => setShowCreate(false)}>
                ✕
              </button>
            </div>
            <div className="card-body">
              {schemasState.loading ? (
                <div className="loading">载入 schema 注册表…</div>
              ) : (
                <NodeForm
                  schemas={schemas}
                  docId={doc.docId}
                  parentCandidates={nodes
                    .filter((candidate) => candidate.status === "active")
                    .map((candidate) => ({ nodeId: candidate.nodeId, anchor: candidate.anchor }))}
                  defaultParentId={selectedNode?.nodeId ?? null}
                  nextOrdinal={nodes.length}
                  onSaved={async (saved) => {
                    setShowCreate(false);
                    setSelectedNode(saved);
                    await Promise.all([nodesState.reload(), sectionsState.reload(), docState.reload()]);
                  }}
                  onCancel={() => setShowCreate(false)}
                />
              )}
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
}
