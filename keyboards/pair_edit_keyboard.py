from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_pair_edit_kb() -> InlineKeyboardMarkup:
    edit_ikb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Оставить элемент без изменений ☑️", callback_data="no_changes")],
            [InlineKeyboardButton(text="Отменить редактирование пары 👋", callback_data="cancel")]
        ]
    )

    return edit_ikb
