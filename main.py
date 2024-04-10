import requests
import os
import json
import pandas as pd
from sqlalchemy import create_engine
import pymysql 

user_name = "dev1"
pw = os.getenv("local_db_pw")

conn = create_engine("mysql+pymysql://{}:{}@localhost/database1".format(user_name, pw))



pd.set_option('display.max_columns', 500)

api_key = os.getenv("NREL_API_KEY")

def get_ev_chargers(_api_key, ret_amount):
    req_url = "https://developer.nrel.gov/api/alt-fuel-stations/v1.json?api_key={}&status=E&fuel_type=ELEC&ev_network=Tesla&limit={}".format(_api_key, ret_amount)
    response = requests.get(req_url)
    response = json.loads(response.content)
    df = pd.DataFrame(response['fuel_stations'])
    df = df[['station_name',"date_last_confirmed", "latitude", "longitude"]]
    return df

ev_chargers = get_ev_chargers(api_key, 100)


# FOR SQL SERVER MANAGEMENT STUDIO - 
ev_chargers.to_sql("EV_Charger", con=conn,if_exists="replace")
