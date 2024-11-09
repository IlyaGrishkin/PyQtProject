from random import sample

import psycopg2

conn = psycopg2.connect(dbname='words', user='postgres', password='Uhbirf55', host='localhost')
cursor = conn.cursor()

nums = sample(range(1, 249), 10)

cursor.execute(f"SELECT word, is_rigth FROM stress WHERE word_id IN {tuple(nums)}")
data = cursor.fetchall()
conn.commit()
print(data)