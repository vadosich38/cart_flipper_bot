from DBPackage.DBclass import DBMethods
from typing import List, Tuple
import random
from typing import Union


class SpecCollCardsPaginator:
    """Paginator class for handling card navigation.
    Args:
        telegram_id (int): Telegram user ID.
    Attributes:
        card_values (List[Tuple[str, str, bool, int]]): List of card values from the active collection.
    """
    def __init__(self, telegram_id: int, mode: str = "active", collection_id: Union[int, None] = None):
        #TODO: некорректный коммент?
        # Getting card values if card has no attribute "learned"
        if mode == "active":
            self.card_values = DBMethods.get_active_collections_cards(telegram_id=telegram_id)
            self.turned_card = False
            random.shuffle(self.card_values)
        elif mode == "specific":
            # не удаляй тудушку, пож!
            #TODO: здесь будет использоваться метод БД для получения карточек конкретной коллекции
            # сначала свести выходные данные методов БД к одному формату!
            self.card_values = DBMethods.get_cards_by_collection_id(collection_id=collection_id)
            self.turned_card = False
            self.collection_id = collection_id
            self.cur_card_id = 0

    def start(self) -> str:
        """Get the value of the current card.
        Returns:
            str: The value of the current card.
        """
        self.cur_card_id = self.card_values[0][3]
        return self.card_values[0][0]

    def not_learned(self) -> str:
        """Moving card to the end of the list, proceed to next card
        Returns:
            str: The value of the next card.
        """
        # Moving card to the end of list.
        self.card_values.append(self.card_values.pop(0))
        # Set turned status to False
        self.turned_card = False
        self.cur_card_id = self.card_values[0][3]

        # Returns first card value
        return self.card_values[0][0]

    def show(self) -> str:
        """Get second value associated with the current card.
        Returns:
            str: Second value associated with the current card.
        """
        # Returns second
        if self.turned_card:
            self.turned_card = False
            return self.card_values[0][0]
        else:
            self.turned_card = True
            return self.card_values[0][1]

    def set_learned(self) -> str or None:
        """Setting learned status for card."""
        # Deleting card from local list
        del self.card_values[0]
        self.turned_card = False
        self.cur_card_id = self.card_values[0][3]

        # Getting value from the next card of return None
        return self.card_values[0][0] if self.card_values[0][0] else None
