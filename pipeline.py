from src.data import utils
from datetime import datetime

def pipeline(place, start, end):
  """
  Pipeline is defined in this functions, performs all the steps in order, 
  if is needed the individual functions can be used outside this scope
  to automate each step with a different method
  Parameters:
  Place (string): Name of the city or the address of
  the place where we want to obtain the data.
  start (datetime): Date from wich we want to obtain data.
  end (datetime): End date to retreive data.
  """  
  # Fetch information returns a dataframe with the data queried,
  # if file storage is needed it can be done with that object
  # this function is not optimized for large file consumption
  # but it could be implemented
  print('Getting information')
  data = utils.get_data(place, start, end)

  # Store data just recieves the dataframe and upserts it into 
  # the database
  print('Storing data')
  utils.store_data(data)

  # Execute analysis functions, this functions shold be more 
  # flexible than the rest of the pipeline since any of this
  # functions should be able to execute its codeseparated when
  # scheduled
  print('Performing Analysis')
  utils.month_avg_analysis()

# Calls the pipeline with historical parameters
def process_historic_data(place,start=datetime(1931, 1, 1),end=None):
  pipeline(place,start,end)

# Calls the pipeline with daily parameters
def process_daily_data(place):
  pipeline(place)

if __name__ == '__main__':
  process_historic_data('Berlin / Tegel',datetime(1931, 1, 1))
  