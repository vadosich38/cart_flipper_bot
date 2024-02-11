import asyncio

from bot_set.bot_object import card_flipper_bot
from DBPackage.DBclass import DBMethods
from keyboards.to_study_kb import get_to_study_notification_kb


async def send_notification():
    active_users = DBMethods.get_active_users_telegram_ids()
    success_counter = 0
    error_counter = 0
    for i_user in active_users:
        try:
            await card_flipper_bot.send_message(chat_id=i_user,
                                                text="Пришло время пройти урок, начни прямо сейчас 🧑‍🏫",
                                                reply_markup=get_to_study_notification_kb())
            success_counter += 1
            DBMethods.update_last_activity(telegram_id=i_user)
        except Exception as error:
            error_counter += 1
            print(f"Пользователь {i_user} не активен, ошибка: {error}")
            DBMethods.deactivate_user(telegram_id=i_user)
        finally:
            print(f"Успешно отправлено {success_counter} уведомлений, {error_counter} отправок привели к ошибке")


async def scheduler():
    while True:
        await send_notification()
        await asyncio.sleep(24 * 3600)
