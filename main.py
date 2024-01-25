"""
Main bot code
"""
import logging
from aiogram import Bot
import asyncio
from DBPackage.DBclass import DBMethods

from main_modes.start_cmd import start_router
from main_modes.start_cmd import start_cmd

from main_modes.education_cmd import education_cmd_router
from main_modes.education_cmd import education_cmd

from main_modes.collections_cmd import collections_cmd_router
from main_modes.collections_cmd import collections_cmd

from bot_handlers.education_handlers1.education_paginator_handlers import (paginator_card_show,
                                                                           paginator_card_not_learned,
                                                                           paginator_card_learned, learning_exit)

from bot_handlers.collections_review_handlers2.collection_review_router import collections_review_router
from bot_handlers.collections_review_handlers2.add_collection_callback import add_new_collection_cmd
from bot_handlers.collections_review_handlers2.cancel_callback import collections_menu_cancel
from bot_handlers.collections_review_handlers2.edit_collection_callback_handler import edit_collection_callback
from bot_handlers.collections_review_handlers2.next_callback_handler import next_collection_callback
from bot_handlers.collections_review_handlers2.previous_callback_handler import previous_collection_callback

from bot_handlers.collection_add_handlers21.collection_add_router import collection_add_router
from bot_handlers.collection_add_handlers21.cancel_cmd_handler import collection_add_cmd_handler
from bot_handlers.collection_add_handlers21.get_collection_name_handler_handler1 import get_collection_name_handler, get_collection_name_error_handler
from bot_handlers.collection_add_handlers21.collection_active_mode_callback_handler2 import collection_activate_callback
from bot_handlers.collection_add_handlers21.collection_filling_callback_handler3 import collection_filling_callback, collection_not_filling_callback

from bot_handlers.collection_edit_handlers22.collection_edit_router import collection_edit_router
from bot_handlers.collection_edit_handlers22.add_pair_callback_handler import add_new_paar_callback
from bot_handlers.collection_edit_handlers22.change_collection_status_callback_handler import collection_activate_callback, collection_deactivate_callback
from bot_handlers.collection_edit_handlers22.delete_pair_callback_handler import pair_delete_callback
from bot_handlers.collection_edit_handlers22.edit_pair_callback_handler import edit_pair_callback
from bot_handlers.collection_edit_handlers22.flip_pair_callback_handler import flip_pair_callback
from bot_handlers.collection_edit_handlers22.next_pair_callback_handler import next_pair_callback
from bot_handlers.collection_edit_handlers22.previous_pair_callback_handler import previous_pair_callback

from bot_handlers.pair_add_handlers221.pair_add_router import pair_add_router
from bot_handlers.pair_add_handlers221.first_elem_get_handler1 import get_first_elem
from bot_handlers.pair_add_handlers221.second_elem_get_handler2 import get_second_elem
from bot_handlers.pair_add_handlers221.mirror_regim_callback3 import set_mirror_mode, set_no_mirror_mode

from bot_handlers.pair_edit_handlers222.edit_pair_router import edit_pair_router
from bot_handlers.pair_edit_handlers222.cancel_cmd import cancel_pair_editing
from bot_handlers.pair_edit_handlers222.first_elem_edit_handler1 import get_first_elem, first_elem_leave_unchanged
from bot_handlers.pair_edit_handlers222.second_elem_edit_handler2 import get_second_elem, second_elem_leave_unchanged


from bot_set.dispatcher_object import card_flipper_dp
from bot_set.bot_object import card_flipper_bot


async def on_startup(bot: Bot) -> None:
    # Create DB\Tables if not
    print("\nВыполняется код непосредственно перед поллингом бота")
    DBMethods.create_tables()
    print("БД создана")
    print("Bot is ready")


async def main() -> None:
    #зарегистрировать он стартап
    card_flipper_dp.startup.register(on_startup)
    #зарегистрировать мидлвари

    #привзать роутеры в диспетчер
    card_flipper_dp.include_routers(start_router, education_cmd_router, collections_cmd_router,
                                    collections_review_router, collection_add_router, collection_edit_router,
                                    pair_add_router, edit_pair_router)

    async with card_flipper_bot.context():
        # сбрсоить обновления бота
        await card_flipper_bot.delete_webhook(drop_pending_updates=True)

        try:
            #поллинг
            await card_flipper_dp.start_polling(card_flipper_bot)
        except Exception as error_obj:
            print("При поллинге бота возникла ошибка,", error_obj)
        finally:
            pass


if __name__ == "__main__":
    asyncio.run(main())


