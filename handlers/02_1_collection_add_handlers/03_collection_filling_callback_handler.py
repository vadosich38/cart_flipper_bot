#TODO: Да –– меняет состояние бота  FSM: pair_adding и вызывает сценарий 02_02_01_pair_add_handlers
# Нет –– меняет состояние бота FSM: collection и возвращает к списку коллекций.

from aiogram.types import CallbackQuery
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from .collection_add_router import collection_add_router
from bot_set.bot_states import BotStates
from bot_set.texts import bot_texts
from keyboards.main_menu_kb import get_main_kb
from bot_set.bot_object import card_flipper_bot


@collection_add_router.callback_query(F.data == "yes", StateFilter(BotStates.collection_adding_get_fill_decision))
async def collection_filling_callback(callback_data: CallbackQuery, state: FSMContext):
    await state.set_state(BotStates.get_first_elem_new_pair_adding)
    await callback_data.answer(text="Добавить карточки в коллекцию 🟩")
    await card_flipper_bot.send_message(chat_id=callback_data.from_user.id,
                                        text="Пришлите первый элемент карточки 📂")
    #TODO: переход к сценарию pair_add


@collection_add_router.callback_query(F.data == "no", StateFilter(BotStates.collection_adding_get_fill_decision))
async def collection_not_filling_callback(callback_data: CallbackQuery, state: FSMContext):
    await callback_data.answer(text="Оставить коллекцию пустой 🟥")
    await card_flipper_bot.send_message(chat_id=callback_data.from_user.id,
                                        text="Новая коллекция останется пустая. Если вы хахотите ее наполнить, "
                                             "перейдите к редактированию коллекции 👁‍🗨")

    await state.set_state(BotStates.main_menu)
    await card_flipper_bot.send_message(chat_id=callback_data.from_user.id,
                                        text=bot_texts["return_in_main_menu"],
                                        reply_markup=get_main_kb())
