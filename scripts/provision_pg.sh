#!/usr/bin/env bash
# AgenticDocer 本地 PG 环境 provision（幂等，可重复执行）
#
# 背景：本机 PG 16.15 跑在 Podman 容器 pgvector/pgvector:pg16（:5432），
#       superuser 为 postgres（trust 认证）。本脚本创建 ADR-007 定义的两个角色与两个库。
#
# 用法：bash scripts/provision_pg.sh
set -euo pipefail

PGHOST="${PGHOST:-127.0.0.1}"
PGPORT="${PGPORT:-5432}"
SUPER_URL="postgresql://postgres@${PGHOST}:${PGPORT}/postgres"

OWNER_PW="${AGENTICDOCER_OWNER_PW:-agenticdocer_dev}"
APP_PW="${AGENTICDOCER_APP_PW:-agenticdocer_app_dev}"

# 本机 all_proxy=socks5 会破坏 PG 连接（TLS handshake 失败）
unset all_proxy ALL_PROXY http_proxy https_proxy ftp_proxy 2>/dev/null || true

echo "[1/3] 创建/更新角色（ADR-007 §4.1）"
psql "$SUPER_URL" -v ON_ERROR_STOP=1 -q <<SQL
DO \$\$ BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname='agenticdocer') THEN
    CREATE ROLE agenticdocer LOGIN;
  END IF;
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname='agenticdocer_app') THEN
    CREATE ROLE agenticdocer_app LOGIN;
  END IF;
END \$\$;
-- 密码必须单独 ALTER（DO 块内的 CREATE ROLE ... PASSWORD 在此 PG 上不生效）
ALTER ROLE agenticdocer     WITH LOGIN PASSWORD '${OWNER_PW}';
ALTER ROLE agenticdocer_app WITH LOGIN PASSWORD '${APP_PW}';
SQL

echo "[2/3] 创建数据库（主库 + 测试库）"
for db in agenticdocer agenticdocer_test; do
  exists=$(psql "$SUPER_URL" -tAc "SELECT 1 FROM pg_database WHERE datname='${db}'")
  if [ -z "$exists" ]; then
    psql "$SUPER_URL" -v ON_ERROR_STOP=1 -q -c "CREATE DATABASE ${db} OWNER agenticdocer"
    echo "  created ${db}"
  else
    echo "  ${db} exists"
  fi
  psql "$SUPER_URL" -v ON_ERROR_STOP=1 -q -c "GRANT CONNECT ON DATABASE ${db} TO agenticdocer_app"
done

echo "[3/3] 授权 schema public"
for db in agenticdocer agenticdocer_test; do
  psql "postgresql://postgres@${PGHOST}:${PGPORT}/${db}" -v ON_ERROR_STOP=1 -q \
    -c "GRANT ALL ON SCHEMA public TO agenticdocer; GRANT USAGE, CREATE ON SCHEMA public TO agenticdocer_app;"
done

echo
echo "验证："
PGPASSWORD="$APP_PW" psql "postgresql://agenticdocer_app@${PGHOST}:${PGPORT}/agenticdocer" \
  -tAc "SELECT 'app role OK: ' || current_user || '@' || current_database()"
PGPASSWORD="$OWNER_PW" psql "postgresql://agenticdocer@${PGHOST}:${PGPORT}/agenticdocer" \
  -tAc "SELECT 'owner role OK: ' || current_user || '@' || current_database()"
echo "完成。"
