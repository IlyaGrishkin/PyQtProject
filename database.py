import sqlite3
from random import sample

RUSSIAN_TOPICS = {
    'stress': 'Ударения',
    'ударения': 'stress',
    'наречия': 'adverb',
    'adverb': 'Наречия',
}


def create_database():
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stress
    (
        word_id INTEGER PRIMARY KEY,
        word TEXT,
        is_rigth boolean  
    )  """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attempts
        (
            attempt_id INTEGER PRIMARY KEY,
            result TEXT,
            topic TEXT,
            mistakes TEXT  
        )  """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS adverb
        (
            word_id INTEGER PRIMARY KEY,
            word TEXT,
            fused boolean
                
        )  """)
    conn.commit()


def count_rows(db_name):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(
        f'SELECT Count(*) FROM {db_name}'
    )
    data = cursor.fetchall()
    conn.commit()
    return int(data[0][0])




def add_new_stress(word, is_rigth):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(
        f'INSERT INTO stress (word, is_rigth) VALUES {(word, is_rigth)}'
    )
    conn.commit()


def get_stress(n):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    nums = sample(range(1, count_rows('stress') + 1), n)
    cursor.execute(f"SELECT word, is_rigth FROM stress WHERE word_id IN {tuple(nums)}")
    data = cursor.fetchall()
    conn.commit()
    return data


def get_adverb(n):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    nums = sample(range(1, count_rows('adverb') + 1), n)
    cursor.execute(f"SELECT word, fused FROM adverb WHERE word_id IN {tuple(nums)}")
    data = cursor.fetchall()
    conn.commit()
    return data


def add_new_attempt(result: str, topic, mistakes):
    topic = RUSSIAN_TOPICS[topic]
    mistakes = ';'.join(mistakes)
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(
        f'INSERT INTO attempts (result, topic, mistakes) VALUES {(result, topic, mistakes)}'
    )
    conn.commit()


def get_attempts():
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(
        """
         SELECT result, topic FROM attempts
         
         """
    )
    data = cursor.fetchall()
    conn.commit()
    return data



