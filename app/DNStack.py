#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio

import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.netutil
import tornado.process
import tornado.locale
import platform
import db
from tornado.log import gen_log
from handler.page import Page404Handler
from config.settings import *
from handler import route
#from ui_modules import UIModules # Don't support Jinja2
from Template import TemplateLoader # For Jinja2


class App(tornado.web.Application):

    def __init__(self,handlers,conf,log):
        self.__version__ = conf['version']
        self.log = log
        settings = conf['app_settings']
        settings['default_handler_class'] = Page404Handler  # 404
        # Don't Support for Jinja2
        #settings['ui_modules'] = UIModules
        #tornado.web.Application.__init__(self, handlers, **settings)
        # Support for Jinja2
        tpl_loader = TemplateLoader(settings['template_path'], False)
        tornado.web.Application.__init__(self, handlers, template_loader=tpl_loader.Loader(), **settings)
        #每10秒执行一次
        #tornado.ioloop.PeriodicCallback(self.test, 1 * 10 * 1000).start()
        # Init Database
        self.db = db.DB(**conf['db'])
        #Init Redis
        R = db.Redis(**conf['redis'])
        self.redis = R.Connect()
        # Load Locale
        self.__load_locale(settings['default_lang'])


    #def test(self):
    #    self.log.info('Test')

    # Load Locale
    def __load_locale(self,default_lang):
        tornado.locale.load_translations('locale')
        tornado.locale.set_default_locale(default_lang)

class DNStack():

    def __init__(self,processes=4):
        self.__version__ = '1.0.0'
        self.host = config['host']
        self.port = config['port']
        self.urls = route
        self.config = config
        self.config['version'] = self.__version__
        self.log = gen_log
        if platform.system() == "Linux":  #根据操作系统类型来确定是否启用多线程
            self.processes = processes # 当processes>1时，PeriodicCallback定时任务会响相应的执行多次
        else:
            self.processes = 1
        self.log.info('DNStack %s' % self.__version__)  # 启动时打印版本号
        self.log.info('Listen Port: %s' % self.port)


    # 单进程模式
    def run(self):
        app = App(self.urls, self.config, self.log)
        app.listen(self.port)
        tornado.ioloop.IOLoop.current().start()


    # 多线程模式
    def run_multi(self):
        http_sockets = tornado.netutil.bind_sockets(self.port, self.host)
        tornado.process.fork_processes(num_processes=self.processes)
        http_server = tornado.httpserver.HTTPServer(request_callback=App(self.urls,self.config,self.log), xheaders=True)
        http_server.add_sockets(http_sockets)
        tornado.ioloop.IOLoop.instance().start()
