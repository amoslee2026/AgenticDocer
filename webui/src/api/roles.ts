// 角色基线排序（ADR-007 §5）：admin ⊃ editor ⊃ reviewer ⊃ reader。
// 与后端 role_permits 的「角色硬上限」口径一致，用于前端决定是否渲染入口/编辑器。
import type { RoleName } from "./types";

export const ROLE_RANK: Record<RoleName, number> = {
  reader: 0,
  reviewer: 1,
  editor: 2,
  admin: 3,
};

export function roleAtLeast(role: RoleName, min: RoleName): boolean {
  return ROLE_RANK[role] >= ROLE_RANK[min];
}
