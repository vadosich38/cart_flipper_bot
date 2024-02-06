from .collection_edit_router import collection_edit_router
from bot_set.bot_states import BotStates
from bot_set.bot_object import card_flipper_bot
from bot_set.texts import bot_texts
from keyboards.main_menu_kb import get_main_kb

from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import F


@collection_edit_router.callback_query(F.data == "back_to_collections", StateFilter(BotStates.collection_editing))
async def back_to_main_menu_callback(callback_data: CallbackQuery, state: FSMContext) -> None:
    await callback_data.answer("Вернуться в главное меню ✅")
    await card_flipper_bot.delete_message(chat_id=callback_data.from_user.id,
                                          message_id=callback_data.message.message_id)
    await state.set_state(BotStates.main_menu)
    await card_flipper_bot.send_message(chat_id=callback_data.from_user.id,
                                        text=bot_texts["return_in_main_menu"],
                                        reply_markup=get_main_kb())

