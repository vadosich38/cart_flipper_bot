import sqlite3
from loader import logger
import pickle


class DBMethods:
    #TODO: пропиши плз доку где ее нет и типизацию данных
    DATABASE_NAME = 'main.db'

    @staticmethod
    def connect(func):
        """Database connection wrapper"""
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
    def create_tables(cur):
        """Creating tables in DB if they're not exist"""
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
                status BOOL NOT NULL,
                collection_id INTEGER,
                FOREIGN KEY (collection_id) REFERENCES Collections(collection_id)
            )
        ''')

    @staticmethod
    @connect
    def add_user(cur, telegram_id: int):
        """Add user record to the database"""
        logger.debug(f'Making user:{telegram_id} record in database')
        cur.execute('INSERT OR IGNORE INTO Users (telegram_id) VALUES (?)', (telegram_id,))

    @staticmethod
    @connect
    def add_collection_by_telegram_id(cur, telegram_id: int, collection_name: str):
        """Add collection record to the database"""
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
    def add_card_by_collection_id(cur, collection_id, card_value_1, card_value_2):
        logger.debug(f'Making card record in collection in database')
        cur.execute('INSERT OR IGNORE INTO Cards (card_value_1, card_value_2, '
                    'status, collection_id) VALUES (?, ?, ?, ?)',
                    (card_value_1, card_value_2, False, collection_id,))

    @staticmethod
    @connect
    def get_collections_by_telegram_id(cur, telegram_id: int):
        """Get a tuple of collections for a given telegram_id"""
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
    def set_collection_status_by_telegram_id(cur, telegram_id, collection_id, status):
        """Set status for a collection and reset status for other collections of the same user"""
        logger.debug(f'Setting active status for collection for telegram_id: {telegram_id}')

        # Reset status for other collections of the same user
        cur.execute('''
            UPDATE Collections
            SET status = 0
            WHERE user_id = (SELECT user_id FROM Users WHERE telegram_id = ?)
        ''', (telegram_id,))

        # Set status for the specified collection
        cur.execute('''
            UPDATE Collections
            SET status = ?
            WHERE user_id = (SELECT user_id FROM Users WHERE telegram_id = ?)
            AND collection_id = ?
        ''', (status, telegram_id, collection_id))

    @staticmethod
    @connect
    def get_active_collection_cards(cur, telegram_id):
        """Get a list of card IDs from the active collection for a user"""
        logger.debug(f'Getting card IDs from the active collection for telegram_id: {telegram_id}')

        # Retrieve the card IDs from the active collection for the given user
        cur.execute('''
            SELECT c.card_value_1, c.card_value_2, c.status, c.card_id
            FROM Cards c
            JOIN Collections col ON c.collection_id = col.collection_id
            JOIN Users u ON col.user_id = u.user_id
            WHERE u.telegram_id = ? AND col.status = 1
        ''', (telegram_id,))
        return cur.fetchall()

    @staticmethod
    @connect
    def set_card_learned_status(cur, card_id):
        """Set the learned status of a card to True by its ID"""
        logger.debug(f'Setting learned status to True for card ID: {card_id}')

        # Set the status to True for the specified card ID
        cur.execute('''
            UPDATE Cards
            SET status = 1
            WHERE card_id = ?
        ''', (card_id,))
