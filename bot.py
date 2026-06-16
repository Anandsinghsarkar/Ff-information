import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher

from config import BOT_TOKEN

# Routers
from handlers.user import router as user_router
from handlers.admin import router as admin_router


# ==========================
# LOGGING
# ==========================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ==========================
# BOT STARTUP
# ==========================

async def main():

    bot = Bot(
        token=BOT_TOKEN
    )

    dp = Dispatcher()

    # Routers
    dp.include_router(
        user_router
    )

    dp.include_router(
        admin_router
    )

    logging.info(
        "FF INFO BOT STARTED"
    )

    await bot.delete_webhook(
        drop_pending_updates=True
    )

    await dp.start_polling(
        bot
    )


# ==========================
# RUN
# ==========================

if __name__ == "__main__":

    try:
        asyncio.run(
            main()
        )

    except KeyboardInterrupt:
        print(
            "Bot Stopped"
        )