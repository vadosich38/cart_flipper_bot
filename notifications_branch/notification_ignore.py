from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import F

from bot_set.texts import bot_texts
from keyboards.main_menu_kb import get_main_kb
from bot_set.bot_states import BotStates
from main_modes.start_cmd import start_router


@start_router.message(F.text.lower() == "пропустить 🤖")
async def ignore_notification_cmd(message: Message, state: FSMContext) -> None:
    await message.delete()
    await state.set_state(BotStates.main_menu)
    await message.answer(text="Сегодня вы пропустили урок и выбились из режима обучения 🫣\n"
                              "Помните, что в обучении главное регулярность и дисциплина 💪",
                         reply_markup=get_main_kb())
