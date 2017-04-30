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
        data = self.db.query(Domain).order_by('id desc').offset(offset).limit(line).all()
        grps = self.db.query(Groups).all()
        group = {}
        for i in grps:
            group[i.id] = i.name
        status = {1:u'<span style="color:green">已启用</span>',2:u'<span style="color:red">暂停解析</span>'}
        self.render('domain/index.html',data=data,group=group,status=status)


class GroupHandler(BaseHandler):
    @Auth
    def get(self):
        data = self.db.query(Groups).order_by('id desc').all()
        self.render('domain/group.html',data=data)


class RecordHandler(BaseHandler):
    @Auth
    def get(self):
        zone = self.get_argument('zone')
        data = self.db.query(Record).filter_by(zone=zone).order_by(Record.host,Record.type,Record.data).all()
        status = {1: u'<span style="color:green">已启用</span>', 2: u'<span style="color:red">暂停解析</span>'}
        self.render('domain/record.html',data=data,status=status,zone=zone)
