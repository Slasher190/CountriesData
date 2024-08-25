from Model.LocationModel import CountriesCollection, StatesCollection, CitiesCollection, CountryModel, StateModel, CityModel
from database import countries_collection, states_collection, cities_collection
from typing import List
from fastapi import HTTPException

async def get_all_countries():
    """
    Retrieve all countries from the database.
    """
    countries = await countries_collection.find().to_list(None)
    if not countries:
        raise HTTPException(status_code=404, detail="No countries found")
    
    # for country in countries:
    #     if isinstance(country.get("timezones"), str):
    #         try:
    #             country["timezones"] = json.loads(country["timezones"])
    #         except:
    #             country["timezones"] = []
    #             raise
    
    return CountriesCollection(countries=countries)

async def get_states_by_country(country_identifier: str):
    """
    Retrieve states for a given country ID or code.
    """
    if country_identifier.isdigit():
        matching_states = states_collection.find({"country_id": int(country_identifier)})
    else:
        matching_states = states_collection.find({"country_code": country_identifier})
    
    states = await matching_states.to_list(length=1000)
    if not states:
        raise HTTPException(status_code=404, detail="No states found")
    
    return StatesCollection(states=states)

async def get_cities_by_state(state_identifier: str):
    """
    Retrieve cities for a given state ID or code.
    """
    if state_identifier.isdigit():
        matching_cities = cities_collection.find({"state_id": int(state_identifier)})
    else:
        matching_cities = cities_collection.find({"state_code": state_identifier})
    
    cities = await matching_cities.to_list(length=1000)
    if not cities:
        raise HTTPException(status_code=404, detail="No cities found")
    
    return CitiesCollection(cities=cities)

async def get_countries_by_ids(ids: List[int]) -> CountriesCollection:
    countries: List[CountryModel] = []
    if (len(ids)):
        countries = await countries_collection.find({"id": {"$in": ids}}).to_list(length=len(ids))
    if not countries:
        raise HTTPException(status_code=404, detail="No countries found")
    
    return CountriesCollection(countries = countries)

async def get_states_by_ids(ids: List[int]) -> StatesCollection:
    states: List[StateModel] = []
    if (len(ids)):
        states = await states_collection.find({"id": {"$in": ids}}).to_list(length=len(ids))
        print(states)
    if not states:
        raise HTTPException(status_code=404, detail="No states found")
    return StatesCollection(states=states)

async def get_cities_by_ids(ids: List[int]) -> CitiesCollection:
    print(ids, "ids")
    cities: List[CityModel] = []
    if (len(ids)):
        cities = await cities_collection.find({"id": {"$in": ids}}).to_list(length=len(ids))
    
    if not cities:
        raise HTTPException(status_code=404, detail="No cities found")
    
    return CitiesCollection(cities=cities)