from typing import Union
from bot_set.bot_object import card_flipper_bot
from aiogram.types import ReplyKeyboardMarkup


class DataFormatsHandler:
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


send_card_element = DataFormatsHandler()
