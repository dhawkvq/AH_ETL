import json, sys
from psycopg2 import Error
import datetime
from helpers import format_dates, createFields, connect_db
from create_users import create_user
from create_locations import create_location
from create_property import create_property
from create_reservation import create_reservation



conn = connect_db()
cursor = conn.cursor()


def commit():

  try:
    conn.commit()

  except (Exception, Error) as err:
    print ("\npsycopg2 connect error:", err)

# Create users first to have access to user id 
# for foreign key restraint on 

print('***** CREATING USERS *****\n\n')
with open('./6-25-2020-ah-prod-users.json') as json_data:

  user_dict = json.load(json_data)
  for *_,user in user_dict.items():
    create_user(cursor,user)

  commit()

print('***** FINISHED CREATING USERS *****\n\n')
print('***** CREATING LOCATIONS AND PROPERTIES *****\n\n')
# Create locations and property tables for access to id's 
# needed for foreign key restraints on reservations
with open('./6-25-2020-prod-props-db.json') as prop_data:

  location_dict = json.load(prop_data)

  for firebase_id,location in location_dict.items():

    location_id, managing_account = create_location(cursor,location)

    location['firebase_id'] = firebase_id
    location['location_id'] = location_id
    location['managing_account'] = managing_account

    create_property(cursor,location)

  commit()


print('***** FINISHED CREATING LOCATIONS AND PROPERTIES *****\n\n')
print('***** CREATING RESERVATIONS *****\n\n')
# Create reservations
with open('./6-25-2020-ah-prod-users.json') as json_data:

  user_dict = json.load(json_data)

  for *_,user in user_dict.items():

    if 'reservations' in user:
      for *__,res in user['reservations'].items():

        cursor.execute('SELECT id from account WHERE firebase_id = %s', (user['uid'],))
        # grabbing account id to set account foreign key restraint in reservation
        user_account = cursor.fetchone()
        if(user_account):

          res['user_account_id'] = user_account

          create_reservation(cursor,res)

        else:
          with open('logs/no_user.txt', 'w') as no_user:
            no_user.write('\n')
            no_user.write(json.dumps(user))

  commit()

print('***** FINISHED CREATING RESERVATIONS *****\n\n')