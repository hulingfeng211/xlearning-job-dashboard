# -*- coding:utf-8 -*-

import os
import sys
from functools import partial
import shutil

from tornado.web import Application, url, StaticFileHandler, HTTPError
from tornado.gen import IOLoop, coroutine,sleep
from tornado.options import parse_command_line, define,options
from tornado.log import gen_log
from motor import motor_tornado
from bson import ObjectId

from core import BaseHandler
import utils

define('mongo_host', default='169.24.2.63',
       type=str, help='The database ip address')

define('mongo_port', default=27017, type=int, help='The database port')
define('port', default=8081, type=int, help='listen at this port')


path_join = partial(os.path.join, os.path.dirname(os.path.abspath(__file__)))

PAGE_SIZE = 10
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
        #data = self.get_all_request_arguments()
        job_id=self.get_request_argument('jid',None)
        gen_log.info(job_id)
        if job_id and utils.is_object_id(job_id):
            job = yield self.db.jobs.find_one({"_id":ObjectId(job_id)})
            from hdfs import InsecureClient
            hdfs_client=InsecureClient("http://169.24.2.194:50070",user='hdfs')
            content=hdfs_client.list("/tmp")
            gen_log.info(content)
            content=hdfs_client.list("/tmp")
            gen_log.info(content)

            work_dir=os.path.join(UPLOAD_DIR,job.get('uuid',None))
            data_dir=os.path.join(work_dir,"data")
            model_dir=os.path.join(work_dir,"model")

            # 判断数据文件目录是否存在
            if not  os.path.exists(data_dir):
                self.write_json("数据文件未上传，请上传数据文件",code=1)
                return 

            # 判断模型文件目录是否存在
            if not os.path.exists(model_dir):
                self.write_json("模型文件未上传,请上传模型文件",code=1)
                return 
            
            #开始上传数据文件 
            remote_hdfs_data_dir,local_data_dir=job.get('input',"").split("#")
            hdfs_client.upload(remote_hdfs_data_dir,data_dir,overwrite=True)

            # 切换到model目录
            os.chdir(model_dir)

            # 执行提交任务的命令

            
        #yield self.db.jobs.insert(data)
        #self.write_json('success')


class JobHandler(BaseHandler):

    @coroutine
    def get(self):
        page_index = int(self.get_argument("page_index", 1))
        #page_size = 10
        total = yield self.db.jobs.count({})
        data = yield self.db.jobs.find({}).skip((page_index - 1) * PAGE_SIZE).limit(PAGE_SIZE).to_list(length=None)
        self.write_json({
            "total": total,
            "data": data
        })

    @coroutine
    def post(self,*args,**kwargs):
        
        gen_log.info(self.request.headers)
        gen_log.info(self.request.body)
        data = self.get_all_request_arguments()
        yield self.db.jobs.insert(data)
        self.write_json('success')
    
    @coroutine
    def delete(self,*args,**kwargs):
        job_id=self.get_argument("jid",None)
        yield sleep(3)
        if utils.is_object_id(job_id):
            job=yield self.db.jobs.find_one({"_id":ObjectId(job_id)})
            # 删除本地文件
            work_dir=os.path.join(UPLOAD_DIR,job.get('uuid',None))            
            shutil.rmtree(work_dir,ignore_errors=True)
            yield self.db.jobs.remove({"_id":ObjectId(job_id)})
            self.write_json("删除成功")
        else:
            self.write_json("不是有效的文档的格式,请检查",code=1)



class FileUploadHandler(BaseHandler):

    @coroutine
    def post(self):
        #{'file': [{'filename': 'C:\\Users\\15921\\Desktop\\a.txt', 'body': b'a', 'content_type': 'text/plain'}]}
        uuid = self.get_argument('uuid')
        upload_type = self.get_argument('type')

        gen_log.info(UPLOAD_DIR)
        job_file_dir = os.path.join(UPLOAD_DIR, uuid)
        job_file_dir = os.path.join(job_file_dir, upload_type)

        if not os.path.exists(job_file_dir):
            os.makedirs(job_file_dir, exist_ok=False)
            # os.mkdirs()

        gen_log.info(uuid)
        for upload_file in self.request.files.get('file', []):
            # C:\\Users\\15921\\Desktop\\a.txt
            remote_file_name = upload_file.get('filename')
            file_name = os.path.basename(remote_file_name)
            local_file_path = os.path.join(job_file_dir, file_name)

            if not os.path.exists(local_file_path):
                # todo save file to dir
                with open(local_file_path, 'wb') as f:
                    f.write(upload_file.get('body'))

            else:
                # todo err file is exists
                raise HTTPError(status_code=500, log_message='文件已经存在')


def make_app():
    parse_command_line()
    
    gen_log.info('upload path:{0}'.format(UPLOAD_DIR))
    #db = motor_tornado.MotorClient('169.24.2.63', 27017).xlearning_job
    db = motor_tornado.MotorClient(
        options.mongo_host, options.mongo_port).xlearning_job
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
        url(r'/api/job/create', JobSubmitHandler),
        url(r'/api/jobs', JobHandler),
    ]
    app = Application(handlers=handlers, **setting)
    app.db = db
    app.listen(options.port)
    IOLoop.current().start()


if __name__ == '__main__':
    make_app()
