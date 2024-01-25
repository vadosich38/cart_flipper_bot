from DBPackage.DBclass import DBMethods
from typing import List, Tuple
import random
from typing import Union


class CardsPaginator:
    #TODO: изменить класс с учетом изсенений метода БД get_active_collections_cards
    """Paginator class for handling card navigation.
    Args:
        telegram_id (int): Telegram user ID.
    Attributes:
        card_values (List[Tuple[str, str, bool, int]]): List of card values from the active collection.
    """
    def __init__(self, telegram_id: int):
        #TODO: некорректный коммент?
        # Getting card values if card has no attribute "learned"
        self.card_values = DBMethods.get_active_collections_cards(telegram_id=telegram_id)
        self.turned_card = False
        random.shuffle(self.card_values)

    def start(self) -> tuple[Union[str, int], str]:
        """Get the value of the current card.
        Returns:
            str: The value of the current card.
        """
        return self.card_values[0][1], self.card_values[0][2]

    def not_learned(self) -> tuple[Union[str, int], str]:
        """Moving card to the end of the list, proceed to next card
        Returns:
            str: The value of the next card.
        """
        # Moving card to the end of list.
        self.card_values.append(self.card_values.pop(0))
        # Set turned status to False
        self.turned_card = False

        # Returns first card value
        return self.card_values[0][1], self.card_values[0][2]

    def show(self) -> tuple[Union[str, int], str]:
        """Get second value associated with the current card.
        Returns:
            str: Second value associated with the current card.
        """
        # Returns second
        if self.turned_card:
            self.turned_card = False
            return self.card_values[0][1], self.card_values[0][2]
        else:
            self.turned_card = True
            return self.card_values[0][3], self.card_values[0][4]

    def set_learned(self) -> tuple[Union[str, int], str] or None:
        """Setting learned status for card."""
        # Deleting card from local list
        del self.card_values[0]
        self.turned_card = False

        # Getting value from the next card of return None
        return self.card_values[0][1], self.card_values[0][2] if self.card_values[0][1] else None
