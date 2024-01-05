#TODO: После выбора режима “Коллекции” Состояние бота меняется FSM: collections,
# запускается сценарий collections_review_handlers
# в пользователь получает кнопку
# “Добавить новую коллекцию” и “Вернуться в главное меню” и сообщение с списком коллекций, реализованный пагинацией
# с прикрепленной инлайн клавиатурой с кнопками: <<Предыдущая, Редактировать, Следующая>>

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

collections_cmd_router = Router()


@collections_cmd_router.message(Command("Открыть мои коллекции"))
async def collections_cmd(message: Message) -> None:
    pass
