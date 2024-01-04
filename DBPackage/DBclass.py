import sqlite3


class DBMethods:
    pass
## пример структуры DB. твое мнение?

# Создаем соединение с базой данных
#TODO: соединение нужно создавать в другом файле в функции get_connection,
# используется одно соединение и хранится как константа. В каждый метод передается соединение для экономии транзакций

#TODO: курсор создается в каждом методе
conn = sqlite3.connect('flashcards.db')
cursor = conn.cursor()

# Создаем таблицу пользователей
#TODO: user_id, user_name, группы принадлежащие юзеру: список, словарь, кортеж: названия или id
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE
    )
''')

# Создаем таблицу групп
#TODO: как здесь передается связь из групп в коллекции?
cursor.execute('''
    CREATE TABLE IF NOT EXISTS groups (
        group_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        name TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
''')

# Создаем таблицу сетов (коллекций)
#TODO: как здесь передается связь из коллекций в пары?
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sets (
        set_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        group_id INTEGER,
        name TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (user_id),
        FOREIGN KEY (group_id) REFERENCES groups (group_id)
    )
''')

# Создаем таблицу карточек
#TODO: как по тз: объект 1, тип данных, обхект 2, тип данных
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cards (
        card_id INTEGER PRIMARY KEY,
        set_id INTEGER,
        word TEXT NOT NULL,
        translation TEXT NOT NULL,
        FOREIGN KEY (set_id) REFERENCES sets (set_id)
    )
''')

# Вставляем пример данных
cursor.executemany('''
    INSERT OR IGNORE INTO users (username) VALUES (?)
''', [('user1',), ('user2',)])

cursor.executemany('''
    INSERT OR IGNORE INTO groups (user_id, name) VALUES (?, ?)
''', [(1, 'Group1'), (2, 'Group2')])

cursor.executemany('''
    INSERT OR IGNORE INTO sets (user_id, group_id, name) VALUES (?, ?, ?)
''', [
    (1, 1, 'Set1'),
    (1, 1, 'Set2'),
    (1, 2, 'Set3'),
    (2, 2, 'Set4'),
])

cursor.executemany('''
    INSERT OR IGNORE INTO cards (set_id, word, translation) VALUES (?, ?, ?)
''', [
    (1, 'Word1', 'Translation1'),
    (1, 'Word2', 'Translation2'),
    (2, 'Word3', 'Translation3'),
    (3, 'Word4', 'Translation4'),
    (4, 'Word5', 'Translation5'),
])

# Сохраняем изменения
conn.commit()

# Закрываем соединение
conn.close()
