# -*- coding:utf-8 -*-

import os
from functools import partial

from tornado.web import Application, url,StaticFileHandler
from tornado.gen import IOLoop, coroutine
from tornado.options import parse_command_line

from core import BaseHandler

path_join = partial(os.path.join, os.path.dirname(__file__))




class IndexHandler(BaseHandler):
    def get(self):
        self.render('index.html')


class HelloHandler(BaseHandler):
    def get(self):
        self.write("hello,iView")




def make_app():
    parse_command_line()
    setting = {
        "debug": True,
        "static_file": path_join('dist'),
        "static_url_prefix": '/dist/'
    }
    handlers = [
        url(r'/', IndexHandler),
        url(r'/api/hello',HelloHandler),
        #url(r'/dist/(.*)',StaticFileHandler,{"path":path_join('dist')}) 
    ]
    app = Application(handlers=handlers, **setting)
    app.listen(8081)
    IOLoop.current().start()

if __name__ == '__main__':
    make_app()
