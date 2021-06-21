import os
from dotenv import load_dotenv
from utils import connect

load_dotenv()

def init_env():
  """
  Creates a new sqlite database where we can store the fetched data,
  as well as the tables that are needed to store the information.
  """
  conn = create_database()
  create_tables(conn)

def create_database():
  print('Creating database')
  database_dir = os.environ.get("DATABASE_LOCATION")
  conn = connect(database_dir)
  return conn

def create_tables(con):
  print('Generating tables')
  q='''CREATE TABLE "temperatures" (
  "time" TIMESTAMP,
  "tavg" REAL,
  "tmin" REAL,
  "tmax" REAL,
  "prcp" REAL,
  "snow" REAL,
  "wdir" REAL,
  "wspd" REAL,
  "wpgt" REAL,
  "pres" REAL,
  "tsun" REAL,
  "place" TEXT
)'''
  cur = con.cursor()
  cur.execute(q)
  con.commit()
  con.close()

if __name__ == '__main__':
  init_env()