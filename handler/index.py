#!/usr/bin/python
# -*- coding:utf-8 -*-
# Powered By KK Studio
# Index Page

from BaseHandler import BaseHandler
from tornado.web import authenticated as Auth

class IndexHandler(BaseHandler):

    #@Auth
    def get(self):
        #self.log.info('Hell,Index page!') # Log Test
        self.render('index/index.html')

class BlankHandler(BaseHandler):
    # @Auth
    def get(self):
        self.render('index/blank.html')
