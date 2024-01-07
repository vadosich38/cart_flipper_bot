#TODO: Кнопка “Активировать/деактивировать коллекцию” изменяет статус активности выбранной коллекции.

from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from .collection_edit_router import collection_edit_router
from bot_set.texts import bot_texts
from keyboards.main_menu_kb import get_main_kb
from bot_set.bot_states import BotStates


@collection_edit_router.message(F.text.lower() == "активировать коллекцию 🟩",
                                StateFilter(BotStates.collection_editing))
async def collection_activate_handler(message: Message, state: FSMContext) -> None:
    #TODO: сменить статус коллекции
    await message.answer(text="Коллекция активирована 🟩")
    await message.answer(text=bot_texts["return_in_main_menu"],
                         reply_markup=get_main_kb())
    await state.clear()


@collection_edit_router.message(F.text.lower() == "деактивировать коллекцию 🟥",
                                StateFilter(BotStates.collection_editing))
async def collection_deactivate_handler(message: Message, state: FSMContext) -> None:
    #TODO: сменить статус коллекции
    await message.answer(text="Коллекция деактивирована 🟥")
    await message.answer(text=bot_texts["return_in_main_menu"],
                         reply_markup=get_main_kb())
    await state.clear()
