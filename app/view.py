from aiohttp import web, MsgType
import aiohttp_jinja2 as engine
from aiohttp_session import get_session

from . import config
from .form import ContactForm, CallbackForm
from .utility import cache, EmailMultipart


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
    session = await get_session(request)
    contact = ContactForm(session, prefix='contact')
    callback = CallbackForm(session, prefix='callback')
    return dict(
        title='Строительный контроль',
        description='Проведение мероприятий строительного контроля в Москве и области',
        keywords='строительный контроль',
        contact=contact,
        callback=callback,
    )


async def contact(request):
    session = await get_session(request)
    messages = session.pop('flash.messages', [])
    post = await request.post()
    form = ContactForm(session, post, prefix='contact')
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
    session = await get_session(request)
    messages = session.pop('flash.messages', [])
    post = await request.post()
    form = CallbackForm(session, post, prefix='callback')
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
    session = await get_session(request)
    callback = CallbackForm(session, prefix='callback')
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
