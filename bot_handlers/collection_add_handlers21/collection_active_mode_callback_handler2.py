# да - активировать коллекцию, нет - не активировать коллекцию
# Пользователь получает сообщение: Коллекция активна/не активна. Хотите ее наполнить?

from aiogram.types import CallbackQuery
from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from .collection_add_router import collection_add_router
from bot_set.bot_states import BotStates
from bot_set.bot_object import card_flipper_bot
from keyboards.yes_no_ikb import get_yes_no_ikb
from DBPackage.DBclass import DBMethods


@collection_add_router.callback_query(F.data == "yes", StateFilter(BotStates.collection_adding_get_active_mode))
async def collection_activate_callback(callback_data: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    collection_id = DBMethods.get_collection_id_by_collection_name_and_telegram_id(
        collection_name=data["new_coll_name"],
        telegram_id=callback_data.from_user.id)
    await state.update_data({"new_coll_id": collection_id})

    DBMethods.set_collection_active_by_collection_id(collection_id=collection_id)
    await callback_data.answer(text="Коллекция активирована! 🟢")
    await card_flipper_bot.send_message(chat_id=callback_data.from_user.id,
                                        text="Коллекция активна 🟩\n\n"
                                             "Хотите ее наполнить карточками? 📂",
                                        reply_markup=get_yes_no_ikb())
    await state.set_state(BotStates.collection_adding_get_fill_decision)


@collection_add_router.callback_query(F.data == "no", StateFilter(BotStates.collection_adding_get_active_mode))
async def collection_deactivate_callback(callback_data: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    collection_id = DBMethods.get_collection_id_by_collection_name_and_telegram_id(
        collection_name=data["new_coll_name"],
        telegram_id=callback_data.from_user.id)
    await state.update_data({"new_coll_id": collection_id})

    DBMethods.set_collection_inactive_by_collection_id(collection_id=collection_id)

    await callback_data.answer(text="Коллекция не активна! 🔴")
    await card_flipper_bot.send_message(chat_id=callback_data.from_user.id,
                                        text="Коллекция остается не активированной 🟥\n\n"
                                             "Хотите ее наполнить карточками? 📂",
                                        reply_markup=get_yes_no_ikb())
    await state.set_state(BotStates.collection_adding_get_fill_decision)

