#TODO: Принимается первый элмент или остается без изменений.
# Пользователь получает сообщение: “Второй элемент пары: …,
# пришлите на что его изменить или нажмите кнопку “Оставить без изменений”.

from .edit_paar_router import edit_paar_router

from aiogram import F


@edit_paar_router.message()
async def get_first_elem():
    pass


@edit_paar_router.message(F.text("Оставить без изменений"))
async def first_elem_leave_unchanged():
    pass
