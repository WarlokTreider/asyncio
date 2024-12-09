import asyncpg
import asyncio

async def create_table():
    conn = await asyncpg.connect(
        user='postgres',
        password='postgres',
        database='swapi_characters_db',
        host='localhost'
    )
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS characters (
            id SERIAL PRIMARY KEY,
            birth_year TEXT,
            eye_color TEXT,
            films TEXT,
            gender TEXT,
            hair_color TEXT,
            height TEXT,
            homeworld TEXT,
            mass TEXT,
            name TEXT,
            skin_color TEXT,
            species TEXT,
            starships TEXT,
            vehicles TEXT
        );
    """)
    print("Table 'characters' created successfully.")
    await conn.close()

if __name__ == '__main__':
    asyncio.run(create_table())
