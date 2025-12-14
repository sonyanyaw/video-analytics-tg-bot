from src.database.db import get_pool
import asyncio

async def run_sql_fetchone(sql: str):
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(sql)
        return row[0] if row and len(row) > 0 else 0


def run_sql_sync(sql: str):
    return asyncio.get_event_loop().run_until_complete(run_sql_fetchone(sql))
