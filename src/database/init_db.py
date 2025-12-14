import asyncio
from src.database.db import get_pool

async def create_tables():
    """Создание таблиц 'videos' и 'video_snapshots' в базе данных."""
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS videos (
                id UUID PRIMARY KEY,
                creator_id VARCHAR(255),
                video_created_at TIMESTAMPTZ,
                views_count INTEGER,
                likes_count INTEGER,
                comments_count INTEGER,
                reports_count INTEGER,
                created_at TIMESTAMPTZ,
                updated_at TIMESTAMPTZ
            );
        """)
        print("Таблица 'videos' успешно создана (или уже существует).")

        await conn.execute("""
            CREATE TABLE IF NOT EXISTS video_snapshots (
                id UUID PRIMARY KEY,
                video_id UUID REFERENCES videos(id) ON DELETE CASCADE,
                views_count INTEGER,
                likes_count INTEGER,
                comments_count INTEGER,
                reports_count INTEGER,
                delta_views_count INTEGER,
                delta_likes_count INTEGER,
                delta_comments_count INTEGER,
                delta_reports_count INTEGER,
                created_at TIMESTAMPTZ,
                updated_at TIMESTAMPTZ
            );
        """)
        print("Таблица 'video_snapshots' успешно создана (или уже существует).")
    await pool.close()

if __name__ == "__main__":
    print("Инициализация базы данных...")
    asyncio.run(create_tables())
    print("Инициализация завершена.")
