// API 客户端：同源 fetch + 会话 Cookie；错误统一解包（store 错误为平铺，
// 鉴权错误嵌在 detail 下——两种形状都兼容）。
import type { ViolationDTO } from "./types";

export class ApiError extends Error {
  status: number;
  code: string | null;
  violations: ViolationDTO[];

  constructor(status: number, message: string, code: string | null, violations: ViolationDTO[]) {
    super(message);
    this.status = status;
    this.code = code;
    this.violations = violations;
  }
}

interface RawErrorShape {
  error?: string;
  message?: string;
  code?: string;
  violations?: ViolationDTO[];
  detail?: { error?: string; reason?: string; message?: string };
}

async function parseError(response: Response): Promise<ApiError> {
  let raw: RawErrorShape = {};
  try {
    raw = (await response.json()) as RawErrorShape;
  } catch {
    // 非 JSON 错误体（如网关截断）
  }
  const message =
    raw.message ?? raw.detail?.message ?? `请求失败（HTTP ${response.status}）`;
  const code = raw.error ?? raw.detail?.error ?? raw.code ?? null;
  return new ApiError(
    response.status,
    code === "DTO_AUTH_REJECTED" ? `${message}（${raw.detail?.reason ?? ""}）` : message,
    code,
    raw.violations ?? [],
  );
}

export async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    ...init,
    headers: {
      ...(init?.body !== undefined ? { "Content-Type": "application/json" } : {}),
      ...init?.headers,
    },
  });
  if (!response.ok) {
    throw await parseError(response);
  }
  if (response.status === 204) {
    return undefined as T;
  }
  return (await response.json()) as T;
}

export function apiGet<T>(path: string): Promise<T> {
  return api<T>(path);
}

export function apiPost<T>(path: string, body?: unknown): Promise<T> {
  return api<T>(path, { method: "POST", body: body === undefined ? undefined : JSON.stringify(body) });
}

export function apiPatch<T>(path: string, body: unknown): Promise<T> {
  return api<T>(path, { method: "PATCH", body: JSON.stringify(body) });
}

export function apiDelete(path: string, body?: unknown): Promise<void> {
  return api<void>(path, {
    method: "DELETE",
    body: body === undefined ? undefined : JSON.stringify(body),
  });
}

/** 渲染产物里的资产相对路径 `assets/<sha>.<ext>` → API 资产端点（asset_id 为裸 sha256）。 */
export function toAssetUrl(src: string): string {
  const match = /^assets\/([0-9a-f]{64})(\.[^)]+)?$/i.exec(src.trim());
  if (match) {
    return `/api/v1/assets/${match[1]}`;
  }
  return src;
}
