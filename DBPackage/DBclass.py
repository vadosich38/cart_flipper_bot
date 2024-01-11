import sqlite3
from loader import logger
from typing import List, Tuple
import pickle


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
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS Collections (
                collection_id INTEGER PRIMARY KEY,
                collection_name TEXT NOT NULL,
                status BOOL NOT NULL,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES Users(user_id)
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS Cards (
                card_id INTEGER PRIMARY KEY,
                card_value_1 TEXT NOT NULL,
                card_value_2 TEXT NOT NULL,
                collection_id INTEGER,
                FOREIGN KEY (collection_id) REFERENCES Collections(collection_id)
            )
        ''')

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
    def add_card_by_collection_id(cur, collection_id: int, card_value_1: str, card_value_2: str) -> None:
        """Add card record to the collection in the database.
        Args:
            cur: The SQLite cursor.
            collection_id (int): ID of the collection.
            card_value_1 (str): Value 1 of the card.
            card_value_2 (str): Value 2 of the card.
        Returns:
            None
        """
        logger.debug(f'Making card record in collection in database')
        cur.execute('INSERT OR IGNORE INTO Cards (card_value_1, card_value_2, '
                    'status, collection_id) VALUES (?, ?, ?)',
                    (card_value_1, card_value_2, collection_id,))

    @staticmethod
    @connect
    def get_collections_by_telegram_id(cur, telegram_id: int) -> List[Tuple[str, int]]:
        """Get a tuple of collections for a given telegram_id.
        Args:
            cur: The SQLite cursor.
            telegram_id (int): Telegram user ID.
        Returns:
            List of tuples containing collection_name and collection_id.
        """
        logger.debug(f'Getting collections for telegram_id: {telegram_id}')
        cur.execute('''
            SELECT c.collection_name, c.collection_id
            FROM Collections c
            JOIN Users u ON c.user_id = u.user_id
            WHERE u.telegram_id = ?
        ''', (telegram_id,))
        return cur.fetchall()

    @staticmethod
    @connect
    def set_collection_active_by_telegram_id(cur, telegram_id: int, collection_id: int) -> None:
        """Set status for a collection and reset status for other collections of the same user.
        Args:
            cur: The SQLite cursor.
            telegram_id (int): Telegram user ID.
            collection_id (int): ID of the collection.
        Returns:
            None
        """
        logger.debug(f'Setting active status for collection for telegram_id: {telegram_id}')

        # Reset status for other collections of the same user
        cur.execute('''
            UPDATE Collections
            SET status = 0
            WHERE user_id = (SELECT user_id FROM Users WHERE telegram_id = ?)
        ''', (telegram_id,))

        # Set the status to True for the specified collection ID
        cur.execute('''
            UPDATE Collections
            SET status = 1
            WHERE user_id = (SELECT user_id FROM Users WHERE telegram_id = ?)
            AND collection_id = ?
        ''', (telegram_id, collection_id))

    @staticmethod
    @connect
    def get_active_collection_cards(cur, telegram_id: int) -> List[Tuple[str, str]]:
        """Get a list of card IDs from the active collection for a user.
        Args:
            cur: The SQLite cursor.
            telegram_id (int): Telegram user ID.
        Returns:
            List of tuples containing card_value_1, card_value_2,
        """
        logger.debug(f'Getting card IDs from the active collection for telegram_id: {telegram_id}')

        # Retrieve the card IDs from the active collection for the given user
        cur.execute('''
            SELECT c.card_value_1, c.card_value_2
            FROM Cards c
            JOIN Collections col ON c.collection_id = col.collection_id
            JOIN Users u ON col.user_id = u.user_id
            WHERE u.telegram_id = ? AND col.status = 1
        ''', (telegram_id,))
        return cur.fetchall()

