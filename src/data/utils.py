import os
import sqlite3
import requests
import urllib.parse
import pandas as pd
from datetime import datetime, timedelta, date
from meteostat import Point, Daily

from dotenv import load_dotenv
load_dotenv()

def connect(database):
  """Connects to database
  
  Parameters:
  database (string): Directory of sqlite database

  Returns:
  conn: Connection Object
  """
  conn = sqlite3.connect(database)
  return conn

def default_date():
  yesterday = date.today() - timedelta(days=2)
  yesterday = datetime(yesterday.year, yesterday.month, yesterday.day)
  return yesterday

def get_coords(place):
  url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(place) +'?format=json'
  response = requests.get(url).json()
  # An empty array in the response is a search parameter not found
  # in this case a non existent city or address
  if len(response) == 0:
    raise Exception('City name not found')
  return [float(response[0]["lat"]), float(response[0]["lon"])]

def get_data(place, start=None, end=None):
  """
  Fetches data from Meteostat API
  
  Parameters:
  Place (string): Name of the city or the address of
  the place where we want to obtain the data.
  start (datetime): Date from wich we want to obtain data.
  end (datetime): End date to retreive data.

  Returns:
  data (Pandas DataFrame): Pandas DF containing the found
  information.
  """
  # If start date parameters are not passed, the default values
  # are taken for yesterdays date so only a day of data is 
  # retreived
  if(start == None):
    start = end = default_date()
  
  # If onlu the start date is passed but no end, the end date
  # becomes yesterdays date
  if(end == None):
    end = default_date()

  lat, lon = get_coords(place)

  # Meteostat object, more information related to this object 
  # can be found in the Meteostat documentation 
  # https://dev.meteostat.net/python/daily.html
  data = Daily(Point(lat,lon,70), start, end)
  data = data.fetch()
  data['place'] = place
  
  return data

def store_data(df):
  """
  Upserts the information in the database, tablenames are
  hardcoded
  
  Parameters:
  df (DataFrame): Data to be added.
  """
  # Connect to db
  conn = connect(os.environ.get("DATABASE_LOCATION"))

  # In this process we perform an upsert of data since we dont
  # want to have the same information multiple times

  # Writing temporal data
  df.to_sql('tmp',conn, if_exists='replace')

  # Getting cursor
  cur = conn.cursor()

  # Deleting existing data
  query = """DELETE FROM temperatures 
  WHERE (time, place) IN (SELECT time, place FROM tmp);"""
  cur.execute(query)
  conn.commit()
  
  # Appending new data
  query = "INSERT INTO temperatures SELECT * FROM tmp;"
  cur.execute(query)
  conn.commit()

  # Deleting temporal data
  query = "DROP TABLE tmp;"
  cur.execute(query)
  conn.commit()

  # Close Connection
  conn.close()

def month_avg_analysis(place='Berlin / Tegel',month='02', csv_output=True, csv_name='month_avg_analysis.csv',plot_data=True, plot_name='month_avg_plot.jpg'):
  query = f"""SELECT strftime('%Y',time) year,AVG(tavg) temp_avg
  FROM temperatures
  WHERE strftime('%m',time) = '{month}'
  AND place = '{place}'
  GROUP BY strftime('%Y',time);"""
  conn = connect(os.environ.get("DATABASE_LOCATION"))
  data = pd.read_sql(query, conn)

  if csv_output:
    data.to_csv(f'reports/{csv_name}', index=False)
  
  if plot_data:
    title = f'{place} average temperature per year for month {month}'
    data.plot(x='year', title=title, figsize=(20, 5)).get_figure().savefig(f'reports/{plot_name}')
  
