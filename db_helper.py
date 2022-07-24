from replit.database.database import ObservedList, ObservedDict
from replit import db
import json
class db_raw(object):
  def __getitem__(self, key):
    return json.loads(db.get_raw(key)) if type(db[key]) == ObservedList or type(db[key]) == ObservedDict else db[key]
db_raw = db_raw()
def all(key):
  try:
    return list(db_raw[key].values())
  except:
    return db_raw[key]
def one(key):
  return db_raw["advice"][key]
