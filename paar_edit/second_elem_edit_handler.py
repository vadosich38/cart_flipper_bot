from .edit_paar_router import edit_paar_router

from aiogram import F


@edit_paar_router.message()
async def get_second_elem():
    pass


@edit_paar_router.message(F.text("Оставить без изменений"))
async def second_elem_leave_unchanged():
    pass
