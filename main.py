from fastapi import FastAPI
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
import numpy as np
from pydantic import BaseModel, EmailStr
from pydantic.functional_validators import BeforeValidator
from typing import Optional, List
import pandas as pd
from contextlib import asynccontextmanager

from typing_extensions import Annotated
import motor.motor_asyncio

load_dotenv()
USE_LIFESPAN = True

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])

db = client.my_data

countries_collection = db.get_collection("countries")
states_collection = db.get_collection("states")
cities_collection = db.get_collection("cities")

student_collection = db.get_collection("students")

PyObjectId = Annotated[str, BeforeValidator(str)]

def preprocess_data(df):
    df = df.replace({np.nan: None})
    return df

async def load_data():
    url_countries = 'https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/csv/countries.csv'
    url_states = 'https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/csv/states.csv'
    url_cities = 'https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/csv/cities.csv'

    countries = pd.read_csv(url_countries)
    states = pd.read_csv(url_states)
    cities = pd.read_csv(url_cities)

    # def parse_timezones(timezone_str):
    #     if isinstance(timezone_str, str):
    #         try:
    #             json_str = timezone_str.replace("'", '"')
    #             return json.loads(json_str)
    #         except (json.JSONDecodeError, TypeError):
    #             return []
    #     else:
    #         return []
    # countries['timezones'] = countries['timezones'].apply(parse_timezones)

    countries = countries.drop(columns=['timezones'])
    
    countries = preprocess_data(countries)
    states = preprocess_data(states)
    cities = preprocess_data(cities)
    
    countries_count = await countries_collection.count_documents({})
    state_count = await states_collection.count_documents({})
    cities_count = await cities_collection.count_documents({})

    if countries_count == 0:
        countries_collection.insert_many(countries.to_dict('records'))
    
    if state_count == 0:
        states_collection.insert_many(states.to_dict('records'))

    if cities_count == 0:
        cities_collection.insert_many(cities.to_dict('records'))

@asynccontextmanager
async def lifespan(app: FastAPI):
    await load_data()
    yield

app = FastAPI(lifespan=lifespan if USE_LIFESPAN else None)


# Models
class CountryModel(BaseModel):
    id: int
    name: Optional[str] = None
    iso3: Optional[str] = None
    iso2: Optional[str] = None
    numeric_code: Optional[int] = None
    phone_code: Optional[str] = None
    capital: Optional[str] = None
    currency: Optional[str] = None
    currency_name: Optional[str] = None
    currency_symbol: Optional[str] = None
    tld: Optional[str] = None
    native: Optional[str] = None
    region: Optional[str] = None
    region_id: Optional[int] = None
    subregion: Optional[str] = None
    subregion_id: Optional[int] = None
    nationality: Optional[str] = None
    # timezones: Optional[List[Dict]] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    emoji: Optional[str] = None
    emojiU: Optional[str] = None

class StateModel(BaseModel):
    id: int
    name: Optional[str] = None
    country_id: Optional[int] = None
    country_code: Optional[str] = None
    country_name: Optional[str] = None
    state_code: Optional[str] = None
    type: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class CityModel(BaseModel):
    id: int
    name: Optional[str] = None
    state_id: Optional[int] = None
    state_code: Optional[str] = None
    state_name: Optional[str] = None
    country_id: Optional[int] = None
    country_code: Optional[str] = None
    country_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    wikiDataId: Optional[str] = None

class StatesCollection(BaseModel):
    states: List[StateModel]

class CitiesCollection(BaseModel):
    cities: List[CityModel]

class CountriesCollection(BaseModel):
    countries: List[CountryModel]

@app.get("/countries", response_description="Get all countries", response_model=CountriesCollection)
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

@app.get("/states/{country_identifier}", response_description="Get states by country code or ID", response_model=StatesCollection)
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

@app.get("/cities/{state_identifier}", response_description="Get cities by state code or ID", response_model=CitiesCollection)
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