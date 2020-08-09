import json
from helpers import createFields

def create_reservation(cursor,reservation):

  prop_key = reservation['propertyKey']

  res_start,res_end,price = createFields(reservation,'resDetails', reservation['userResDates'], reservation['price'])



  cursor.execute('SELECT id FROM property WHERE firebase_id = %s',(prop_key,))
  property_id = cursor.fetchone()
  if(property_id):

    formatted_res = {
      'state': createFields(reservation, 'state'),
      'account': reservation['user_account_id'], 
      'property': property_id[0],
      'rate': price,
      'timestamp_start': res_start,
      'timestamp_end': res_end,
    }

    cursor.execute("""
      INSERT INTO reservation (state, account, property, rate, timestamp_start, timestamp_end)
      VALUES (%(state)s,%(account)s,%(property)s,%(rate)s,%(timestamp_start)s,%(timestamp_end)s);
      """,
      formatted_res
    )


  else:
    with open('logs/create_reservation.txt', 'w') as failed_res:
      failed_res.write('\n')
      failed_res.write(json.dumps(reservation))

  return