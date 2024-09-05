from pydantic import BaseModel, EmailStr
from typing import Optional, List

class CountryModel(BaseModel):
    id: int
    name: Optional[str] = None
    iso3: Optional[str] = None
    iso2: Optional[str] = None
    numeric_code: Optional[int] = None
    phone_code: Optional[int] = None
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