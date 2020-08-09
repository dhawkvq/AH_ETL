from helpers import createFields


def create_property(cursor,prop):

  new_prop = {
    'firebase_id': prop['firebase_id'],
    'managing_account': prop['managing_account'],
    'location': prop['location_id'],
    'rate': createFields(prop,'price'),
    'acres': 1, #set to default one to meet constraint of not null
    'max_capacity': None,
    'validated_timestamp': None,
    'validated_memo': None
  }
  
  cursor.execute("""
    INSERT INTO property (firebase_id, managing_account, location, rate, acres, max_capacity, validated_timestamp, validated_memo)
    VALUES (%(firebase_id)s,%(managing_account)s,%(location)s,%(rate)s,%(acres)s,%(max_capacity)s,%(validated_timestamp)s,%(validated_memo)s);
    """,
    new_prop
  )

  return