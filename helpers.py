import json
import os
from dotenv import load_dotenv  
from datetime import datetime
from psycopg2 import connect
load_dotenv()


dev_db = os.environ['DEV_DB']
dev_host = os.environ['DEV_HOST']
dev_user = os.environ['DEV_USER']
dev_password = os.environ['DEV_PASSWORD']


def format_dates(dates):  
  reformed_dates = []
  for date in dates:
    if type(date) == int:
      year = 19
      julian_time = f'{year}{date}'
      # formatting Example: 'Sat Apr 04 2020 00:00:00'
      date = datetime.strptime(julian_time, '%y%j').date().strftime('%a %b %d %Y %H:%M:%S')
      reformed_dates.append(date)
    else:
      date = date.split('GMT')[0]
      reformed_dates.append(date)

  return reformed_dates


def createFields(obj,param,*args):

  value = obj[param] if param in obj else None

  if param == 'profilePhoto':
    return json.dumps(value) if 'photo' in value else None 

  if param == 'stripeBusinessInfo':
    # return two None values so business_id,stripe_user_info unpacking wont throw error
    if not value: return [None,None]
    # rename and remove livemode at the same time
    value['live_mode'] = value.pop('livemode')
    value['token_type'] = json.dumps(value['token_type'])
    
    return [ value['stripe_user_id'], value]

  if param == 'resDetails':
    resDates, price = args
    resDates = format_dates(resDates)

    if type(price) == int:
      formatted_price = price
    else:
      formatted_price = int(price.split('.')[0])

    return [ resDates[0], resDates.pop(), formatted_price ]


  if param == 'propertyPics':
    if not value: return None

    return [json.dumps(pic) for pic in value]

    

  if param == 'name':
    if value:
      # splitting name to check if entry has a middle initial, and then only returning first and last
      split_name = value.split()
      first_name = split_name[0]
      last_name = split_name.pop()
      return [first_name,last_name]
    
    return [None,None]

  if param == 'price':
    if type(value) == int: return value
    # splitting price on decimal if any contained in price string. 
    # going to return whole num for type int needed for rate on property
    split_price = value.split('.')
    return int(split_price[0])

  return value


def connect_db(config='local'):

  valid_config = config if config == 'dev' else None

  return connect(
    dbname = dev_db if valid_config else 'postgres',
    user = dev_user if valid_config else '',
    host = dev_host if valid_config else 'localhost',
    password = dev_password if valid_config else '',
    # attempt to connect for 3 seconds then raise exception
    connect_timeout = 3
  )


def state_iso_code(state):

  states = {
    'Arkansas' : 'US-AR',
    'Missouri' : 'US-MO',
    'Oklahoma' : 'US-OK'
  }

  return states[state]