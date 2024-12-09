import asyncio
import aiohttp
import asyncpg

DB_CONFIG = {
    "user": "postgres",
    "password": "postgres",
    "database": "swapi_characters_db",
    "host": "localhost"
}

BASE_URL = "https://swapi.dev/api/people/"


async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Failed to fetch data from {url}: {response.status}")
                return None


async def fetch_all_characters():
    characters = []
    url = BASE_URL

    while url:
        data = await fetch_data(url)
        if data:
            characters.extend(data['results'])
            url = data.get('next')
        else:
            url = None

    return characters


async def fetch_details(urls, key_name):
    details = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    details.append(data.get(key_name, ""))
    return ", ".join(details)


async def process_character(character):
    films = await fetch_details(character["films"], "title")
    species = await fetch_details(character["species"], "name")
    starships = await fetch_details(character["starships"], "name")
    vehicles = await fetch_details(character["vehicles"], "name")
    homeworld = await fetch_data(character["homeworld"])
    homeworld_name = homeworld.get("name") if homeworld else ""

    return {
        "id": int(character["url"].split("/")[-2]),
        "birth_year": character["birth_year"],
        "eye_color": character["eye_color"],
        "films": films,
        "gender": character["gender"],
        "hair_color": character["hair_color"],
        "height": character["height"],
        "homeworld": homeworld_name,
        "mass": character["mass"],
        "name": character["name"],
        "skin_color": character["skin_color"],
        "species": species,
        "starships": starships,
        "vehicles": vehicles,
    }


async def save_characters_to_db(characters):
    conn = await asyncpg.connect(**DB_CONFIG)
    async with conn.transaction():
        for char in characters:
            await conn.execute(
                char["id"], char["birth_year"], char["eye_color"], char["films"], char["gender"],
                char["hair_color"], char["height"], char["homeworld"], char["mass"], char["name"],
                char["skin_color"], char["species"], char["starships"], char["vehicles"])
    await conn.close()


async def main():
    print("Fetching characters...")
    raw_characters = await fetch_all_characters()

    print("Processing characters...")
    tasks = [process_character(character) for character in raw_characters]
    characters = await asyncio.gather(*tasks)

    print("Saving characters to database...")
    await save_characters_to_db(characters)
    print("All characters saved successfully.")


if __name__ == '__main__':
    asyncio.run(main())
