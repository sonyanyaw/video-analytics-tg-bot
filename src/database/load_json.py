import os
import asyncio
import json
import uuid
from datetime import datetime
from dateutil import parser
from src.database.db import get_pool


def ensure_uuid(val) -> uuid.UUID:
    return val if isinstance(val, uuid.UUID) else uuid.UUID(val)


def parse_dt(s: str) -> datetime:
    if isinstance(s, datetime):
        return s
    return parser.isoparse(s) 


async def load_videos_from_json(json_path: str):
    if not os.path.exists(json_path):
        print(f"Файл {json_path} не найден.")
        return

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Ошибка чтения JSON: {e}")
        return

    videos = data.get("videos", [])
    if not videos:
        print("Нет видео в JSON.")
        return

    pool = await get_pool()
    try:
        async with pool.acquire() as conn:
            video_records = []
            for v in videos:
                try:
                    video_records.append((
                        ensure_uuid(v["id"]),
                        v["creator_id"],
                        parse_dt(v["video_created_at"]),   
                        v.get("views_count", 0),
                        v.get("likes_count", 0),
                        v.get("comments_count", 0),
                        v.get("reports_count", 0),
                        parse_dt(v["created_at"]),       
                        parse_dt(v["updated_at"]),       
                    ))
                except KeyError as e:
                    print(f"Отсутствует ключ в видео: {e}")
                    continue

            await conn.executemany("""
                INSERT INTO videos (
                    id, creator_id, video_created_at,
                    views_count, likes_count, comments_count, reports_count,
                    created_at, updated_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                ON CONFLICT (id) DO UPDATE SET
                    views_count = EXCLUDED.views_count,
                    likes_count = EXCLUDED.likes_count,
                    comments_count = EXCLUDED.comments_count,
                    reports_count = EXCLUDED.reports_count,
                    updated_at = EXCLUDED.updated_at
            """, video_records)

            print(f"Вставлено {len(video_records)} видео.")

            snapshot_records = []
            for v in videos:
                for s in v.get("snapshots", []):
                    try:
                        snapshot_records.append((
                            ensure_uuid(s["id"]),
                            ensure_uuid(s["video_id"]),
                            s.get("views_count", 0),
                            s.get("likes_count", 0),
                            s.get("comments_count", 0),
                            s.get("reports_count", 0),
                            s.get("delta_views_count", 0),
                            s.get("delta_likes_count", 0),
                            s.get("delta_comments_count", 0),
                            s.get("delta_reports_count", 0),
                            parse_dt(s["created_at"]),   
                            parse_dt(s["updated_at"]),    
                        ))
                    except KeyError as e:
                        print(f"Отсутствует ключ в снапшоте: {e}")
                        continue

            if snapshot_records:
                await conn.executemany("""
                    INSERT INTO video_snapshots (
                        id, video_id,
                        views_count, likes_count, comments_count, reports_count,
                        delta_views_count, delta_likes_count, delta_comments_count, delta_reports_count,
                        created_at, updated_at
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
                    ON CONFLICT (id) DO UPDATE SET
                        views_count = EXCLUDED.views_count,
                        likes_count = EXCLUDED.likes_count,
                        reports_count = EXCLUDED.reports_count,
                        comments_count = EXCLUDED.comments_count,
                        delta_views_count = EXCLUDED.delta_views_count,
                        delta_likes_count = EXCLUDED.delta_likes_count,
                        delta_reports_count = EXCLUDED.delta_reports_count,
                        delta_comments_count = EXCLUDED.delta_comments_count,
                        updated_at = EXCLUDED.updated_at
                """, snapshot_records)
                print(f"Вставлено {len(snapshot_records)} снапшотов.")
            else:
                print("Снапшотов не найдено.")

    except Exception as e:
        print(f"Ошибка работы с базой данных: {e}")
    finally:
        await pool.close()


if __name__ == "__main__":
    asyncio.run(load_videos_from_json("src/data/videos.json"))