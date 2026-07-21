import time

from app.utils.constant import REQUEST_SUCCESS


class R:
    @classmethod
    def success(cls, data, msg=REQUEST_SUCCESS, code=200, status=200):
        return {
            'status': code,
            'result': data,
            'message': msg,
            'timestamp': int(time.time() * 1000)
        }

    @classmethod
    def error(cls, msg, code=400, status=200):
        return {
            'status': code,
            'result': {},
            'message': msg,
            'timestamp': int(time.time() * 1000)
        }
