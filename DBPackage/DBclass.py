import sqlite3
from loader import logger


class DBMethods:
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
        cur.execute('INSERT OR IGNORE INTO Cards (card_value_1, , card_value_2, collection_id) VALUES (?, ?, ?)',
                    (card_value_1, card_value_2, collection_id,))

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
    def get_cards_by_collection_id(cur, collection_id: int):
        """Get values of cards for a given collection_id"""
        logger.debug(f'Getting cards for collection_id: {collection_id}')
        cur.execute('''
            SELECT c.card_value_1, c.card_value_2
            FROM Cards c
            WHERE c.collection_id = ?
        ''', (collection_id,))
        return cur.fetchall()
