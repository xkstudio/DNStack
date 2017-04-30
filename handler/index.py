#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio
# Index Page

from BaseHandler import BaseHandler
from tornado.web import authenticated as Auth
from model.models import Domain, Groups, Record, User

class IndexHandler(BaseHandler):

    @Auth
    def get(self):
        data = {}
        data['domain'] = self.db.query(Domain).count()
        data['group'] = self.db.query(Groups).count()
        data['record'] = self.db.query(Record).count()
        data['user'] = self.db.query(User).count()
        self.render('index/index.html',data=data)

class BlankHandler(BaseHandler):
    # @Auth
    def get(self):
        self.render('index/blank.html')


class SampleHandler(BaseHandler):
    # @Auth
    def get(self):
        self.render('index/sample.html')
