# хендлер принимает имя коллекции и записывает его
# Пользователь получает сообщение: Имя вашей коллекции…, хотите активировать ее?

from aiogram import F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from .collection_add_router import collection_add_router
from bot_set.bot_states import BotStates
from bot_set.texts import bot_texts
from keyboards.yes_no_ikb import get_yes_no_ikb
from DBPackage.DBclass import DBMethods


@collection_add_router.message(F.text, F.text.len() < 25, StateFilter(BotStates.collection_adding_get_name))
async def get_collection_name_handler(message: Message, state: FSMContext):
    DBMethods.add_collection_by_telegram_id(telegram_id=message.from_user.id, collection_name=message.text)

    await message.reply(text=f"Имя вашей коллекции {message.text}\n\n"
                             f"хотите ее активировать? ☑️",
                        reply_markup=get_yes_no_ikb())
    await state.set_data({"new_coll_name": message.text})
    await state.set_state(BotStates.collection_adding_get_active_mode)


@collection_add_router.message(F.text, F.text.len() > 25, StateFilter(BotStates.collection_adding_get_name))
async def get_collection_name_error_handler(message: Message):
    await message.reply(text=bot_texts["collection_name_to_long"])
