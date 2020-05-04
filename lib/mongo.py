import logging
import pymongo
import settings


class Proxy(object):
  _db = None
  def __getattr__(self, name):
    if Proxy._db == None:
      connection = pymongo.MongoClient(settings.get("mongodb_url"))
      Proxy._db = connection[settings.get("db_name")]
    return getattr(self._db, name)

db = Proxy()