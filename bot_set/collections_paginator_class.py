from DBPackage.DBclass import DBMethods
from typing import List, Tuple


class CollectionsPaginator:
    """Paginator class for handling collections navigation.
    Args:
        telegram_id (int): Telegram user ID.
    Attributes:
        all_collections List[Tuple(str, int, int/str/bool, int]: List of all collections by user.
    """
    def __init__(self, telegram_id: int):
        # Getting all collections data by user
        self.all_collections = DBMethods.get_collections_by_telegram_id(telegram_id=telegram_id)
        # Counter of the sequence number of the displayed collection
        self.collection_index = 0
        self.current_collection_id = self.all_collections[self.collection_index][1]
        # Number of collections to display
        self.collections_number = len(self.all_collections)

    def start(self) -> str:
        """Get the current collection data.
        Returns:
            str: message text for the collection.
        """
        current_collection = self.all_collections[self.collection_index]

        return (f"{current_collection[0]}\n"
                f"Статус: {current_collection[2]}\n"
                f"Количество карточек в коллекции: {current_collection[3]}")

    def next(self) -> str:
        """Returns information about the next collection.
        Returns:
            str: information about the next collection
        """
        # If the last collection in the list is open, the list starts over when you click on the "next" button
        if self.collection_index + 1 == self.collections_number:
            self.collection_index = 0
        else:
            # else increase the counter of the current collection
            self.collection_index += 1

        current_collection = self.all_collections[self.collection_index]
        # Set current collection id
        self.current_collection_id = self.all_collections[self.collection_index][1]

        # Returns next collection data
        return (f"{current_collection[0]}\n"
                f"Статус: {current_collection[2]}\n"
                f"Количество карточек в коллекции: {current_collection[3]}")

    def previous(self) -> str:
        """Returns information about the previous collection.
        Returns:
            str: information about the previous collection.
        """
        # If the first collection in the list is open, pressing the "back" button
        # will jump to the last collection in the list.
        if self.collection_index == 0:
            self.collection_index = self.collections_number - 1
        else:
            # Decrease the counter of the current collection
            self.collection_index -= 1

        current_collection = self.all_collections[self.collection_index]
        # Set current collection id
        self.current_collection_id = self.all_collections[self.collection_index][1]

        # Returns next collection data
        return (f"{current_collection[0]}\n"
                f"Статус: {current_collection[2]}\n"
                f"Количество карточек в коллекции: {current_collection[3]}")
