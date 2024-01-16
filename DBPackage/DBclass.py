import sqlite3
from loader import logger
from typing import List, Tuple
import pickle


#TODO: нужен метод, принимающий айди коллекции и возвращающий bool, True если коллекция активна, False если не активна
class DBMethods:
    DATABASE_NAME = 'main.db'

    @staticmethod
    def connect(func):
        """Database connection wrapper.
        Args:
            func: The function to be wrapped with a database connection.
        Returns:
            The wrapped function.
        """
        def wrapper(*args, **kwargs):
            try:
                connection = sqlite3.connect(DBMethods.DATABASE_NAME)
                cur = connection.cursor()
                logger.debug('Database connection successful')
                result = func(cur, *args, **kwargs)
                connection.commit()
                connection.close()
                return result
            except Exception as exc:
                logger.error(f'Error connecting database: {exc}')
        return wrapper

    @staticmethod
    @connect
    def create_tables(cur) -> None:
        """Creating tables in DB if they're not exist
        Args:
            cur: The SQLite cursor.
        Returns:
            None
        """
        logger.debug('Creating database tables')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                user_id INTEGER PRIMARY KEY,
                telegram_id INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS Collections (
                collection_id INTEGER PRIMARY KEY,
                collection_name TEXT NOT NULL,
                status BOOL NOT NULL,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES Users(user_id)
            );

            CREATE TABLE IF NOT EXISTS Cards (
                card_id INTEGER PRIMARY KEY,
                card_value_1 TEXT NOT NULL,
                card_value_2 TEXT NOT NULL,
                collection_id INTEGER,
                FOREIGN KEY (collection_id) REFERENCES Collections(collection_id)
            );
        ''')

    @staticmethod
    @connect
    def get_collection_id_by_collection_name_and_telegram_id(cur, collection_name: str, telegram_id: int) -> int:
        """Get the collection_id for a given collection_name and telegram_id.
        Args:
            cur: The SQLite cursor.
            collection_name (str): Collection name.
            telegram_id (int): Telegram user ID.
        Returns:
            int: The collection_id if found, otherwise 0.
        """
        logger.debug(f'Getting collection_id for collection_name: {collection_name} and telegram_id: {telegram_id}')

        # Fetch the collection_id based on collection_name and telegram_id
        cur.execute('''
            SELECT collection_id
            FROM Collections col
            JOIN Users u ON col.user_id = u.user_id
            WHERE col.collection_name = ? AND u.telegram_id = ?
        ''', (collection_name, telegram_id))

        result = cur.fetchone()

        if result:
            collection_id = result[0]
            logger.debug(
                f'Found collection_id: {collection_id} for collection_name: {collection_name} and telegram_id: {telegram_id}')
            return collection_id
        else:
            logger.warning(
                f'Collection not found for collection_name: {collection_name} and telegram_id: {telegram_id}')
            return 0

    @staticmethod
    @connect
    def add_user(cur, telegram_id: int) -> None:
        """Add user record to the database
        Args:
            cur: The SQLite cursor.
            telegram_id (int): Telegram user ID.
        Returns:
            None
        """
        logger.debug(f'Making user:{telegram_id} record in database')
        cur.execute('INSERT OR IGNORE INTO Users (telegram_id) VALUES (?)', (telegram_id,))

    @staticmethod
    @connect
    def add_collection_by_telegram_id(cur, telegram_id: int, collection_name: str) -> None:
        """Add collection record to the database.
        Args:
            cur: The SQLite cursor.
            telegram_id (int): Telegram user ID.
            collection_name (str): Name of the collection.
        Returns:
            None
        """
        logger.debug(f'Making collection record in database')
        # Getting user_id
        cur.execute('SELECT user_id FROM Users WHERE telegram_id = ?', (telegram_id,))
        user_id = cur.fetchone()
        # Adding collection if user exits
        if user_id:
            cur.execute('INSERT OR IGNORE INTO Collections (collection_name, user_id) VALUES (?, ?)',
                        (collection_name, user_id[0]))
        else:
            logger.warning(f'User with telegram_id {telegram_id} not found. Collection not added.')

    @staticmethod
    @connect
    def add_card_by_collection_id(cur, collection_id: int, card_value_1: str, value1_type: str,
                                  card_value_2: str, value2_type: str) -> None:
        """Add card record to the collection in the database.
        Args:
            cur: The SQLite cursor.
            collection_id (int): ID of the collection.
            card_value_1 (str): Value 1 of the card.
            value1_type (str): Type of value 1 (photo, text, audio, video, etc.).
            card_value_2 (str): Value 2 of the card.
            value2_type (str): Type of value 2 (photo, text, audio, video, etc.).
        Returns:
            None
        """
        logger.debug(f'Making card record in collection in database')
        cur.execute(
            """INSERT OR IGNORE INTO Cards (card_value_1, value1_type, card_value_2, value2_type, status, 
            collection_id) VALUES (?, ?, ?, ?, ?),
            """,
            (card_value_1, value1_type, card_value_2, value2_type, collection_id,))

    @staticmethod
    @connect
    def get_collections_by_telegram_id(cur, telegram_id: int) -> List[Tuple[str, int, bool, int]]:
        """Get a tuple of collections for a given telegram_id.
        Args:
            cur: The SQLite cursor.
            telegram_id (int): Telegram user ID.
        Returns:
            List of tuples containing collection_name, collection_id, status, and cards_count.
        """

        logger.debug(f'Getting collections for telegram_id: {telegram_id}')
        cur.execute('''
            SELECT c.collection_name, c.collection_id, c.status, COUNT(card_id) AS cards_count
            FROM Collections c
            JOIN Users u ON c.user_id = u.user_id
            LEFT JOIN Cards card ON card.collection_id = c.collection_id
            WHERE u.telegram_id = ?
            GROUP BY c.collection_name, c.collection_id, c.status
        ''', (telegram_id,))

        return cur.fetchall()

    @staticmethod
    @connect
    def set_collection_active_by_collection_id(cur, collection_id: int) -> None:
        """Set status for a collection and reset status for other collections of the same user.
        Args:
            cur: The SQLite cursor.

            collection_id (int): ID of the collection.
        Returns:
            None
        """
        logger.debug(f'Setting active status for collection.')

        # Set the status to True for the specified collection ID
        cur.execute('''
            UPDATE Collections
            SET status = 1
            WHERE collection_id = ?
        ''', (collection_id,))

    @staticmethod
    @connect
    def set_collection_inactive_by_collection_id(cur, collection_id: int) -> None:
        """Set status to inactive for a collection and reset status for other collections of the same user.
        Args:
            cur: The SQLite cursor.
            collection_id (int): ID of the collection.
        Returns:
            None
        """
        logger.debug(f'Setting inactive status for collection.')

        # Set the status to False for the specified collection ID
        cur.execute('''
            UPDATE Collections
            SET status = 0
            WHERE collection_id = ?
        ''', (collection_id, ))

    from typing import List, Tuple

    @staticmethod
    @connect
    def get_active_collections_cards(cur, telegram_id: int) -> List[Tuple[str, str, str, str]]:
    #TODO: добавить в выдачу id карточки List[Tuple[int, str, str, str, str]]
        """Get a list of card values from the active collection for a user.
        Args:
            cur: The SQLite cursor.
            telegram_id (int): Telegram user ID.
        Returns:
            List of tuples containing card_value_1, value1_type, card_value_2, value2_type.
        """
        logger.debug(f'Getting card values from the active collection for telegram_id: {telegram_id}')

        # Retrieve the card values from the active collection for the given user
        cur.execute('''
            SELECT c.card_value_1, c.value1_type, c.card_value_2, c.value2_type
            FROM Cards c
            JOIN Collections col ON c.collection_id = col.collection_id
            JOIN Users u ON col.user_id = u.user_id
            WHERE u.telegram_id = ? AND col.status = 1
        ''', (telegram_id,))

        return cur.fetchall()

    @staticmethod
    @connect
    def get_cards_by_collection_id(cur, collection_id: int) -> List[Tuple[int, str, str, str, str]]:
        """Get a tuple of cards for a given collection_id.
        Args:
            cur: The SQLite cursor.
            collection_id (int): Collection ID.
        Returns:
            List of tuples containing card_id, card_value_1, value1_type, card_value_2, value2_type.
        """

        logger.debug(f'Getting cards for collection_id: {collection_id}')

        cur.execute('''
            SELECT card_id, card_value_1, value1_type, card_value_2, value2_type
            FROM Cards
            WHERE collection_id = ?
        ''', (collection_id,))

        return cur.fetchall()

    @staticmethod
    @connect
    def delete_card_by_id(cur, card_id: int) -> None:
        """Delete a card by its card_id.
        Args:
            cur: The SQLite cursor.
            card_id (int): ID of the card to be deleted.
        Returns:
            None
        """
        logger.debug(f'Deleting card with card_id: {card_id}')

        # Delete the card with the specified card_id
        cur.execute('DELETE FROM Cards WHERE card_id = ?', (card_id,))

    @staticmethod
    @connect
    def get_card_by_id(cur, card_id: int) -> Tuple[int, str, str, str, str, int] or None:
        """Get a card by its card_id.
        Args:
            cur: The SQLite cursor.
            card_id (int): ID of the card to be retrieved.
        Returns:
            Tuple containing card_id, card_value_1, value1_type, card_value_2, value2_type, collection_id.
        """
        logger.debug(f'Getting card with card_id: {card_id}')

        # Retrieve the card with the specified card_id
        cur.execute('''
            SELECT card_id, card_value_1, value1_type, card_value_2, value2_type, collection_id
            FROM Cards
            WHERE card_id = ?
        ''', (card_id,))

        result = cur.fetchone()

        if result:
            logger.debug(f'Found card with card_id: {card_id}')
            return result
        else:
            logger.warning(f'Card not found with card_id: {card_id}')
            return None
