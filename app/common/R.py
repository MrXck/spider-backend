import time

from app.utils.constant import REQUEST_SUCCESS


class R:
    @classmethod
    def success(cls, data, msg=REQUEST_SUCCESS, code=0, status=200):
        return {
            'code': code,
            'data': data,
            'msg': msg,
            'timestamp': int(time.time() * 1000)
        }

    @classmethod
    def error(cls, msg, code=1, status=200):
        return {
            'code': code,
            'data': {},
            'msg': msg,
            'timestamp': int(time.time() * 1000)
        }
