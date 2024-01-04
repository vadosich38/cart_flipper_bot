import sqlite3


class DBMethods:
    pass
## пример структуры DB. твое мнение?

# Создаем соединение с базой данных
conn = sqlite3.connect('flashcards.db')
cursor = conn.cursor()

# Создаем таблицу пользователей
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE
    )
''')

# Создаем таблицу групп
cursor.execute('''
    CREATE TABLE IF NOT EXISTS groups (
        group_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        name TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
''')

# Создаем таблицу сетов (коллекций)
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
