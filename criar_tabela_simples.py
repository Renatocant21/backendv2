import psycopg2

DATABASE_URL = "postgresql://bdpostgre_user:rEUaXS1U7eTg2qfub9jn34QIxZwJYEXh@dpg-d8eus2mrnols73ah57h0-a.ohio-postgres.render.com:5432/bdpostgre"

try:
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proprietario (
            id SERIAL PRIMARY KEY,
            "CPF" VARCHAR(11) UNIQUE NOT NULL,
            "Nome" VARCHAR(100) NOT NULL
        )
    """)
    
    print("✅ Tabela 'proprietario' criada com sucesso!")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Erro: {e}")