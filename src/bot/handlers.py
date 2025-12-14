from aiogram import Router, types
from src.nlp.nlq import parse_nlq_to_sql
from src.database.sql_exec import run_sql_fetchone

router = Router()

@router.message()
async def handle_message(msg: types.Message):
    text = msg.text.strip()
    try:
        sql = parse_nlq_to_sql(text)
    except Exception as e:
        await msg.answer("Не смог распознать запрос: " + str(e))
        return
    try:
        result = await run_sql_fetchone(sql)
        await msg.answer(str(result))
    except Exception as e:
        await msg.answer("Ошибка при выполнении запроса: " + str(e))
