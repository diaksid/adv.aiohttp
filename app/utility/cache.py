import pickle, hashlib
from aiohttp import web, web_reqrep, CIMultiDict

from ..config import memcache as config


def _key(name, kwargs):
    key = [bytes(config.get('prefix', ''), 'utf-8'),
           bytes(name, 'utf-8')] + \
          ['%s%s%s' % (bytes(k, 'utf-8'), b'\xff', pickle.dumps(v))
           for k, v in kwargs.items()]
    key = b'\xff'.join(key)
    key = bytes(hashlib.sha1(key).hexdigest(), 'ascii')
    return key


def cache(name, expire=config.get('expire', 60)):
    def decorator(func):
        async def wrapper(request=None, **kwargs):
            args = [r for r in [request]
                    if isinstance(r, web_reqrep.Request)]
            key = _key(name, kwargs)

            mcache = request.app.mcache
            value = await mcache.get(key)
            if value is None:
                value = await func(*args, **kwargs)
                v_h = {}
                if isinstance(value, web.Response):
                    v_h = value._headers
                    value._headers = [(k, v)
                                      for k, v in value._headers.items()]
                await mcache.set(
                    key,
                    pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL),
                    exptime=expire,
                )
                if isinstance(value, web.Response):
                    value._headers = v_h
            else:
                value = pickle.loads(value)
                if isinstance(value, web.Response):
                    value._headers = CIMultiDict(value._headers)
            return value

        return wrapper

    return decorator
