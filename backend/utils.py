# -*- coding:utf-8 -*- 

from bson import ObjectId 



def is_object_id(doc_id):
    """
    判断输入的字符串是不是ObjectId的格式
    :param doc_id 文档的id
    """
    return ObjectId.is_valid(doc_id)