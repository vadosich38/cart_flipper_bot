from DBPackage.DBclass import DBMethods
from typing import List, Tuple
import random
from typing import Union


class SpecCollCardsPaginator:
    """Paginator class for handling card navigation.
    Args:
    Attributes:
        card_values (List[Tuple[int, str, str, str, str]]): List of card values from the specified collection.
    """
    def __init__(self, collection_id: int):
        # Get cards values by id of the selected collection
        self.card_values = DBMethods.get_cards_by_collection_id(collection_id=collection_id)
        self.turned_card = False
        self.collection_id = collection_id
        self.cur_card_id = 0
        self.cur_card_index = 0
        self.cards_count = len(self.card_values)

    def start(self) -> list:
        """Get the value of the current card.
        Returns:
            str: The value of the current card.
        """
        self.cur_card_id = self.card_values[0][0]
        return [self.card_values[0][1], self.card_values[0][2]]

    def previous(self) -> list:
        """return the previous card
        Returns:
            list: value and value data type
        """
        if self.cur_card_index == 0:
            self.cur_card_index = self.cards_count - 1
        else:
            self.cur_card_index -= 1

        self.cur_card_id = self.card_values[0][0]
        self.turned_card = False

        # Returns previous card value
        return [self.card_values[self.cur_card_index][1], self.card_values[self.cur_card_index][2]]

    def next(self) -> list:
        """return the next card
        Returns:
            list: value and value data type
        """
        if self.cur_card_index + 1 == self.cards_count:
            self.cur_card_index = 0
        else:
            self.cur_card_index += 1

        self.cur_card_id = self.card_values[0][0]
        self.turned_card = False

        # Returns next card value
        return [self.card_values[self.cur_card_index][1], self.card_values[self.cur_card_index][2]]

    def show(self) -> list:
        """Get second value associated with the current card.
        Returns:
            str: Second value associated with the current card.
        """
        # Returns second
        if self.turned_card:
            self.turned_card = False
            return [self.card_values[0][1], self.card_values[0][2]]
        else:
            self.turned_card = True
            return [self.card_values[0][3], self.card_values[0][4]]
