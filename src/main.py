from aiogram import Bot, Dispatcher
from core.config import TELEGRAM_BOT_TOKEN

def main():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()
    dp.run_polling(bot)

if __name__ == "__main__":
    main()
