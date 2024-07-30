import psycopg2

conn = psycopg2.connect(database="pabd_flask", user="postgres", password="sql", host="localhost")

cursor = conn.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS Cadastro (usuario VARCHAR(30) NOT NULL,'
    'email VARCHAR(50) PRIMARY KEY,'
    'senha VARCHAR(20) NOT NULL);')

cursor.execute('CREATE TABLE IF NOT EXISTS Ficha_treino (dia VARCHAR(20) NOT NULL,'
    'treino VARCHAR(100));')

conn.commit()
cursor.close()
conn.close()