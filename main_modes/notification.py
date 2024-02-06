#TODO: обработать нажатие кнопки "напомнить позже"
import aioschedule
import asyncio
import time

from bot_set.bot_object import card_flipper_bot
from DBPackage.DBclass import DBMethods
from keyboards.to_study_kb import get_to_study_notification_kb


async def send_notification():
    #TODO: получить всех пользователей
    # active_users = DBMethods.
    success_counter = 0
    error_counter = 0
    for i_user in active_users:
        try:
            await card_flipper_bot.send_message(chat_id=i_user,
                                                text="Пришло время пройти урок, начни прямо сейчас 🧑‍🏫",
                                                reply_markup=get_to_study_notification_kb())
            success_counter += 1
            #TODO: здесь обновить дату активности пользователя
        except Exception as error:
            error_counter += 1
            print(f"Пользователь {i_user} не активен, ошибка: {error}")
            #TODO: здесь деактивировать пользователя
        finally:
            print(f"Успешно отправлено {success_counter} уведомлений, {error_counter} отправок привели к ошибке")

aioschedule.every().day.at("17:30").do(send_notification)

loop = asyncio.get_event_loop()
while True:
    loop.run_until_complete(aioschedule.run_pending())
    # time.sleep(0.1)
