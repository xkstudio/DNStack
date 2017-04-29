#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio

from sqlalchemy import Column, Integer, SmallInteger, VARCHAR, or_, and_
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True,autoincrement=True)
    username = Column(VARCHAR(32),nullable=False,unique=True)
    password = Column(VARCHAR(64),nullable=False)
    password_key = Column(VARCHAR(12),nullable=False,default='a1b2c3d4e5f6')
    email = Column(VARCHAR(32),nullable=False,unique=True)
    phone = Column(VARCHAR(32),nullable=True)
    nickname = Column(VARCHAR(32),nullable=True)
    gender = Column(SmallInteger,nullable=True) # 性别
    dept = Column(VARCHAR(32),nullable=True) # 部门
    role = Column(VARCHAR(32),nullable=True)
    lang = Column(VARCHAR(12),nullable=False,default='zh_CN')
    login_count = Column(Integer,nullable=False,default=0)
    login_time = Column(Integer,nullable=True)
    login_ua = Column(VARCHAR(600),nullable=True)
    login_ip = Column(VARCHAR(64),nullable=True)
    login_location = Column(VARCHAR(32),nullable=True)
    create_time = Column(Integer,nullable=True)
    update_time = Column(Integer,nullable=True)
    status = Column(SmallInteger,nullable=False,default=1)


class Domain(Base):
    __tablename__ = 'domain'

    id = Column(Integer,primary_key=True,autoincrement=True)
    zone = Column(VARCHAR(128),nullable=False,unique=True)
    gid = Column(Integer,nullable=True)
    comment = Column(VARCHAR(256), nullable=True)
    count = Column(Integer,nullable=False,default=0)
    create_time = Column(Integer,nullable=True)
    update_time = Column(Integer,nullable=True)
    status = Column(SmallInteger, nullable=False, default=1)


class Groups(Base):
    __tablename__ = 'groups'

    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(VARCHAR(128),nullable=False,unique=True)


class Record(Base):
    __tablename__ = 'record'

    id = Column(Integer,primary_key=True,autoincrement=True)
    zone = Column(VARCHAR(128), nullable=False)
    host = Column(VARCHAR(128), nullable=False)
    type = Column(VARCHAR(12), nullable=False)
    data = Column(VARCHAR(128), nullable=False)
    ttl = Column(Integer, nullable=False,default=600)
    mx_priority = Column(Integer, nullable=True)
    refresh = Column(Integer, nullable=True)
    retry = Column(Integer, nullable=True)
    expire = Column(Integer, nullable=True)
    minimum = Column(Integer, nullable=True)
    serial = Column(Integer, nullable=True)
    resp_person = Column(VARCHAR(64), nullable=True)
    primary_ns = Column(VARCHAR(64), nullable=True)
    comment = Column(VARCHAR(256), nullable=True)
    create_time = Column(Integer, nullable=True)
    update_time = Column(Integer, nullable=True)
    status = Column(SmallInteger, nullable=False, default=1)
