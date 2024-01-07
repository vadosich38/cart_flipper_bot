#TODO: да - активировать коллекцию, нет - не активировать коллекцию
# Пользователь получает сообщение: Коллекция активна/не активна. Хотите ее наполнить?

from aiogram.types import CallbackQuery
from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from .collection_add_router import collection_add_router
from bot_set.bot_states import BotStates
from bot_set.bot_object import cart_flipper_bot
from keyboards.yes_no_ikb import get_yes_no_ikb


@collection_add_router.callback_query(F.data == "yes", StateFilter(BotStates.collection_adding_get_active_mode))
async def collection_activate_callback(callback_data: CallbackQuery, state: FSMContext):
    await callback_data.answer(text="Коллекция активирована! 🟢")
    await cart_flipper_bot.send_message(chat_id=callback_data.from_user.id,
                                        text="Коллекция активна 🟩\n\n"
                                             "Хотите ее наполнить карточками? 📂",
                                        reply_markup=get_yes_no_ikb())
    await state.set_state(BotStates.collection_adding_get_fill_decision)


@collection_add_router.callback_query(F.data == "no", StateFilter(BotStates.collection_adding_get_active_mode))
async def collection_deactivate_callback(callback_data: CallbackQuery, state: FSMContext):
    await callback_data.answer(text="Коллекция не активна! 🔴")
    await cart_flipper_bot.send_message(chat_id=callback_data.from_user.id,
                                        text="Коллекция остается не активированной 🟥\n\n"
                                             "Хотите ее наполнить карточками? 📂",
                                        reply_markup=get_yes_no_ikb())
    await state.set_state(BotStates.collection_adding_get_fill_decision)

