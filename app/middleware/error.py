from aiohttp import web

from .. import engine


async def error_middleware(app, handler):
    async def middleware(request):
        async def error(response, context):
            response.content_type = 'text/html'
            response.body = engine.render_string(
                'app/layout/error.html', request, context).encode('utf-8')
            return response

        try:
            response = await handler(request)
        except web.HTTPBadRequest as e:
            return await error(e, dict(
                code=400,
                name='Недопустимый запрос',
                error=e.text,
            ))
        except web.HTTPForbidden as e:
            return await error(e, dict(
                code=403,
                name='Доступ к ресурсу запрещен',
                error=e.text,
            ))
        except web.HTTPNotFound as e:
            return await error(e, dict(
                code=404,
                name='Ресурс не найден',
                error=e.text,
            ))
        except web.HTTPMethodNotAllowed as e:
            return await error(e, dict(
                code=405,
                name='Недопустимый метод',
                error=e.text,
            ))
        except web.HTTPInternalServerError as e:
            return await error(e, dict(
                code=500,
                name='Внутренняя ошибка сервера',
                error=e.text,
            ))
        except Exception as e:
            raise e
        else:
            return response

    return middleware
