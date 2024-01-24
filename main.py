"""
Main bot code
"""
import logging
from aiogram import Bot
import asyncio

from main_modes.start_cmd import start_router
from main_modes.education_cmd import education_cmd_router
from main_modes.collections_cmd import collections_cmd_router

from bot_set.dispatcher_object import cart_flipper_dp
from bot_set.bot_object import card_flipper_bot


async def on_startup(bot: Bot) -> None:
    print("Выполняется код непосредственно перед поллингом бота")


async def main() -> None:
    #зарегистрировать он стартап
    await cart_flipper_dp.startup.register(on_startup)
    #зарегистрировать мидлвари

    #привзать роутеры в диспетчер
    await cart_flipper_dp.include_routers(start_router, education_cmd_router, collections_cmd_router)

    async with card_flipper_bot.context():
        # сбрсоить обновления бота
        await card_flipper_bot.delete_webhook(drop_pending_updates=True)

        try:
            #поллинг
            await cart_flipper_dp.start_polling(bots=card_flipper_bot)
        except Exception as error_obj:
            print("При поллинге бота возникла ошибка,", error_obj)
        finally:
            pass


if __name__ == "__main__":
    asyncio.run(main())


