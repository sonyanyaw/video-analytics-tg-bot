from aiogram import Bot, Dispatcher
from src.core.config import TELEGRAM_BOT_TOKEN
from src.bot.handlers import router

def main():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    dp.run_polling(bot)

if __name__ == "__main__":
    main()
