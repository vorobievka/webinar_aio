import aiohttp
import asyncio
import datetime
from models import init_orm, People, Session
from more_itertools import chunked


MAX_CHUNK = 10
LIST_ATTR = ['birth_year', 'eye_color', 'films', 'gender', 'hair_color', 'height', 'homeworld', 'mass', 'name',
             'skin_color', 'species', 'starships', 'vehicles']


async def get_people(person_id, session):
    async with session.get(f"https://swapi.py4e.com/api/people/{person_id}") as response:
        json_data = await response.json()
        return json_data


async def get_people_detail(url):
    session = aiohttp.ClientSession()
    async with session.get(url) as response:
        json_data_detail = await response.json()
        await session.close()
        return json_data_detail


async def insert_people(list_people_dict):
    async with Session() as session:
        orm_objects = [People(birth_year=people_dict['birth_year'],
                              eye_color=people_dict['eye_color'],
                              films=people_dict['films'],
                              gender=people_dict['gender'],
                              hair_color=people_dict['hair_color'],
                              height=people_dict['height'],
                              homeworld=people_dict['homeworld'],
                              mass=people_dict['mass'],
                              name=people_dict['name'],
                              skin_color=people_dict['skin_color'],
                              species=people_dict['species'],
                              starships=people_dict['starships'],
                              vehicles=people_dict['vehicles']) for people_dict
                       in list_people_dict]
        session.add_all(orm_objects)
        await session.commit()


async def main():
    await init_orm()
    async with aiohttp.ClientSession() as session:
        people_ids = chunked(range(1, 101), MAX_CHUNK)
        for people_ids_chunk in people_ids:
            coros = [get_people(people_id, session) for people_id in people_ids_chunk]
            results_list_dict = []

            results = await asyncio.gather(*coros)
            for swapi_person in results:
                swapi_dict = {}
                detail_string = ''
                for item in LIST_ATTR:
                    if swapi_person.get(item) is None:
                        break
                    if item == 'films':
                        detail_string = ''
                        for film_url in swapi_person.get(item):
                            film_json = await get_people_detail(film_url)
                            film_title = film_json['title']
                            detail_string = detail_string + film_title + ', '
                        swapi_dict[item] = detail_string[0:-2]
                    elif item == 'homeworld':
                        homeworld_json = await get_people_detail(swapi_person.get(item))
                        homeworld_name = homeworld_json['name']
                        swapi_dict[item] = homeworld_name
                    elif item == 'species':
                        detail_string = ''
                        for species_url in swapi_person.get(item):
                            species_json = await get_people_detail(species_url)
                            species_title = species_json['name']
                            detail_string = detail_string + species_title + ', '
                        swapi_dict[item] = detail_string[0:-2]
                    elif item == 'starships':
                        detail_string = ''
                        for starships_url in swapi_person.get(item):
                            starships_json = await get_people_detail(starships_url)
                            starships_title = starships_json['name']
                            detail_string = detail_string + starships_title + ', '
                        swapi_dict[item] = detail_string[0:-2]
                    elif item == 'vehicles':
                        detail_string = ''
                        for vehicles_url in swapi_person.get(item):
                            vehicles_json = await get_people_detail(vehicles_url)
                            vehicles_title = vehicles_json['name']
                            detail_string = detail_string + vehicles_title + ', '
                        swapi_dict[item] = detail_string[0:-2]
                    else:
                        swapi_dict[item] = swapi_person[item]
                if swapi_dict != {}:
                    results_list_dict.append(swapi_dict)
                else:
                    break
            print(results_list_dict)
            insert_task = asyncio.create_task(insert_people(results_list_dict))

        main_task = asyncio.current_task()
        current_task = asyncio.all_tasks()
        current_task.remove(main_task)
        await asyncio.gather(*current_task)

    print("Finished")
    
start = datetime.datetime.now()
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
print(datetime.datetime.now() - start)
