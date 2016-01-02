import asyncio

from aiohttp.web_exceptions import HTTPException


@asyncio.coroutine
def session_middleware(app, handler):
    @asyncio.coroutine
    def middleware(request):
        session = request.session = app['db-session']()
        try:
            response = yield from handler(request)
            session.commit()
            return response
        except HTTPException as e:
            session.commit()
            raise
        except:
            session.rollback()
            raise
        finally:
            session.close()
    return middleware