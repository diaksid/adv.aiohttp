import json
from aiohttp_session import get_session


async def flash_middleware(app, handler):
    async def middleware(request):
        try:
            response = await handler(request)
        except Exception as e:
            raise e
        else:
            session = await get_session(request)
            messages = session.pop('flash.messages', None)
            if messages:
                response.set_cookie('flash.messages', json.dumps(messages))
            else:
                response.del_cookie('flash.messages')
            return response

    return middleware
