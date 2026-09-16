import { useMemo } from "react";
import type { NodeDTO } from "../api/types";

interface Props {
  nodes: NodeDTO[];
  selectedId: string | null;
  onSelect: (node: NodeDTO) => void;
}

interface TreeItem {
  node: NodeDTO;
  children: TreeItem[];
}

function buildTree(nodes: NodeDTO[]): TreeItem[] {
  const items = new Map<string, TreeItem>();
  for (const node of nodes) {
    items.set(node.nodeId, { node, children: [] });
  }
  const roots: TreeItem[] = [];
  for (const item of items.values()) {
    const parentId = item.node.parentNodeId;
    const parent = parentId ? items.get(parentId) : undefined;
    if (parent && parent !== item) {
      parent.children.push(item);
    } else {
      roots.push(item);
    }
  }
  const byOrdinal = (a: TreeItem, b: TreeItem) => a.node.ordinal - b.node.ordinal;
  for (const item of items.values()) {
    item.children.sort(byOrdinal);
  }
  return roots.sort(byOrdinal);
}

function TreeView({
  items,
  selectedId,
  onSelect,
  depth,
}: {
  items: TreeItem[];
  selectedId: string | null;
  onSelect: (node: NodeDTO) => void;
  depth: number;
}) {
  if (items.length === 0 && depth === 0) {
    return <div className="empty">文档暂无节点。</div>;
  }
  return (
    <ul className="tree">
      {items.map((item) => (
        <li key={item.node.nodeId}>
            className={`node-row${item.node.nodeId === selectedId ? " current" : ""}`}
            onClick={() => onSelect(item.node)}
          >
            <span className="node-type">{item.node.atomType}</span>
            <span className="node-anchor">{item.node.anchor}</span>
            {item.node.status === "deleted" ? <span className="badge deleted">deleted</span> : null}
          </div>
          {item.children.length > 0 ? (
            <TreeView items={item.children} selectedId={selectedId} onSelect={onSelect} depth={depth + 1} />
          ) : null}
        </li>
      ))}
    </ul>
  );
}

/** 节点树浏览：按 parentNodeId 组树、ordinal 排序。 */
export function NodeTree({ nodes, selectedId, onSelect }: Props) {
  const tree = useMemo(() => buildTree(nodes), [nodes]);
  return <TreeView items={tree} nodes={nodes} selectedId={selectedId} onSelect={onSelect} depth={0} />;
}
