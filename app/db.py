#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio

import redis as PyRedis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

class DB:

    def __init__(self,host='localhost',port=3306,db='mysql',user='root',passwd='',charset='utf-8'):
        db_uri = 'mysql+mysqldb://%s:%s@%s:%s/%s?charset=%s' % (user,passwd,host,port,db,charset)
        self.session = self.create_session(db_uri,charset)


    def create_session(self,db_uri,encoding='utf-8'):
        engine = create_engine(db_uri, encoding=encoding, echo=False, pool_recycle=60)
        return scoped_session(sessionmaker(bind=engine, autocommit=False))


    def close(self):
        if self.session:
            self.session.remove()

# Wrapper Redis
class Redis():

    def __init__(self,host,port=6379,db=0,password=''):
        self._host = host
        self._port = port
        self._db = db
        self._password = password

    def Connect(self):
        return PyRedis.Redis(self._host, self._port, self._db, self._password)