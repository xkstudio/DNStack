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
        _data = self.db.query(Options).all()
        data = {}
        for i in _data:
            data[i.name] = {'id':i.id,'name':i.name,'value':i.value,'default':i.default_value}
        self.render('system/settings.html',data=data)

