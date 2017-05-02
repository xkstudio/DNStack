#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio

from BaseHandler import BaseHandler
from tornado.web import authenticated as Auth


class StatusHandler(BaseHandler):

    @Auth
    def get(self):
        return self.jsonReturn({'code': 0, 'msg': 'Success'})


class ReloadHandler(BaseHandler):
    @Auth
    def get(self):
        return self.jsonReturn({'code': 0, 'msg': 'Success'})


class ReconfigHandler(BaseHandler):
    @Auth
    def get(self):
        return self.jsonReturn({'code': 0, 'msg': 'Success'})

