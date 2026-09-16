#!/usr/bin/env bash
# AgenticDocer 部署脚本（幂等，可重复执行）
#
# 前置：bash scripts/provision_pg.sh 已跑过（角色与库就绪）
# 用法：bash scripts/deploy.sh [--host HOST] [--port PORT]
set -euo pipefail

REPO="/home/lxx/wrk/AgenticDocer"
UNIT_NAME="agenticdocer-api"
UNIT_DIR="$HOME/.config/systemd/user"

# 本机 all_proxy=socks5 会破坏 PG/HTTP 连接（TLS handshake 失败）
unset all_proxy ALL_PROXY http_proxy https_proxy ftp_proxy 2>/dev/null || true

HOST="127.0.0.1"; PORT="8787"
while [ $# -gt 0 ]; do
  case "$1" in
    --host) HOST="$2"; shift 2 ;;
    --port) PORT="$2"; shift 2 ;;
    *) echo "未知参数：$1"; exit 2 ;;
  esac
done

echo "[1/5] 环境检查"
[ -f "$REPO/.env" ] || { echo "缺少 $REPO/.env（可从 .env.example 复制）"; exit 1; }
[ -d "$REPO/.venv" ] || { echo "缺少 .venv（先跑 uv sync）"; exit 1; }

echo "[2/5] 数据库迁移（alembic upgrade head）"
cd "$REPO"
.venv/bin/python -m alembic upgrade head

echo "[3/5] 前端构建产物检查"
if [ -f "$REPO/webui/dist/index.html" ]; then
  echo "  webui/dist 存在（FastAPI 会静态挂载到 /）"
else
  echo "  ⚠ webui/dist 不存在 —— WebUI 不可用；如需请：cd webui && npm install && npm run build"
fi

echo "[4/5] 安装 systemd user 服务"
mkdir -p "$UNIT_DIR"
cp "$REPO/scripts/$UNIT_NAME.service" "$UNIT_DIR/"
systemctl --user daemon-reload

echo "[5/5] 启动并启用自启"
systemctl --user enable --now "$UNIT_NAME"
sleep 3

echo
echo "状态："
systemctl --user is-active "$UNIT_NAME" | sed 's/^/  active: /'
systemctl --user is-enabled "$UNIT_NAME" | sed 's/^/  enabled: /'
echo
echo "验证："
if command -v curl >/dev/null; then
  code=$(curl -s -o /dev/null -w "%{http_code}" "http://$HOST:$PORT/healthz" || echo "000")
  echo "  GET http://$HOST:$PORT/healthz → $code"
  [ "$code" = "200" ] || echo "  ⚠ healthz 非 200，请查：journalctl --user -u $UNIT_NAME -n 50"
fi
echo
echo "首次部署提醒（ADR-007 S9）："
echo "  1. 放置管理员公钥：cp ~/.ssh/id_ed25519.pub $REPO/data/admin_keys/admin.pub"
echo "  2. 重启服务触发自举：systemctl --user restart $UNIT_NAME"
echo "  3. 验证身份：cd $REPO && uv run agenticdocer auth whoami"
echo
echo "对外暴露（ADR-007 S6，二者缺一不可）："
echo "  ① 已自举 admin（无 users 行则 fail-closed）"
echo "  ② 经 TLS 反向代理终止（否则会话 Cookie 可被嗅探）"
echo "  改 --host 0.0.0.0 见 scripts/$UNIT_NAME.service 注释"
echo "完成。"
