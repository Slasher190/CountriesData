from fastapi import APIRouter
from Controller.LocationController import get_all_countries, get_cities_by_ids, get_cities_by_state, get_countries_by_ids, get_states_by_country, get_states_by_ids
from Model.LocationModel import CountriesCollection, StatesCollection, CitiesCollection
from typing import List

router = APIRouter()

@router.get("/countries", response_description="Get all countries", response_model=CountriesCollection)
async def route_get_all_countries():
    return await get_all_countries()

@router.post("/getCountriesByIds", response_description="Get countries by List of Id's", response_model=CountriesCollection)
async def route_get_countries_by_ids(ids: List[int]):
    return await get_countries_by_ids(ids)

@router.get("/states/{country_identifier}", response_description="Get states by country code or ID", response_model=StatesCollection)
async def route_get_states_by_country(country_identifier: str):
    return await get_states_by_country(country_identifier)

@router.post("/getStatesByIds", response_description="Get states by List of Id's", response_model=StatesCollection)
async def route_get_states_by_ids(ids: List[int]):
    return await get_states_by_ids(ids)

@router.get("/cities/{state_identifier}", response_description="Get cities by state code or ID", response_model=CitiesCollection)
async def route_get_cities_by_state(state_identifier: str):
    return await get_cities_by_state(state_identifier)

@router.post("/getCitiesByIds", response_description="Get cities by List of Id's", response_model=CitiesCollection)
async def route_get_cities_by_ids(ids: List[int]):
    return await get_cities_by_ids(ids)