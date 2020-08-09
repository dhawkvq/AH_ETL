from helpers import state_iso_code, createFields
import pgeocode 

def create_location(cursor,location):

  zip_code = location['zip']
  firebase_id = location['propertyOwnerUid']
  # using pgeocode to grab lat and long based on zip.
  info = pgeocode.Nominatim('US').query_postal_code(zip_code)

  new_location = {
    'iso_3166_2': state_iso_code(location['state']),
    'postal_code': zip_code,
    'locality': None,
    'street': createFields(location,'address'),
    'num': None,
    'line_02': None,
    'latitude': float(info['latitude']) if 'latitude' in info else None, 
    'longitude': float(info['longitude']) if 'longitude' in info else None,
  }
  
  cursor.execute("""
    INSERT INTO location (iso_3166_2, postal_code, locality, street, num, line_02, latitude, longitude)
    VALUES (%(iso_3166_2)s,%(postal_code)s,%(locality)s,%(street)s,%(num)s,%(line_02)s,%(latitude)s,%(longitude)s)
    RETURNING id;
    """,
    new_location
  )
  # grabbing id from execute to place on property
  (location_id,) = cursor.fetchone()

  cursor.execute('SELECT id from account WHERE firebase_id = %s', (firebase_id,))
  # grabbing account id to set managing_account id when inserting property
  (managing_account,) = cursor.fetchone()

  return [location_id, managing_account]