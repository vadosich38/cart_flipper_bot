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
    main_menu = State()

    teaching = State()
    collections_review = State()

    collection_adding_get_name = State()
    collection_adding_get_active_mode = State()
    collection_adding_get_fill_decision = State()

    collection_editing = State()

    get_first_elem_new_pair_adding = State()
    get_second_elem_new_pair_adding = State()
    set_mirror_mode_new_pair_adding = State()

    pair_editing_change_first_elem = State()
    pair_editing_change_second_elem = State()


