#TODO: Принимается второй элмент или остается без изменений.
# Изменения записываются с указанием формата данных: изображение, текст, видео, аудио.
# Пользователь получает сообщение об успешном редактировании пары и возвращается к списку пар коллекции,
# меняет состояние бота FSM: collection_editing.
from .edit_paar_router import edit_paar_router

from aiogram import F


@edit_paar_router.message()
async def get_second_elem():
    pass


@edit_paar_router.message(F.text("Оставить без изменений"))
async def second_elem_leave_unchanged():
    pass
