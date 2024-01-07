#TODO:
# Состояние бота меняется на teaching
# запускается сценарий education_handlers
# Формируется список пар для обучения (метод класса работы с БД):
# Цикл проходит по списку активных коллекций и подключается к БД каждой коллекции,
# где собирает все пары в один словарь в рандом порядке.
# Идя по словарю бот последовательно отправляет пользователю сообщения:
# Объект: Элемент 1, кнопки инлайн клавиатуры: Знаю, развернуть, не знаю
# Когда словарь пуст, пользователь получает приветственное сообщение и напоминание о повторении. Выводится главное меню.

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.filters import StateFilter

from bot_set.bot_states import BotStates

education_cmd_router = Router()


@education_cmd_router.message(F.text.lower() == "Учиться 🧑‍🏫")
async def education_cmd(message: Message, state: FSMContext) -> None:
    await state.set_state(BotStates.teaching)
    # TODO: вернуть пагинацией список карточек к изучению
    pass
