import requests
import os
import json
import pandas as pd
from sqlalchemy import create_engine
import pymysql 
from supabase import create_client, Client

def get_ev_chargers(_api_key, ret_amount):
    req_url = "https://developer.nrel.gov/api/alt-fuel-stations/v1.json?api_key={}&status=E&fuel_type=ELEC&ev_network=Tesla&limit={}".format(_api_key, ret_amount)
    response = requests.get(req_url)
    response = json.loads(response.content)
    df = pd.DataFrame(response['fuel_stations'])
    df = df[['station_name',"date_last_confirmed", "latitude", "longitude"]]
    
    return df


url = "https://ocjstgtyfmhoyljgqiyh.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9janN0Z3R5Zm1ob3lsamdxaXloIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTI3MDY4OTUsImV4cCI6MjAyODI4Mjg5NX0.232HXiB_S2y8hKjZYH-ogk6u2g8rVmdFZCgQk23IWnM"
supabase: Client = create_client(url, key)

api_key = os.getenv("NREL_API_KEY")


ev_chargers = get_ev_chargers(api_key, 100)

for i, val in ev_chargers.iterrows():
    
    val = val.to_dict()
    data, count = supabase.table('DIM_CHARGERS_T').insert(val).execute()

