#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio
import index
import page
import user

route = [
    (r'/',index.IndexHandler),
    (r'/blank',index.BlankHandler),
    (r'/sample',index.SampleHandler),
    (r'/user/login',user.LoginHandler),
    (r'/user/logout',user.LogoutHandler),
    (r'/page/404.html',page.Page404Handler),
    (r'/page/500.html',page.Page500Handler),
    (r'/page/error.html',page.PageErrorHandler),
    (r'/page/blank.html',page.BlankHandler),
]