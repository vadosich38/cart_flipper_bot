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
    pair_adding - режим добавления новой пары
    pair_editing - режим редактирвоания пары
    """

    teaching = State()
    collections_review = State()

    collection_adding_get_name = State()
    collection_adding_get_active_mode = State()
    collection_adding_get_fill_decision = State()

    collection_editing = State()

    pair_adding = State()
    pair_editing = State()
