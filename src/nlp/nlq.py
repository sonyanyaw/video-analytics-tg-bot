import requests
import logging
from src.core.config import YANDEX_GPT_API, CATALOG_ID


# Загрузка промпта один раз при инициализации модуля
try:
    with open("src/prompts/prompt.md", "r", encoding="utf-8") as f:
        PROMPT = f.read()
except FileNotFoundError:
    print("Файл с промптом не найден: src/prompts/prompt.md")
    PROMPT = ""

url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Api-Key {YANDEX_GPT_API}",
}

def parse_nlq_to_sql(text: str) -> str:
    if not PROMPT:
        print("Промпт не загружен. Невозможно выполнить запрос.")
        raise ValueError("Промпт отсутствует.")

    try:
        response = requests.post(
            url,
            headers=headers,
            json={
                "modelUri": f"gpt://{CATALOG_ID}/yandexgpt-lite",
                "completionOptions": {
                    "stream": False,
                    "temperature": 0.6,
                    "maxTokens": "2000",
                },
                "messages": [
                    {"role": "system", "text": PROMPT},
                    {"role": "user", "text": text},
                ],
            },
        )
        response.raise_for_status()
        result_json = response.json()

        # Извлекаем текст из ответа
        sql_query = result_json["result"]["alternatives"][0]["message"]["text"]
        sql_query = sql_query.replace("```", "").strip()
        print(f"Сгенерированный SQL-запрос: {sql_query}")
        return sql_query

    except requests.RequestException as e:
        print(f"Ошибка при выполнении запроса к API: {e}")
        raise
    except (KeyError, IndexError) as e:
        print(f"Ошибка при разборе ответа от YandexGPT: {e}")
        print(f"Полный ответ: {response.text}")
        raise ValueError("Не удалось извлечь SQL-запрос из ответа API.")