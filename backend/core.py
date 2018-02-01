# -*- coding:utf-8 -*-


from tornado.web import RequestHandler
import json
from bson import ObjectId


class JSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)

        return json.JSONEncoder.default(self, o)


def bson_encode(data):
    return JSONEncoder().encode(data)


class BaseHandler(RequestHandler):

    @property
    def db(self):
        return self.application.db
        return 'application/json' in self.request.headers['Content-Type']

    def get_request_argument(self, name, default_value=None):
        """
        根据给定的参数名获取参数值,优先处理了json的请求
        """
        if self.is_json_request():
            body = json.loads(self.request.body)
        if body:
            return body.get(name, default_value)
        else:
            return self.get_argument(name,default_value)

    def is_json_request(self):
        return 'application/json' in self.request.headers['Content-Type']

    def get_all_request_arguments(self):
        """
        获取所有的请求参数，直接将self.requeset.body通过json反序列化后返回
        """
        assert self.is_json_request()
        return json.loads(self.request.body)

    def write_json(self, data, code=0, errmsg=''):
        """
        :param data 需要返回的对象，类型可以是dict,list,int,str,tuple
        :code 状态码，返回给浏览器的请求状态0,表示成功，1表示错误
        """
        self.set_header('content-type', 'application/json')
        self.write(bson_encode({'data': data, 'code': code, 'errmsg': errmsg}))
