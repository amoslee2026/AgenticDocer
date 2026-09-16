"""M08 联调用：把本地开发机公钥登记到既有 admin 用户（走 add_ssh_key 同一代码路径）。

bootstrap 在已有 active admin 时幂等返回、不登记新钥（S9），故本机联调需此一次性登记。
用法：DATABASE_URL=... uv run python scripts-dev/m08_register_key.py
"""

import asyncio
import sys
from pathlib import Path

from agenticdocer.auth.users import add_ssh_key, find_user_by_username
from agenticdocer.store import get_database

PUBKEY = Path.home() / ".ssh" / "id_ed25519.pub"
USERNAME = "admin"


async def main() -> int:
    line = PUBKEY.read_text("utf-8").strip()
    db = get_database()
    user = await find_user_by_username(USERNAME, db=db)
    if user is None:
        print(f"user {USERNAME!r} not found", file=sys.stderr)
        return 1
    key = await add_ssh_key(user.user_id, line, actor="m08-webui-integration", db=db)
    print(f"registered {key.key_id} -> {USERNAME}")
    await db.dispose()
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
