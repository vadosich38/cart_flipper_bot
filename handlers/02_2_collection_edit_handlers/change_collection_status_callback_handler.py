# Кнопка “Активировать/деактивировать коллекцию” изменяет статус активности выбранной коллекции.

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
import asyncio

from .collection_edit_router import collection_edit_router
from bot_set.texts import bot_texts
from keyboards.main_menu_kb import get_main_kb
from bot_set.bot_states import BotStates
from DBPackage.DBclass import DBMethods
from bot_set.bot_object import cart_flipper_bot


@collection_edit_router.callback_query(F.data == "activate", StateFilter(BotStates.collection_editing))
async def collection_activate_callback(callback_data: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    collection_id = data["cur_coll_id"]

    DBMethods.set_collection_active_by_collection_id(collection_id=collection_id)
    await callback_data.answer(text="Коллекция активирована 🟩")
    await asyncio.sleep(1)
    await cart_flipper_bot.send_message(chat_id=callback_data.from_user.id,
                                        text=bot_texts["return_in_main_menu"],
                                        reply_markup=get_main_kb())
    await state.clear()
    await state.set_state(BotStates.main_menu)


@collection_edit_router.message(F.data == "deactivate", StateFilter(BotStates.collection_editing))
async def collection_deactivate_callback(callback_data: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    collection_id = data["cur_coll_id"]

    DBMethods.set_collection_inactive_by_collection_id(collection_id=collection_id)
    await callback_data.answer(text="Коллекция деактивирована 🟥")

    await cart_flipper_bot.send_message(chat_id=callback_data.from_user.id,
                                        text=bot_texts["return_in_main_menu"],
                                        reply_markup=get_main_kb())
    await state.clear()
    await state.set_state(BotStates.main_menu)

