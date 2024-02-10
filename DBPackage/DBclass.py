import sqlite3
from loader import logger
from typing import List, Tuple, Union
from datetime import datetime, timedelta


class DBMethods:
    #Done: нужны 5 методов:
    # 1. - Получить telegram id всех активных пользователей -> list
    # 2. - Актуализировать (изменить) дату и время последней активности пользователя (запись str в тиблицу)
    # 3. - Деактивировать пользователя (установить 0 False в столбец активности юзера)
    # 4. - Метод добавления в столбец next_lesson 20 минут от момента добавления new_time = current_time + timedelta(minutes=20) конкретному пользователю по телеграм айди
    # 5. - Метод получения next_lesson -> class 'datetime.datetime'
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
        #DONE: нужно добавить две строки: статус пользователя Актив или не актив (0, 1) и дату последней активности
        # также столбец "next lesson" с типом class 'datetime.datetime'
        logger.debug('Creating database tables')
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS Users (
                        user_id INTEGER PRIMARY KEY,
                        telegram_id INTEGER NOT NULL UNIQUE,
                        active_status BOOL NOT NULL,
                        last_activity_date TIMESTAMP NOT NULL,
                        next_lesson TIMESTAMP
                    )''')

        cur.execute('''
                    CREATE TABLE IF NOT EXISTS Collections (
                        collection_id INTEGER PRIMARY KEY,
                        collection_name TEXT NOT NULL,
                        status BOOL NOT NULL,
                        user_id INTEGER,
                        FOREIGN KEY (user_id) REFERENCES Users(user_id)
                    )''')

        cur.execute('''
                    CREATE TABLE IF NOT EXISTS Cards (
                        card_id INTEGER PRIMARY KEY,
                        card_value_1 TEXT NOT NULL,
                        value1_type TEXT NOT NULL,
                        card_value_2 TEXT NOT NULL,
                        value2_type TEXT NOT NULL,
                        collection_id INTEGER,
                        FOREIGN KEY (collection_id) REFERENCES Collections(collection_id)
                    )''')

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
        #Done: при создании пользователя нужно также передавать статус и дату активности.
        # При создании пользователь всегда актив, дата записывается из метода datetime.now()
        # если пользователь существует в базе и статус активности == 0 (не активен),
        # то нужно сменить на 1 (активен) и обновить дату активности
        # next_lesson устанавливается в текущее время datetime.now() тип данных class 'datetime.datetime'
        """Add user record to the database
        Args:
            cur: The SQLite cursor.
            telegram_id (int): Telegram user ID.
        Returns:
            None
        """
        time_now = datetime.now()
        logger.debug(f'Making user:{telegram_id} record in database')
        cur.execute('INSERT OR IGNORE INTO Users (telegram_id, active_status, last_activity_date, next_lesson) '
                    'VALUES (?, ?, ?, ?)',
                    (telegram_id, 1, time_now, time_now,))

        # Checking if the user exists and is active, if so, update last activity date
        cur.execute('''
            UPDATE Users 
            SET last_activity_date = ? 
            WHERE telegram_id = ? AND active_status = 1
        ''', (time_now, telegram_id,))

        # Checking if the user exists and is inactive, if so, activate them and update last activity date
        cur.execute('''
            UPDATE Users 
            SET active_status = 1, last_activity_date = ? 
            WHERE telegram_id = ? AND active_status = 0
        ''', (time_now, telegram_id,))

    @staticmethod
    @connect
    def add_collection_by_telegram_id(cur, telegram_id: int, collection_name: str, coll_status: int) -> None:
        """Add collection record to the database.
        Args:
            cur: The SQLite cursor.
            telegram_id (int): Telegram user ID.
            collection_name (str): Name of the collection.
            coll_status (int): Collection status (active/deactive)
        Returns:
            None
        """
        logger.debug(f'Making collection record in database: {telegram_id, collection_name, coll_status}')
        # Getting user_id
        cur.execute('SELECT user_id FROM Users WHERE telegram_id = ?', (telegram_id,))
        user_id = cur.fetchone()
        # Adding collection if user exits
        if user_id:
            #TODO: оставлять OR IGNORE?
            cur.execute('INSERT INTO Collections (collection_name, user_id, status) VALUES (?, ?, ?)',
                        (collection_name, user_id[0], coll_status))
            # cur.execute('INSERT OR IGNORE INTO Collections (collection_name, user_id) VALUES (?, ?)',
            #             (collection_name, user_id[0]))
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
            """INSERT INTO Cards (card_value_1, value1_type, card_value_2, value2_type, collection_id) 
            VALUES (?, ?, ?, ?, ?)
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
        ''', (collection_id,))

    from typing import List, Tuple

    @staticmethod
    @connect
    def get_active_collections_cards(cur, telegram_id: int) \
            -> List[Tuple[int, Union[str, int], str, Union[str, int], str]]:
        """Get a list of card values from the active collection for a user.
        Args:
            cur: The SQLite cursor.
            telegram_id (int): Telegram user ID.
        Returns:
            List of tuples containing card_id, card_value_1, value1_type, card_value_2, value2_type.
        """
        logger.debug(f'Getting card values from the active collection for telegram_id: {telegram_id}')
        # Retrieve the card values from the active collection for the given user
        cur.execute('''
            SELECT c.card_id, c.card_value_1, c.value1_type, c.card_value_2, c.value2_type
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

    # DONE: нужен метод, принимающий айди коллекции и возвращающий bool, True если коллекция активна,
    # False если не активна
    @staticmethod
    @connect
    def is_collection_active(cur, collection_id: int) -> bool:
        """
        Get collection status by collection_id
        Args:
            cur: The SQLite cursor.
            collection_id(int): ID if the collection.
        Returns:
                Bool
        """
        cur.execute('''
            SELECT status
            FROM Collections col
            JOIN Users u ON col.user_id = u.user_id
            WHERE col.collection_id = ? 
        ''', (collection_id,))

        collection_status = int(cur.fetchone()[0])

        if collection_status == 0:
            return False

        return True

    @staticmethod
    @connect
    def edit_card(cur, card_id: int, card_value: Union[str, int], card_value_type: str, elem_num: int) -> None:
        # DONE: нужен метод, который будет принимать новые элементы карточки и перезаписывать их при редактировании карточки.
        # принимает параметр card_id и производит поиск карточки по этому параметру
        # принимает card_value, card_value_type и elem_numm номер стороны карточки - 1 (будет elem1) или 2 (elem2).
        # затем записывает изменения в карточке
        """Edit a card by updating its values.
        Args:
            cur: The SQLite cursor.
            card_id (int): ID of the card to be edited.
            card_value (Union[str, int]): New value for the card.
            card_value_type (str): Type of the card value (photo, text, audio, video, etc.).
            elem_num (int): Element number (1 or 2) to indicate which side of the card to edit.
        Returns:
            None
        """
        logger.debug(f'Editing card with card_id: {card_id}')

        # Determine which card_value and card_value_type to update based on elem_num
        if elem_num == 1:
            update_column = 'card_value_1'
            update_type_column = 'value1_type'
        elif elem_num == 2:
            update_column = 'card_value_2'
            update_type_column = 'value2_type'
        else:
            raise ValueError("elem_num should be 1 or 2.")

        # Update the specified values in the card
        cur.execute(f'''
            UPDATE Cards
            SET {update_column} = ?, {update_type_column} = ?
            WHERE card_id = ?
        ''', (card_value, card_value_type, card_id,))

    @staticmethod
    @connect
    def delete_collection_by_id(cur, collection_id: int) -> None:
        """Delete a collection and all its cards by collection_id.
        Args:
            cur: The SQLite cursor.
            collection_id (int): ID of the collection to be deleted.
        Returns:
            None
        """
        logger.debug(f'Deleting collection with collection_id: {collection_id}')

        # Delete all cards associated with the collection
        cur.execute('DELETE FROM Cards WHERE collection_id = ?', (collection_id,))

        # Delete the collection itself
        cur.execute('DELETE FROM Collections WHERE collection_id = ?', (collection_id,))

    @staticmethod
    @connect
    def get_active_users_telegram_ids(cur) -> list:
        """Get the telegram IDs of all active users.
        Args:
            cur: The SQLite cursor.
        Returns:
            list: List of active users' telegram IDs.
        """
        logger.debug('Getting telegram IDs of all active users')
        cur.execute('SELECT telegram_id FROM Users WHERE active_status = 1')
        result = cur.fetchall()
        telegram_ids = [row[0] for row in result]
        return telegram_ids

    @staticmethod
    @connect
    def update_last_activity(cur, telegram_id: int) -> None:
        """Update the last activity date and time for a user.
        Args:
            cur: The SQLite cursor.
            telegram_id (int): Telegram user ID.
        Returns:
            None
        """
        logger.debug(f'Updating last activity for user: {telegram_id}')
        cur.execute('UPDATE Users SET last_activity_date = ? WHERE telegram_id = ?', (datetime.now(), telegram_id,))

    @staticmethod
    @connect
    def deactivate_user(cur, telegram_id: int) -> None:
        """Deactivate a user.
        Args:
            cur: The SQLite cursor.
            telegram_id (int): Telegram user ID.
        Returns:
            None
        """
        logger.debug(f'Deactivating user: {telegram_id}')
        cur.execute('UPDATE Users SET active_status = 0 WHERE telegram_id = ?', (telegram_id,))

    @staticmethod
    @connect
    def set_next_lesson(cur, telegram_id: int) -> None:
        """Set the next lesson for a user 20 minutes from the current time.
        Args:
            cur: The SQLite cursor.
            telegram_id (int): Telegram user ID.
        Returns:
            None
        """
        logger.debug(f'Setting next lesson for user: {telegram_id}')
        new_time = datetime.now() + timedelta(minutes=20)
        cur.execute('UPDATE Users SET next_lesson = ? WHERE telegram_id = ?', (new_time, telegram_id))

    @staticmethod
    @connect
    def get_next_lesson(cur, telegram_id: int) -> datetime:
        """Get the next lesson datetime for a user.
        Args:
        cur: The SQLite cursor.
        telegram_id (int): Telegram user ID.
        Returns:
        datetime: The datetime of the next lesson.
        """
        logger.debug(f'Getting next lesson for user: {telegram_id}')
        cur.execute('SELECT next_lesson FROM Users WHERE telegram_id = ?', (telegram_id,))
        result = cur.fetchone()
        if result:
            #возвращаем объект datetime для сравнения
            return datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S.%f')
        else:
            logger.warning(f'Next lesson not found for user: {telegram_id}')
            return datetime.now()
