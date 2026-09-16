// §3 M07「前端契约（TS）」——与后端 pydantic（alias_generator=to_camel）对齐。
// 后端实现侧的补充形状（契约超集）以注释标明（M08 报告项）。

export type AtomType =
  | "clause"
  | "definition"
  | "table"
  | "figure"
  | "code"
  | "example"
  | "note"
  | "cross_ref";

export type Format = "md" | "html" | "text";
export type NodeStatus = "active" | "deleted";
export type DocStatus = "draft" | "reviewed" | "approved";
export type RoleName = "admin" | "editor" | "reviewer" | "reader";
export type CommentState = "open" | "resolved" | "orphaned";
export type EntityKind = "doc" | "node" | "ref" | "comment" | "schema" | "auth";
export type GrantScope = "doc_type" | "doc";
export type GrantPermission = "read" | "write" | "review";
export type UserStatus = "active" | "disabled";

export interface NodeDTO {
  nodeId: string;
  docId: string;
  atomType: string;
  format: Format;
  ordinal: number;
  parentNodeId: string | null;
  level: number | null;
  anchor: string;
  content: Record<string, unknown>;
  status: NodeStatus;
  version: number;
  createdAt: string;
  updatedAt: string;
}

export interface DocDTO {
  docId: string;
  docType: string;
  title: string;
  meta: Record<string, unknown>;
  sourceRef: string | null;
  status: DocStatus;
  version: number;
  createdAt: string;
  updatedAt: string;
}

export interface EventDTO {
  eventId: string;
  entity: EntityKind;
  entityId: string;
  op: string;
  payload: Record<string, unknown>;
  actor: string;
  ts: string;
}

export interface CommentDTO {
  commentId: string;
  nodeId: string;
  targetEventId: string | null;
  body: string;
  state: CommentState;
  author: string;
  version: number;
  ts: string;
}

export interface SchemaDTO {
  typeName: string;
  version: number;
  jsonSchema: Record<string, unknown>;
}

export interface UserDTO {
  userId: string;
  username: string;
  role: RoleName;
  status: UserStatus;
  keyFingerprints: string[];
  createdAt: string;
}

export interface GrantDTO {
  /** 实现侧补充（§3 M07 GrantDTO 无此字段，后端 Grant 模型输出含 grantId/grantedBy/grantedAt） */
  grantId: string;
  userId: string;
  scope: GrantScope;
  value: string;
  permission: GrantPermission;
  grantedBy: string | null;
  grantedAt: string;
}

export interface SectionDTO {
  nodeId: string;
  anchor: string;
  title: string;
  level: number;
  ordinal: number;
  childCount: number;
  /** 实现侧补充（§3 M07 块无此字段，后端 SectionDTO.of 输出含 parentNodeId） */
  parentNodeId?: string | null;
}

export interface SessionDTO {
  userId: string;
  username: string;
  role: RoleName;
  permissions: GrantDTO[];
  expiresAt: string | null;
}

export interface ChallengeDTO {
  nonce: string;
  expiresAt: string;
}

/** 渲染响应（M06 RenderOutput：M04 RenderResult + markdown 文本） */
export interface RenderOutputDTO {
  docId: string;
  outPath: string;
  assetsExported: string[];
  section: string | null;
  markdown: string;
}

/** 422/409 违规明细（ErrorResponse.violations[]；ruleId 稳定，勿对 message 断言） */
export interface ViolationDTO {
  ruleId: string;
  path: string;
  message: string;
  fixHint: string | null;
}

/** GET /docs/{id}/diff（REQ-M07-F06） */
export interface DiffEntryDTO {
  nodeId: string | null;
  anchor: string | null;
  op: "added" | "modified" | "deleted" | "ref_added" | "ref_removed" | string;
  field: string | null;
  before: unknown;
  after: unknown;
}

export interface DocDiffDTO {
  docId: string;
  fromTs: string | null;
  toTs: string | null;
  changes: DiffEntryDTO[];
  summary: { added: number; modified: number; deleted: number; refs: number };
}

/** GET /events/replay（NodeSnapshot：折叠态 + 事件序列） */
export interface NodeSnapshotDTO {
  node: NodeDTO | null;
  history: EventDTO[];
}

/** EditableTableMode（§3 M06；前端镜像服务端判定以便决定是否展示编辑器） */
export interface EditableTableModeDTO {
  editable: boolean;
  reason:
    | "flag_on"
    | "doc_type_whitelist"
    | "role_insufficient"
    | "flag_off"
    | "html_fragment";
}

export interface TableEditPayload {
  rows: string[][];
  expectedVersion: number;
  header?: boolean;
  headerNames?: string[];
  registerName?: string | null;
  atomType?: string | null;
}
export interface MetricsSnapshotDTO {
  windowSeconds: number;
  /** 实测实现形状（M12 metrics.py）：{route, count, p50, p95, p99, errorRate}，无 method/maxMillis */
  endpoints: Array<{
    route: string;
    count: number;
    p50: number;
    p95: number;
    p99: number;
    errorRate: number;
  }>;
  slowQueries: Array<Record<string, unknown>>;
  authFailures: number;
  render: Record<string, unknown>;
}

export interface TableHealthDTO {
  name: string;
  rows: number;
  sizeBytes: number;
  deadTup: number;
  lastAutovacuum: string | null;
}

export interface HealthReportDTO {
  tables: TableHealthDTO[];
  indexes: Array<{ name: string; scans: number; sizeBytes: number }>;
  partitions: Array<Record<string, unknown>>;
  pool: Record<string, unknown>;
  advice: string[];
  verdict: string;
}

export interface RoleInfoDTO {
  role: RoleName;
  permissions: string[];
}

export interface TermDTO {
  term: string;
  definitionNodeId: string | null;
  kind: "glossary" | "normative-keyword";
}

export const ROLE_AT_LEAST: Record<RoleName, number> = {
  reader: 0,
  reviewer: 1,
  editor: 2,
  admin: 3,
};

/** ssh_keys 行（keyId = SHA256 指纹，与 ssh-keygen -lf 一致） */
export interface SshKeyDTO {
  keyId: string;
  userId: string;
  keyType: string;
  publicKey: string;
  createdAt: string;
  revokedAt: string | null;
}

