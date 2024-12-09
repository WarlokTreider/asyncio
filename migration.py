import asyncpg
import asyncio

async def create_table():
    conn = await asyncpg.connect(
        user='postgres',
        password='postgres',
        database='swapi_characters_db',
        host='localhost'
    )
    await conn.execute()
    print("Table 'characters' created successfully.")
    await conn.close()

if __name__ == '__main__':
    asyncio.run(create_table())
