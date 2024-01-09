#TODO:
# Состояние бота меняется на teaching
# запускается сценарий education_handlers
# Формируется список пар для обучения (метод класса работы с БД):
# Цикл проходит по списку активных коллекций и подключается к БД каждой коллекции,
# где собирает все пары в один словарь в рандом порядке.
# Идя по словарю бот последовательно отправляет пользователю сообщения:
# Объект: Элемент 1, кнопки инлайн клавиатуры: Знаю, развернуть, не знаю
# Когда словарь пуст, пользователь получает приветственное сообщение и напоминание о повторении. Выводится главное меню.


from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.filters import StateFilter
from bot_set.bot_states import BotStates
from keyboards.paginator_kb import cards_paginator_kb as pag_kb
from keyboards.paginator_kb import exit_kb
from bot_set.routers import education_cmd_router
from bot_set.paginator_class import Paginator


@education_cmd_router.message(F.text.lower() == "Учиться 🧑‍🏫")
async def education_cmd(message: Message, state: FSMContext) -> None:
    await state.set_state(BotStates.teaching)
    p_i = Paginator(message.chat.id)
    value = p_i.get_start()
    if value:
        await message.answer(value, reply_markup=pag_kb(p_i.get_pos(), p_i.get_len()))
        await state.set_data({'paginator_instance': p_i})
    else:
        await message.answer('All cards is learned', reply_markup=exit_kb())


@education_cmd_router.callback_query(F.data.startswith('paginator'), StateFilter(BotStates.teaching))
async def process_paginator_callback(callback_data: CallbackQuery, state: FSMContext):
    _, action = callback_data.data.split('_')
    data = await state.get_data()
    p_i = data['paginator_instance']
    if action == 'menu':
        await state.set_data({})
        await state.set_state(BotStates.main_menu)
    if p_i.get_len == 0:
        await callback_data.answer('All cards is learned', reply_markup=exit_kb())
    if action == 'back':
        await callback_data.answer(p_i.get_card_bck(), reply_markup=pag_kb(p_i.get_pos(), p_i.get_len()))
    elif action == 'forward':
        await callback_data.answer(p_i.get_card_fwd(), reply_markup=pag_kb(p_i.get_pos(), p_i.get_len()))
    elif action == 'show':
        await callback_data.answer(p_i.get_response(), reply_markup=pag_kb(p_i.get_pos(), p_i.get_len(), True))
    elif action == 'learned':
        p_i.set_learned()
        await callback_data.answer(p_i.get_start(), reply_markup=pag_kb(p_i.get_pos(), p_i.get_len()))
    await state.set_data({'paginator_instance': p_i})

