#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio
# Domain Page

from BaseHandler import BaseHandler
from tornado.web import authenticated as Auth


class IndexHandler(BaseHandler):
    @Auth
    def get(self):
        self.render('domain/index.html')


class GroupHandler(BaseHandler):
    @Auth
    def get(self):
        self.render('domain/group.html')


class RecordHandler(BaseHandler):
    @Auth
    def get(self):
        self.render('domain/record.html')
