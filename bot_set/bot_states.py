from aiogram.fsm.state import StatesGroup, State


class BotStates(StatesGroup):
    """Класс описывающий состояния бота

    ОСНОВНОЙ ФУНКЦИОНАЛ БОТА
    teaching - режим обучения
    collections - режим просмотра коллекций

    РАБОТА С КОЛЛЕКЦИЯМИ
    collection_edition - режим демонстрации содержимого коллекции и доступам к функциям редактирования коллекций
    collection_adding - режим создания новой коллекции

    РАБОТА С ПАРАМИ
    paar_adding - режим добавления новой пары
    paar_editing - режим редактирвоания пары
    """

    teaching = State()
    collections_review = State()

    collection_adding = State()
    collection_edition = State()

    paar_adding = State()
    paar_editing = State()
