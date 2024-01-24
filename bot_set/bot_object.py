from aiogram import Bot
from config_reader import config

card_flipper_bot = Bot(token=config.bot_token.get_secret_value(),
                       parse_mode="HTML")
