#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio
import index
import page
import user
import domain
import system

route = [
    (r'/',index.IndexHandler),
    (r'/blank',index.BlankHandler),
    (r'/sample',index.SampleHandler),
    (r'/user/login',user.LoginHandler),
    (r'/user/logout',user.LogoutHandler),
    (r'/user/profile',user.ProfileHandler),
    (r'/user/passwd',user.PasswdHandler),
    (r'/domain',domain.IndexHandler),
    (r'/domain/state',domain.StateDomainHandler),
    (r'/domain/create',domain.CreateDomainHandler),
    (r'/domain/update',domain.UpdateDomainHandler),
    (r'/domain/status',domain.StatusDomainHandler),
    (r'/domain/delete',domain.DeleteDomainHandler),
    (r'/domain/group',domain.GroupHandler),
    (r'/domain/record',domain.RecordHandler),
    (r'/domain/record/create',domain.CreateRecordHandler),
    (r'/domain/record/update',domain.UpdateRecordHandler),
    (r'/domain/record/status',domain.StatusRecordHandler),
    (r'/domain/record/delete',domain.DeleteRecordHandler),
    (r'/system/state',system.StateHandler),
    (r'/system/settings',system.SettingsHandler),
    (r'/page/404.html',page.Page404Handler),
    (r'/page/500.html',page.Page500Handler),
    (r'/page/error.html',page.PageErrorHandler),
    (r'/page/blank.html',page.BlankHandler),
]