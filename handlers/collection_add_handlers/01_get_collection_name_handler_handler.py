#TODO: хендлер принимает имя коллекции и записывает его
# Пользователь получает сообщение: Имя вашей коллекции…, хотите активировать ее?

from aiogram import F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from .collection_add_router import collection_add_router
from bot_set.bot_states import BotStates
from bot_set.texts import bot_texts
from keyboards.yes_no_ikb import get_yes_no_ikb


@collection_add_router.message(F.text, len(F.text) < 25, StateFilter(BotStates.collection_adding_get_name))
async def get_collection_name_handler(message: Message, state: FSMContext):
    await state.update_data(new_coll_name=message.text)
    new_collection_data = await state.get_data()

    await message.reply(text=f"Имя вашей коллекции {new_collection_data['new_coll_name']}\n\n"
                             f"хотите ее активировать? ☑️",
                        reply_markup=get_yes_no_ikb())
    await state.set_state(BotStates.collection_adding_get_active_mode)


@collection_add_router.message(F.text, len(F.text) > 25, StateFilter(BotStates.collection_adding_get_name))
async def get_collection_name_error_handler(message: Message):
    await message.reply(text=bot_texts["collection_name_to_long"])
