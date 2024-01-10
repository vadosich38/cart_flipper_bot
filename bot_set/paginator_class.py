from DBPackage.DBclass import DBMethods
from typing import List, Tuple
import random


class Paginator:
    """Paginator class for handling card navigation.
    Args:
        telegram_id (int): Telegram user ID.
    Attributes:
        card_values (List[Tuple[str, str, bool, int]]): List of card values from the active collection.
    """
    def __init__(self, telegram_id: int):
        # Getting card values if card has no attribute "learned"
        self.card_values = [i for i in DBMethods.get_active_collection_cards(telegram_id) if i[2] == 0]
        # Randomizing list
        random.shuffle(self.card_values)

    def start(self) -> str:
        """Get the value of the current card.
        Returns:
            str: The value of the current card.
        """
        return self.card_values[0][0]

    def not_learned(self) -> str:
        """Moving card to the end of the list, proceed to next card
        Returns:
            str: The value of the next card.
        """
        self.card_values.append(self.card_values.pop(0))
        return self.card_values[0][0]

    def show(self) -> str:
        """Get second value associated with the current card.
        Returns:
            str: Second value associated with the current card.
        """
        return self.card_values[0][1]

    def set_learned(self) -> str or None:
        """Setting learned status for card in DB."""
        # Setting learned status for card
        DBMethods.set_card_learned_status(self.card_values[0][3])
        # Deleting card from local list
        del self.card_values[0]
        # Getting value from the next card of return None
        return self.card_values[0][0] if self.card_values[0][0] else None
