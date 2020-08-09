from helpers import createFields


def create_user(cursor,user_data):

  first_name,last_name = createFields(user_data,'name')

  new_user = {
    'firebase_id': createFields(user_data,'uid'),
    'handle': None,
    'name_first': first_name,
    'name_last': last_name,
    'type': None,
    'timestamp': createFields(user_data,'createdAT'), 
    'email': createFields(user_data,'email'),
    'email_validated_timestamp': None,
    'phone': None,
    'phone_validated_timestamp': None,
    'location': None
  }

  cursor.execute("""
    INSERT INTO account (firebase_id,handle,name_first, name_last, type, timestamp, email, email_validated_timestamp, phone, phone_validated_timestamp, location)
    VALUES (%(firebase_id)s,%(handle)s,%(name_first)s,%(name_last)s,%(type)s,%(timestamp)s,%(email)s,%(email_validated_timestamp)s,%(phone)s,%(phone_validated_timestamp)s,%(location)s);
    """,
    new_user
  )

  return 