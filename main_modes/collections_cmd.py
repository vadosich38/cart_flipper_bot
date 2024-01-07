#TODO: После выбора режима “Коллекции” Состояние бота меняется FSM: collections,
# запускается сценарий collections_review_handlers
# в пользователь получает кнопку
# “Добавить новую коллекцию” и “Вернуться в главное меню” и сообщение с списком коллекций, реализованный пагинацией
# с прикрепленной инлайн клавиатурой с кнопками: <<Предыдущая, Редактировать, Следующая>>

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot_set.bot_states import BotStates
from keyboards.back_to_main_menu import get_return_in_main_menu_kb

collections_cmd_router = Router()


@collections_cmd_router.message(Command("Коллекции 📜"))
async def collections_cmd(message: Message, state: FSMContext) -> None:
    await state.set_state(BotStates.collections_review)
    # TODO: вернуть пагинацией список коллеккций
    await message.answer(text="",
                         reply_markup=get_return_in_main_menu_kb())
    pass
