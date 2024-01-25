from typing import Union
from bot_set.bot_object import card_flipper_bot
from aiogram.types import ReplyKeyboardMarkup, Message
from DBPackage.DBclass import DBMethods


class DataFormatsHandlerToSendMessage:
    def __call__(self, user_id: int, card_value: Union[str, int], card_value_type: str,
                 keyboard: Union[ReplyKeyboardMarkup, None] = None):
        if card_value_type == "text":
            self.send_text(text=card_value, user_id=user_id, keyboard=keyboard)
        elif card_value_type == "photo":
            self.send_photo(photo_id=card_value, user_id=user_id, keyboard=keyboard)
        elif card_value_type == "audio":
            self.send_audio(audio_id=card_value, user_id=user_id, keyboard=keyboard)
        elif card_value_type == "video":
            self.send_video(video_id=card_value, user_id=user_id, keyboard=keyboard)

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
    async def send_audio(audio_id: int, user_id: int, keyboard: Union[ReplyKeyboardMarkup, None]) -> None:
        await card_flipper_bot.send_audio(chat_id=user_id,
                                          audio=audio_id,
                                          reply_markup=keyboard)

    @staticmethod
    async def send_video(video_id: int, user_id: int, keyboard: Union[ReplyKeyboardMarkup, None]) -> None:
        await card_flipper_bot.send_video(chat_id=user_id,
                                          video=video_id,
                                          reply_markup=keyboard)


def data_formats_handler_to_write(message: Message, card_id: int, elem_numm: int) -> None:
    # https://docs.aiogram.dev/en/latest/api/enums/content_type.html
    if message.content_type == "text":
        DBMethods.edit_card(card_id=card_id,
                            card_value=message.text,
                            card_value_type="text",
                            elem_numm=elem_numm)
    elif message.content_type == "photo":
        DBMethods.edit_card(card_id=card_id,
                            card_value=message.photo[-1].file_id,
                            card_value_type="photo",
                            elem_numm=elem_numm)
    elif message.content_type == "audio":
        DBMethods.edit_card(card_id=card_id,
                            card_value=message.audio.file_id,
                            card_value_type="audio",
                            elem_numm=elem_numm)
    elif message.content_type == "video":
        DBMethods.edit_card(card_id=card_id,
                            card_value=message.video.file_id,
                            card_value_type="video",
                            elem_numm=elem_numm)


send_card_element = DataFormatsHandlerToSendMessage()
