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


# 编辑域名
class UpdateDomainHandler(BaseHandler):
    @Auth
    def post(self):
        domain_id = self.get_argument('id',None)
        gid = self.get_argument('gid',None)
        comment = self.get_argument('comment',None)
        if not domain_id and not gid:
            return self.jsonReturn({'code': -1, 'msg': u'参数错误'})
        data = self.db.query(Domain).filter_by(id=domain_id).first()
        if not data:
            return self.jsonReturn({'code': -2, 'msg': u'域名不存在'})
        # Check Group ID
        group = self.db.query(Groups).filter_by(id=gid).first()
        if not group:
            return self.jsonReturn({'code': -3, 'msg': u'分组不存在'})
        self.db.query(Domain).filter_by(id=domain_id).update({'gid': gid, 'comment': comment, 'update_time': self.time})
        self.db.query(Groups).filter_by(id=data.gid).update({'domain_count': Groups.domain_count-1})
        self.db.query(Groups).filter_by(id=gid).update({'domain_count': Groups.domain_count+1})
        self.db.commit()
        return self.jsonReturn({'code': 0, 'msg': 'Success'})


# 域名状态管理
class StatusDomainHandler(BaseHandler):
    @Auth
    def post(self):
        status = self.get_argument('status',None) # 1 or 2
        id = self.get_argument('id',None)
        if not id and status not in ['1','2']:
            return self.jsonReturn({'code': -1, 'msg': u'参数错误'})
        data = self.db.query(Domain).filter_by(id=id).first()
        if not data:
            return self.jsonReturn({'code': -2, 'msg': u'域名不存在'})
        self.db.query(Domain).filter_by(id=id).update({'status': status, 'update_time': self.time})
        self.db.commit()
        return self.jsonReturn({'code': 0, 'msg': 'Success'})


# 删除域名：这里需要添加权限控制，风险操作！！！
class DeleteDomainHandler(BaseHandler):
    @Auth
    def post(self):
        id = self.get_argument('id',None)
        if not id:
            return self.jsonReturn({'code': -1, 'msg': u'参数错误'})
        data = self.db.query(Domain).filter_by(id=id).first()
        if not data:
            return self.jsonReturn({'code': -2, 'msg': u'域名不存在'})
        self.db.query(Domain).filter_by(id=id).delete() # 删除域名
        self.db.query(Record).filter_by(zone=data.zone).delete() # 删除解析记录
        self.db.query(Groups).filter_by(id=data.gid).update({'domain_count': Groups.domain_count - 1}) # 更新分组数据统计
        self.db.commit()
        return self.jsonReturn({'code': 0, 'msg': 'Success'})


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


# 新增记录
class CreateRecordHandler(BaseHandler):
    @Auth
    def post(self):
        host = self.get_argument('host', None)
        zone = self.get_argument('zone', None)
        type = self.get_argument('type', None)
        data = self.get_argument('data', None)
        ttl = self.get_argument('ttl')
        mx_priority = self.get_argument('mx_priority')
        comment = self.get_argument('comment')
        if not host or not zone or not type or not data:
            return self.jsonReturn({'code': -1, 'msg': u'参数错误'})
        type = type.upper()
        if type not in ['A','AAAA','MX','NS','CNAME','TXT','PTR']:
            return self.jsonReturn({'code': -1, 'msg': u'解析类型错误'})
        if host == '@' and type in ['NS','SOA']:
            return self.jsonReturn({'code': -2, 'msg': u'禁止添加该类型的解析'})
        domain = self.db.query(Domain).filter_by(zone=zone).first()
        if not domain:
            return self.jsonReturn({'code': -3, 'msg': u'域名不存在'})
        if not ttl: ttl = 600
        if not comment: comment = None
        if type in ['A','AAAA','NS','CNAME','TXT','PTR']:
            r = Record(host=host,zone=zone,type=type,data=data,ttl=ttl, comment=comment, create_time=self.time, update_time=self.time)
        else: # type = 'MX'
            if not mx_priority:
                mx_priority = 10
            r = Record(host=host, zone=zone, type=type, data=data, ttl=ttl, mx_priority=mx_priority, comment=comment, create_time=self.time,update_time=self.time)
        self.db.add(r)
        self.db.query(Domain).filter_by(id=domain.id).update({'record_count': Domain.record_count + 1}) # 更新记录统计
        self.db.commit()
        return self.jsonReturn({'code': 0, 'msg': 'Success'})


# 更新解析记录
class UpdateRecordHandler(BaseHandler):
    @Auth
    def post(self):
        id = self.get_argument('id', None)
        host = self.get_argument('host', None)
        zone = self.get_argument('zone', None)
        type = self.get_argument('type', None)
        data = self.get_argument('data', None)
        ttl = self.get_argument('ttl')
        mx_priority = self.get_argument('mx_priority')
        comment = self.get_argument('comment')
        if not id or not host or not zone or not type or not data:
            return self.jsonReturn({'code': -1, 'msg': u'参数错误'})
        type = type.upper()
        if type not in ['A','AAAA','MX','NS','CNAME','TXT','PTR']:
            return self.jsonReturn({'code': -2, 'msg': u'解析类型错误'})
        if host == '@' and type in ['NS','SOA']:
            return self.jsonReturn({'code': -3, 'msg': u'禁止添加该类型的解析'})
        domain = self.db.query(Domain).filter_by(zone=zone).first()
        if not domain:
            return self.jsonReturn({'code': -4, 'msg': u'域名不存在'})
        record = self.db.query(Record).filter_by(id=id).first()
        if not record:
            return self.jsonReturn({'code': -5, 'msg': u'无效解析'})
        if not ttl: ttl = 600
        if not comment: comment = None
        if type in ['A', 'AAAA', 'NS', 'CNAME', 'TXT', 'PTR']:
            self.db.query(Record).filter_by(id=id).update(
                {'host': host, 'type': type, 'data': data, 'ttl': ttl, 'comment': comment, 'update_time': self.time})
        else:
            if not mx_priority: mx_priority = 10
            self.db.query(Record).filter_by(id=id).update(
                {'host': host, 'type': type, 'data': data, 'ttl': ttl, 'mx_priority': mx_priority, 'comment': comment, 'update_time': self.time})
        self.db.commit()
        return self.jsonReturn({'code': 0, 'msg': 'Success'})


# 记录状态管理
class StatusRecordHandler(BaseHandler):
    @Auth
    def post(self):
        id = self.get_argument('id', None)
        status = self.get_argument('status',None) # 1 or 2
        if not id and status not in ['1','2']:
            return self.jsonReturn({'code': -1, 'msg': u'参数错误'})
        data = self.db.query(Record).filter_by(id=id).first()
        if not data:
            return self.jsonReturn({'code': -2, 'msg': u'解析不存在'})
        self.db.query(Record).filter_by(id=id).update({'status': status, 'update_time': self.time})
        self.db.commit()
        return self.jsonReturn({'code': 0, 'msg': 'Success'})


# 删除解析
class DeleteRecordHandler(BaseHandler):
    @Auth
    def post(self):
        id = self.get_argument('id',None)
        if not id:
            return self.jsonReturn({'code': -1, 'msg': u'参数错误'})
        data = self.db.query(Record).filter_by(id=id).first()
        if not data:
            return self.jsonReturn({'code': -2, 'msg': u'解析不存在'})
        self.db.query(Record).filter_by(id=id).delete() # 删除解析记录
        self.db.query(Domain).filter_by(zone=data.zone).update({'record_count': Domain.record_count - 1}) # 更新解析统计
        self.db.commit()
        return self.jsonReturn({'code': 0, 'msg': 'Success'})

