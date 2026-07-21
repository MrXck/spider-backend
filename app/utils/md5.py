import hashlib

from app.utils.constant import ENCODE_STRING


def md5hex(string):
    md5 = hashlib.md5(b'dsakfhdsk^&%&(*&*()^^&$^%TYU')
    md5.update(string.encode(ENCODE_STRING))
    return md5.hexdigest()
