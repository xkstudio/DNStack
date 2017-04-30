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
        data = self.db.query(Domain).order_by(Domain.id.desc()).offset(offset).limit(line).all()
        grps = self.db.query(Groups).all()
        group = {}
        for i in grps:
            group[i.id] = i.name
        status = {1:u'<span style="color:green">已启用</span>',2:u'<span style="color:red">暂停解析</span>'}
        self.nav_active['/domain'] = 'active'
        self.render('domain/index.html',data=data,group=group,status=status)


# 新增域名
class CreateDomainHandler(BaseHandler):
    @Auth
    def post(self):
        domain = self.get_argument('domain',None)
        gid = self.get_argument('gid',None)
        comment = self.get_argument('comment',None)
        if not domain and not gid:
            return self.jsonReturn({'code': -1, 'msg': u'参数错误'})
        chk = self.db.query(Domain).filter_by(zone=domain).first()
        if chk:
            return self.jsonReturn({'code': -2, 'msg': u'域名重复'})
        # Check Group ID
        grp = self.db.query(Groups).filter_by(id=gid).first()
        if not grp:
            return self.jsonReturn({'code': -3, 'msg': u'分组不存在'})
        d = Domain(zone=domain,gid=gid,comment=comment,create_time=self.time,update_time=self.time)
        self.db.add(d)
        self.db.commit()
        if d.id:
            self.db.query(Groups).filter_by(id=gid).update({'domain_count': Groups.domain_count+1})
            self.db.commit()
            code = 0
            msg = u'成功添加域名'
        else:
            self.db.rollback()
            gid = 0
            code = -4
            msg = u'保存域名失败'
        return self.jsonReturn({'code': code, 'msg': msg, 'gid': gid})



class GroupHandler(BaseHandler):
    @Auth
    def get(self):
        self.nav_active['/domain/group'] = 'active'
        data = self.db.query(Groups).order_by(Groups.id.desc()).all()
        self.render('domain/group.html',data=data)


class RecordHandler(BaseHandler):
    @Auth
    def get(self):
        zone = self.get_argument('zone',None)
        if zone:
            data = self.db.query(Record).filter_by(zone=zone).order_by(Record.host,Record.type,Record.data).all()
        else:
            zone = ''
            data = []
        status = {1: u'<span style="color:green">已启用</span>', 2: u'<span style="color:red">暂停解析</span>'}
        self.nav_active['/domain/record'] = 'active'
        self.render('domain/record.html',data=data,status=status,zone=zone)

