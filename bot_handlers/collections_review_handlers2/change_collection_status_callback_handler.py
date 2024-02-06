# Кнопка “Активировать/деактивировать коллекцию” изменяет статус активности выбранной коллекции.

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
import asyncio

from bot_handlers.collections_review_handlers2.collection_review_router import collections_review_router
from bot_set.texts import bot_texts
from keyboards.main_menu_kb import get_main_kb
from bot_set.bot_states import BotStates
from DBPackage.DBclass import DBMethods
from bot_set.bot_object import card_flipper_bot


@collections_review_router.callback_query(F.data == "activate", StateFilter(BotStates.collections_review))
async def collection_activate_callback(callback_data: CallbackQuery, state: FSMContext) -> None:
    #Из даты получаем экземпляр класса пагинатора коллекций, а затем его параметр айди коллекции
    data = await state.get_data()
    coll_pag_inst = data["coll_pag_inst"]
    collection_id = coll_pag_inst.current_collection_id

    DBMethods.set_collection_active_by_collection_id(collection_id=collection_id)

    #Пользователю сообщается о результате действия
    await callback_data.answer(text="Коллекция активирована 🟩", show_alert=True)
    #Удаляем старое сообщение
    await card_flipper_bot.delete_message(chat_id=callback_data.from_user.id,
                                          message_id=callback_data.message.message_id)
    await asyncio.sleep(2)

    #Возвращаем главное меню
    await card_flipper_bot.send_message(chat_id=callback_data.from_user.id,
                                        text=bot_texts["return_in_main_menu"],
                                        reply_markup=get_main_kb())

    #Очизается память и состояние бота, затем состояние возвращается в "главное меню"
    await state.clear()
    await state.set_state(BotStates.main_menu)


@collections_review_router.callback_query(F.data == "deactivate", StateFilter(BotStates.collections_review))
async def collection_deactivate_callback(callback_data: CallbackQuery, state: FSMContext) -> None:
    #Из даты получаем экземпляр класса пагинатора коллекций, а затем его параметр айди коллекции
    data = await state.get_data()
    coll_pag_inst = data["coll_pag_inst"]
    collection_id = coll_pag_inst.current_collection_id

    #Изменяется состояние коллекции
    DBMethods.set_collection_inactive_by_collection_id(collection_id=collection_id)

    #Пользователю сообщается о результате действия
    await callback_data.answer(text="Коллекция деактивирована 🟥", show_alert=True)
    #Удаляем старое сообщение
    await card_flipper_bot.delete_message(chat_id=callback_data.from_user.id,
                                          message_id=callback_data.message.message_id)
    await asyncio.sleep(2)

    #Возвращаем главное меню
    await card_flipper_bot.send_message(chat_id=callback_data.from_user.id,
                                        text=bot_texts["return_in_main_menu"],
                                        reply_markup=get_main_kb())

    #Очизается память и состояние бота, затем состояние возвращается в "главное меню"
    await state.clear()
    await state.set_state(BotStates.main_menu)

