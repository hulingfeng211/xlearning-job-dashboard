# -*- coding:utf-8 -*-

import os
from functools import partial
import shutil

from tornado.web import Application, url, StaticFileHandler,HTTPError
from tornado.gen import IOLoop, coroutine
from tornado.options import parse_command_line
from tornado.log import gen_log
from motor import motor_tornado 

from core import BaseHandler

db=motor_tornado.MotorClient('localhost', 27017).xlearning_job

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

class JobSubmitHandler(BaseHandler):
    
    @coroutine
    def post(self):
        gen_log.info(self.request.headers)
        gen_log.info(self.request.body)
        data=self.get_all_request_arguments()
        yield self.db.jobs.insert(data)
        self.write_json('success')

class JobHandler(BaseHandler):
    
    @coroutine 
    def get(self):
       data=yield self.db.jobs.find({}).to_list(length=None)
       self.write_json(data)         

class FileUploadHandler(BaseHandler):
    
    @coroutine
    def post(self):
        #{'file': [{'filename': 'C:\\Users\\15921\\Desktop\\a.txt', 'body': b'a', 'content_type': 'text/plain'}]}
        uuid=self.get_argument('uuid')
        upload_type=self.get_argument('type')

        gen_log.info(UPLOAD_DIR)
        job_file_dir=os.path.join(UPLOAD_DIR,uuid)
        job_file_dir=os.path.join(job_file_dir,upload_type)
        
        if not os.path.exists(job_file_dir):
            os.makedirs(job_file_dir,exist_ok=False)
            #os.mkdirs()

        gen_log.info(uuid)
        for upload_file in self.request.files.get('file',[]):
            # C:\\Users\\15921\\Desktop\\a.txt
            remote_file_name=upload_file.get('filename')
            file_name=os.path.basename(remote_file_name)
            local_file_path=os.path.join(job_file_dir,file_name)
            
            if not os.path.exists(local_file_path) :
                # todo save file to dir 
                with open(local_file_path,'wb') as f:
                    f.write(upload_file.get('body'))
                
            else:
                # todo err file is exists
                raise HTTPError(status_code=500,log_message='文件已经存在')  
               


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
        url(r'/api/upload/model', FileUploadHandler),
        url(r'/api/job/create',JobSubmitHandler),
        url(r'/api/jobs',JobHandler),
    ]
    app = Application(handlers=handlers, **setting)
    app.db=db
    app.listen(8081)
    IOLoop.current().start()


if __name__ == '__main__':
    make_app()
