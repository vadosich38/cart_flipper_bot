from typing import Union, List
from bot_set.bot_object import card_flipper_bot
from aiogram.types import ReplyKeyboardMarkup, Message
from DBPackage.DBclass import DBMethods


class DataFormatsHandlerToSendMessage:
    async def __call__(self, user_id: int, card_value: Union[str, int], card_value_type: str,
                       keyboard: Union[ReplyKeyboardMarkup, None] = None):
        if card_value_type == "text":
            await self.send_text(text=card_value, user_id=user_id, keyboard=keyboard)
        elif card_value_type == "photo":
            await self.send_photo(photo_id=card_value, user_id=user_id, keyboard=keyboard)
        elif card_value_type == "voice":
            await self.send_voice(voice_id=card_value, user_id=user_id, keyboard=keyboard)
        elif card_value_type == "video":
            await self.send_video(video_id=card_value, user_id=user_id, keyboard=keyboard)

    @staticmethod
    async def send_text(text: str, user_id: int, keyboard: Union[ReplyKeyboardMarkup, None]) -> None:
        await card_flipper_bot.send_message(chat_id=user_id,
                                            text=text,
                                            reply_markup=keyboard)

    @staticmethod
    async def send_photo(photo_id: int, user_id: int, keyboard: Union[ReplyKeyboardMarkup, None]) -> None:
        await card_flipper_bot.send_photo(chat_id=user_id,
                                          photo=photo_id,
                                          reply_markup=keyboard)

    @staticmethod
    async def send_voice(voice_id: int, user_id: int, keyboard: Union[ReplyKeyboardMarkup, None]) -> None:
        await card_flipper_bot.send_voice(chat_id=user_id,
                                          voice=voice_id,
                                          reply_markup=keyboard)

    @staticmethod
    async def send_video(video_id: int, user_id: int, keyboard: Union[ReplyKeyboardMarkup, None]) -> None:
        await card_flipper_bot.send_video(chat_id=user_id,
                                          video=video_id,
                                          reply_markup=keyboard)


def data_formats_handler_to_edit(message: Message, card_id: int, elem_num: int) -> None:
    # https://docs.aiogram.dev/en/latest/api/enums/content_type.html
    if message.content_type == "text":
        DBMethods.edit_card(card_id=card_id,
                            card_value=message.text,
                            card_value_type="text",
                            elem_num=elem_num)
    elif message.content_type == "photo":
        DBMethods.edit_card(card_id=card_id,
                            card_value=message.photo[-1].file_id,
                            card_value_type="photo",
                            elem_num=elem_num)
    elif message.content_type == "audio":
        DBMethods.edit_card(card_id=card_id,
                            card_value=message.audio.file_id,
                            card_value_type="audio",
                            elem_num=elem_num)
    elif message.content_type == "video":
        DBMethods.edit_card(card_id=card_id,
                            card_value=message.video.file_id,
                            card_value_type="video",
                            elem_num=elem_num)


def data_formats_handler_to_write(message: Message) -> dict[Union[str, int], str]:
    # https://docs.aiogram.dev/en/latest/api/enums/content_type.html
    #TODO: не уверен, что корректно получаю тип данных!!! проверить при тесте
    if message.content_type == "text":
        elem_to_write = {"value": message.text, "value_type": "text"}
    elif message.content_type == "photo":
        elem_to_write = {"value": message.photo[-1].file_id, "value_type": "photo"}
    elif message.content_type == "voice":
        elem_to_write = {"value": message.voice.file_id, "value_type": "voice"}
    elif message.content_type == "video":
        elem_to_write = {"value": message.video.file_id, "value_type": "video"}
    else:
        elem_to_write = {"value": message.text, "value_type": "unknown"}

    return elem_to_write


send_card_element = DataFormatsHandlerToSendMessage()
