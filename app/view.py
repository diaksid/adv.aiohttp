from aiohttp import web, MsgType
import aiohttp_jinja2 as engine
from aiohttp_session import get_session

from proj.aiohttp.form import ContactForm, CallbackForm
from proj.aiohttp.utility import cache, EmailMultipart

from . import config


__all__ = ['context_processor',
           'home',
           'contact', 'callback',
           'ws', 'ws_handler']


async def context_processor(request):
    session = await get_session(request)
    return dict(
        debug=getattr(config, 'debug', True),
        static=getattr(config, 'static', '/static'),
        media=getattr(config, 'media', '/media'),
        yandex=getattr(config, 'yandex', None),
        google=getattr(config, 'google', None),
        twitter=getattr(config, 'twitter', None),
        messages=session.pop('flash.messages', None),
    )


@engine.template('app/content/home.html')
async def home(request):
    secret = getattr(config, 'session_key', b'')
    session = await get_session(request)
    contact = ContactForm(session, secret, prefix='contact')
    callback = CallbackForm(session, secret, prefix='callback')
    return dict(
        title='Строительный контроль',
        description='Проведение мероприятий строительного контроля в Москве и области',
        keywords='строительный контроль',
        contact=contact,
        callback=callback,
    )


async def contact(request):
    secret = getattr(config, 'session_key', b'')
    session = await get_session(request)
    messages = session.pop('flash.messages', [])
    post = await request.post()
    form = ContactForm(session, secret, post, prefix='contact')
    if form.validate():
        mail = EmailMultipart(request)
        mail.contact(form.data)
        send = await mail.send()
        if send:
            messages.append(('Сообщение отправлено', 'success',))
        else:
            messages.append(('Ошибка отправки сообщения', 'error',))
    else:
        messages.append(('Ошибка ввода данных', 'error',))
    session['flash.messages'] = messages
    raise web.HTTPSeeOther(request.app.router['home'].url())


async def callback(request):
    secret = getattr(config, 'session_key', b'')
    session = await get_session(request)
    messages = session.pop('flash.messages', [])
    post = await request.post()
    form = CallbackForm(session, secret, post, prefix='callback')
    if form.validate():
        mail = EmailMultipart(request)
        mail.callback(form.data)
        send = await mail.send()
        if send:
            messages.append(('Сообщение отправлено', 'success',))
        else:
            messages.append(('Ошибка отправки сообщения', 'error',))
    else:
        messages.append(('Ошибка ввода данных', 'error',))
    session['flash.messages'] = messages
    raise web.HTTPSeeOther(request.app.router['home'].url())


@engine.template('app/content/chat.html')
async def ws(request):
    secret = getattr(config, 'session_key', b'')
    session = await get_session(request)
    callback = CallbackForm(session, secret, prefix='callback')
    return dict(
        title='Строительный контроль Chat',
        description='Строительный контроль Chat',
        callback=callback,
    )


async def ws_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    async for msg in ws:
        if msg.tp == MsgType.text:
            if msg.data == 'close':
                await ws.close()
            else:
                ws.send_str(msg.data + '/answer')
        elif msg.tp == MsgType.close:
            print('websocket connection closed')
        elif msg.tp == MsgType.error:
            print('ws connection closed with exception: %s', ws.exception())
    return ws
