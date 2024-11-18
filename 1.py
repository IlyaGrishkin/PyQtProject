import sqlite3

conn = sqlite3.connect('db.db')
cursor = conn.cursor()


with open(r"C:\Users\ilagr\OneDrive\Desktop\adverb_fused.txt", encoding='utf-8') as file:
    for line in file:
        word = line.strip()
        cursor.execute(
            f'INSERT INTO adverb (word, fused) VALUES {(word, True)}'
        )
    conn.commit()
