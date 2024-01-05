from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

start_router = Router()


@start_router.message(CommandStart)
async def start_cmd(message: Message) -> None:
    pass
