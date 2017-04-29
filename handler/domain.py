#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio
# Domain Page

from BaseHandler import BaseHandler
from tornado.web import authenticated as Auth
from model.models import Domain, Groups, Record


class IndexHandler(BaseHandler):
    @Auth
    def get(self):
        page = int(self.get_argument('page', 1))
        line = int(self.get_argument('line', 20))
        offset = (page - 1) * line
        data = self.db.query(Domain).offset(offset).limit(line).all()
        self.render('domain/index.html',data=data)


class GroupHandler(BaseHandler):
    @Auth
    def get(self):
        self.render('domain/group.html')


class RecordHandler(BaseHandler):
    @Auth
    def get(self):
        self.render('domain/record.html')
