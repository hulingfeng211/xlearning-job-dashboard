# -*- coding:utf-8 -*-

import os
from functools import partial

from tornado.web import Application, url, StaticFileHandler
from tornado.gen import IOLoop, coroutine
from tornado.options import parse_command_line
from tornado.log import gen_log

from core import BaseHandler


path_join = partial(os.path.join, os.path.dirname(__file__))

UPLOAD_DIR = path_join('upload')

if not os.path.exists(UPLOAD_DIR):
    os.mkdir(UPLOAD_DIR)


class IndexHandler(BaseHandler):
    def get(self):
        self.render('index.html')


class HelloHandler(BaseHandler):
    def get(self):
        self.write("hello,iView")


class ModelFileUploadHandler(BaseHandler):
    
    @coroutine
    def post(self):
        #{'file': [{'filename': 'C:\\Users\\15921\\Desktop\\a.txt', 'body': b'a', 'content_type': 'text/plain'}]}
        for upload_file in self.request.files.get('file',[]):
            # C:\\Users\\15921\\Desktop\\a.txt
            file_name=upload_file.get('filename')
            
            body=upload_file.get('body')
            gen_log.info(file_name)


def make_app():
    parse_command_line()
    setting = {
        "debug": True,
        "static_file": path_join('dist'),
        #"static_url_prefix": '/dist/'
    }
    handlers = [
        url(r'/', IndexHandler),
        url(r'/api/hello', HelloHandler),
        url(r'/dist/(.*)', StaticFileHandler, {"path": path_join('dist')}),
        url(r'/api/upload/model', ModelFileUploadHandler)
    ]
    app = Application(handlers=handlers, **setting)
    app.listen(8081)
    IOLoop.current().start()


if __name__ == '__main__':
    make_app()
