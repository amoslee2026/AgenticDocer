// 数据访问层：每个端点一个薄封装（camelCase 契约见 ./types）。
import { apiDelete, apiGet, apiPatch, apiPost } from "./client";
import type {
  ChallengeDTO,
  CommentDTO,
  DocDiffDTO,
  DocDTO,
  EventDTO,
  GrantDTO,
  HealthReportDTO,
  MetricsSnapshotDTO,
  NodeDTO,
  NodeSnapshotDTO,
  RenderOutputDTO,
  RoleInfoDTO,
  SchemaDTO,
  SectionDTO,
  SessionDTO,
  SshKeyDTO,
  TableEditPayload,
  TermDTO,
  UserDTO,
} from "./types";
// ── M10 鉴权 ────────────────────────────────────────────────────────────

export const authApi = {
  challenge: () => apiPost<ChallengeDTO>("/api/v1/auth/challenge"),
  login: (keyFingerprint: string, nonce: string, signature: string) =>
    apiPost<SessionDTO>("/api/v1/auth/login", { keyFingerprint, nonce, signature }),
  logout: () => apiPost<void>("/api/v1/auth/logout"),
  me: () => apiGet<SessionDTO>("/api/v1/auth/me"),
};

// ── M06 节点/渲染 ───────────────────────────────────────────────────────

export const nodeApi = {
  get: (nodeId: string, docId?: string) =>
    apiGet<NodeDTO>(
      `/api/v1/nodes/${nodeId}${docId ? `?doc_id=${encodeURIComponent(docId)}` : ""}`,
    ),
  listByDoc: (docId: string, includeDeleted = false) =>
    apiGet<NodeDTO[]>(
      `/api/v1/docs/${encodeURIComponent(docId)}/nodes${includeDeleted ? "?include_deleted=true" : ""}`,
    ),
  create: (payload: Record<string, unknown>) => apiPost<NodeDTO>("/api/v1/nodes", payload),
  delete: (nodeId: string, expectedVersion: number) =>
    apiDelete(`/api/v1/nodes/${nodeId}?expected_version=${expectedVersion}`),
  sections: (docId: string) =>
    apiGet<SectionDTO[]>(`/api/v1/docs/${encodeURIComponent(docId)}/sections`),
  render: (docId: string, section?: string) =>
    apiGet<RenderOutputDTO>(
      `/api/v1/docs/${encodeURIComponent(docId)}/render${section ? `?section=${encodeURIComponent(section)}` : ""}`,
    ),
  patchTable: (nodeId: string, payload: TableEditPayload) =>
    apiPatch<NodeDTO>(`/api/v1/nodes/${nodeId}/table`, payload),
};

// ── M07 WebUI API ───────────────────────────────────────────────────────

export const docApi = {
  list: (status?: string) => apiGet<DocDTO[]>(`/api/v1/docs${status ? `?status=${status}` : ""}`),
  get: (docId: string) => apiGet<DocDTO>(`/api/v1/docs/${encodeURIComponent(docId)}`),
  setStatus: (docId: string, status: string, expectedVersion: number) =>
    apiPost<DocDTO>(`/api/v1/docs/${encodeURIComponent(docId)}/status`, { status, expectedVersion }),
  diff: (docId: string, from?: string, to?: string) => {
    const params = new URLSearchParams();
    if (from) {
      params.set("from", from);
    }
    if (to) {
      params.set("to", to);
    }
    const query = params.toString();
    return apiGet<DocDiffDTO>(
      `/api/v1/docs/${encodeURIComponent(docId)}/diff${query ? `?${query}` : ""}`,
    );
  },
};

export const schemaApi = {
  list: () => apiGet<SchemaDTO[]>("/api/v1/schemas"),
  get: (atomType: string) =>
    apiGet<SchemaDTO>(`/api/v1/schemas/${encodeURIComponent(atomType)}`),
  register: (typeName: string, jsonSchema: Record<string, unknown>, version = 1) =>
    apiPost<SchemaDTO>("/api/v1/schemas", { typeName, jsonSchema, version }),
};

export const termApi = {
  list: () => apiGet<TermDTO[]>("/api/v1/terms"),
  upsert: (term: string, kind: string, definitionNodeId?: string | null) =>
    apiPost<TermDTO>("/api/v1/terms", {
      term,
      kind,
      definitionNodeId: definitionNodeId ?? null,
    }),
};

export const eventApi = {
  list: (params: { entity?: string; entityId?: string; since?: string; limit?: number }) => {
    const search = new URLSearchParams();
    if (params.entity) {
      search.set("entity", params.entity);
    }
    if (params.entityId) {
      search.set("entity_id", params.entityId);
    }
    if (params.since) {
      search.set("since", params.since);
    }
    if (params.limit) {
      search.set("limit", String(params.limit));
    }
    const query = search.toString();
    return apiGet<EventDTO[]>(`/api/v1/events${query ? `?${query}` : ""}`);
  },
  replayNode: (nodeId: string, upto?: string) =>
    apiGet<NodeSnapshotDTO>(
      `/api/v1/events/replay?node_id=${nodeId}${upto ? `&upto=${encodeURIComponent(upto)}` : ""}`,
    ),
};

export const commentApi = {
  listByDoc: (docId: string, states?: string[]) => {
    const search = new URLSearchParams({ doc_id: docId });
    for (const state of states ?? []) {
      search.append("state", state);
    }
    return apiGet<CommentDTO[]>(`/api/v1/comments?${search.toString()}`);
  },
  listByNode: (nodeId: string) =>
    apiGet<CommentDTO[]>(`/api/v1/comments?node_id=${nodeId}`),
  create: (nodeId: string, body: string, expectedVersion?: number | null) =>
    apiPost<CommentDTO>("/api/v1/comments", {
      nodeId,
      body,
      expectedVersion: expectedVersion ?? null,
    }),
  setState: (commentId: string, state: string, expectedVersion: number) =>
    apiPatch<CommentDTO>(`/api/v1/comments/${commentId}`, { state, expectedVersion }),
};

// ── admin ───────────────────────────────────────────────────────────────

export const adminApi = {
  metrics: (windowSeconds?: number) =>
    apiGet<MetricsSnapshotDTO>(
      `/api/v1/admin/metrics${windowSeconds ? `?window=${windowSeconds}` : ""}`,
    ),
  health: () => apiGet<HealthReportDTO>("/api/v1/admin/health"),
};

export const userApi = {
  list: () => apiGet<UserDTO[]>("/api/v1/users"),
  create: (username: string, role: string) =>
    apiPost<UserDTO>("/api/v1/users", { username, role }),
  patch: (userId: string, payload: { role?: string; status?: string }) =>
    apiPatch<UserDTO>(`/api/v1/users/${userId}`, payload),
  remove: (userId: string) => apiDelete(`/api/v1/users/${userId}`),
  addKey: (userId: string, publicKey: string) =>
    apiPost<SshKeyDTO>(`/api/v1/users/${userId}/keys`, { publicKey }),
  revokeKey: (userId: string, keyId: string) =>
    apiDelete(`/api/v1/users/${userId}/keys`, { keyId }),
  roles: () => apiGet<RoleInfoDTO[]>("/api/v1/roles"),
  grants: (userId?: string) =>
    apiGet<GrantDTO[]>(`/api/v1/grants${userId ? `?user_id=${userId}` : ""}`),
  createGrant: (payload: { userId: string; scope: string; value: string; permission: string }) =>
    apiPost<GrantDTO>("/api/v1/grants", payload),
  deleteGrant: (grantId: string) => apiDelete(`/api/v1/grants/${grantId}`),
};
