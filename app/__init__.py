import sys
import os
import jinja2
import aiohttp_jinja2 as engine
import aiomcache
from aiohttp_session import session_middleware, SimpleCookieStorage
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp import web

from . import config
from .middleware import (
    error_middleware,
    flash_middleware,
    minify_middleware,
)
from .view import (
    context_processor,
    home,
    contact, callback,
    ws, ws_handler,
)


assert sys.version_info >= (3, 5), 'Please use Python 3.5 or higher.'

__version__ = '0.0.1'

__all__ = ['application', 'init']

os.chdir(os.path.abspath(os.path.dirname(__file__)))


def application(loop=None):
    middlewares = [
        minify_middleware,
        error_middleware,
        flash_middleware,
    ]
    if getattr(config, 'test', None):
        storage = SimpleCookieStorage()
    else:
        storage = EncryptedCookieStorage(config.session_key)
    middlewares.append(session_middleware(storage))

    app = web.Application(loop=loop,
                          middlewares=middlewares,
                          debug=config.debug)

    app.mcache = aiomcache.Client(*config.memcache['server'], loop=loop)

    if config.debug:
        import aiohttp_debugtoolbar
        aiohttp_debugtoolbar.setup(app, intercept_redirects=False)

    engine.setup(app,
                 context_processors=[context_processor,
                                     engine.request_processor],
                 loader=jinja2.FileSystemLoader('./template'))

    app.router \
        .add_resource('/', name='home') \
        .add_route('GET', home)

    app.router \
        .add_resource('/contact', name='contact') \
        .add_route('POST', contact)
    app.router \
        .add_resource('/callback', name='callback') \
        .add_route('POST', callback)

    app.router \
        .add_resource('/ws', name='chat') \
        .add_route('GET', ws)
    app.router.add_route('GET', '/wsh', ws_handler)

    return app


async def init(loop):
    app = application(loop)
    handler = app.make_handler()
    srv = await loop.create_server(handler, *config.server)

    print('serving on', srv.sockets[0].getsockname())
    print('started at http://%s:%d' % config.server)

    return srv, handler
