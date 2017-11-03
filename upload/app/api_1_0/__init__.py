# -*- coding: utf-8 -*-
import json
from datetime import datetime
from collections import OrderedDict
from flask import request, Blueprint, Response

api = Blueprint('api', __name__)


@api.before_request
def before_request():
    """请求获取到执行
    :return:
    """
    print request.headers


@api.after_request
def after_request(resp):
    """请求返回前执行
    :param resp:
    :return:
    """
    return resp


@api.errorhandler(400)
def err_400(error):
    return make_json_resp(return_msg=error.__str__()), 200


@api.errorhandler(500)
def err_500(error):
    return make_json_resp(return_msg=error.__str__()), 200


ISOTIMEFORMAT = '%Y-%m-%d %X'  # 时间格式


class JsonUtil(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime(ISOTIMEFORMAT)
        return json.JSONEncoder.default(self, obj)


def make_json_resp(
        return_code=0,
        return_msg=u'调用成功',
        data=None,
        ensure_ascii=False,
        transcode=False,
        encoding='utf-8',
        cross_domain=False,
        **kwargs):
    """生成API返回对象
    :param return_code: 返回码
    :param return_msg:  返回信息
    :param data:        具体对象
    :param ensure_ascii:是否二次编码
    :param transcode:   是否转码
    :param encoding:    字符编码
    :param headers:    字符编码
    :param kwargs:      JSON序列化参数
    :return:
    """
    json_base = dict(
        return_code=return_code,
        return_msg=return_msg,
        data=data
    )

    # 编码转换
    if transcode:
        json_base = _transcoding_dict(json_base, encoding)

    resp_str = json.dumps(json_base, sort_keys=True, ensure_ascii=ensure_ascii, encoding=encoding, cls=JsonUtil)
    resp = Response(resp_str, mimetype='application/json; charset=utf-8', **kwargs)

    if cross_domain:
        resp.headers.add('Access-Control-Allow-Origin', '*')
        resp.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        resp.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')

    return resp


def _transcoding(data, encoding='utf-8'):
    """编码转换
    :param data: 需要转换的数据
    :return: 转换好的数据
    """
    if not data:
        return data

    result = None
    if isinstance(data, str) and hasattr(data, 'decode'):
        result = data.decode(encoding)
    else:
        result = data
    return result


def _transcoding_list(data, encoding='utf-8'):
    """编码转换 for list
    :param data: 需要转换的 list 数据
    :return: 转换好的 list
    """
    if not isinstance(data, list):
        raise ValueError('Parameter data must be list object.')

    result = []
    for item in data:
        if isinstance(item, dict):
            result.append(_transcoding_dict(item, encoding=encoding))
        elif isinstance(item, list):
            result.append(_transcoding_list(item, encoding=encoding))
        elif isinstance(item, str) and hasattr(item, 'decode'):
            result.append(_transcoding(item, encoding=encoding))
        else:
            result.append(item)
    return result


def _transcoding_dict(data, encoding='utf-8'):
    """编码转换 for dict
    :param data: 需要转换的 dict 数据
    :return: 转换好的 dict
    """
    if not isinstance(data, dict):
        raise ValueError('Parameter data must be dict object.')

    result = {}
    for k, v in data.items():
        k = _transcoding(k, encoding=encoding)
        if isinstance(v, dict) and not isinstance(v, OrderedDict):
            v = _transcoding_dict(v, encoding=encoding)
        elif isinstance(v, list):
            v = _transcoding_list(v, encoding=encoding)
        else:
            v = _transcoding(v, encoding=encoding)
        result.update({k: v})
    return result

from . import main
