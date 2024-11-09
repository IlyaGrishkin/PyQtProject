import psycopg2

conn = psycopg2.connect(dbname='words', user='postgres', password='Uhbirf55', host='localhost')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS public.stress
(
    word_id INT GENERATED ALWAYS AS IDENTITY,
    word text,
    is_rigth boolean  
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.stress
    OWNER to postgres;
    """
)
conn.commit()


