import logging
import pymongo
import settings


class Proxy(object):
  _db = None
  def __getattr__(self, name):
    if Proxy._db == None:
      connection = pymongo.MongoClient(settings.get("DB_URI"))
      Proxy._db = connection[settings.get("DB_NAME")]
    return getattr(self._db, name)

db = Proxy()