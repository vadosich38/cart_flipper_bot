#TODO: Пользователь получает сообщение "Ваша пара имеет обратное значение?":
# да – добавляется 2 пары (зеркальные), нет - одна.
# Пользователь получает уведомление об успешном добавлении пары.
# состояние бота меняется на FSM: collection_edit_handlers
# пользователь возвращается в меню редактирвоания коллекции и запускается сценарий collection_edit_handlers

from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from .pair_add_router import pair_add_router
from bot_set.bot_states import BotStates
from bot_set.bot_object import cart_flipper_bot


@pair_add_router.callback_query(StateFilter(BotStates.set_mirror_mode_new_pair_adding))
async def set_mirror_mode(callback_data: CallbackQuery, state: FSMContext) -> None:
    if callback_data.data == "yes":
        #TODO: производится запись карточки два раза зеркально (элемент1 == элемент2 и элемент2 == элемент1)
        await callback_data.answer(text="Добавить карточку зеркально 🟢")
    else:
        # TODO: производится запись карточки один раз (элемент1 == элемент2)
        await callback_data.answer(text="Добавить карточку 🟢")

    await cart_flipper_bot.send_message(chat_id=callback_data.from_user.id,
                                        text="Карточка добавлена! 🟩\n\n")
    await state.set_state(BotStates.collection_editing)
    #TODO: вернуть список пар колекции по сценарию редактирвоания коллекции!
