import hashlib


def md5(data: str | bytes, encoding: str = "utf-8") -> str:
    if isinstance(data, str):
        return hashlib.md5(data.encode(encoding)).hexdigest()
    if isinstance(data, bytes):
        return hashlib.md5(data).hexdigest()
