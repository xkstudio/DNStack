#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio

from BaseHandler import BaseHandler
from tornado.web import authenticated as Auth
from model.models import Options

class StateHandler(BaseHandler):

    @Auth
    def get(self):
        self.nav_active['/system/state'] = 'active'
        self.render('system/state.html')


class SettingsHandler(BaseHandler):

    @Auth
    def get(self):
        self.nav_active['/settings'] = 'active'
        self.render('system/settings.html')

