import motor.motor_asyncio
import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np

load_dotenv()

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])

db = client.my_data
print("Database is running at: ", os.environ["MONGODB_URL"])
countries_collection = db.get_collection("countries")
states_collection = db.get_collection("states")
cities_collection = db.get_collection("cities")

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