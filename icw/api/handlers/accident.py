import asyncio

from aiohttp.web_exceptions import HTTPNotFound
from aiohttp_utils import Response

from ..db import Accident
from . import BaseHandler

__all__ = ['AccidentDetailHandler']


class AccidentDetailHandler(BaseHandler):
    @asyncio.coroutine
    def get(self, request):
        session = request.app['db-session']()
        accident = session.query(Accident).get(request.match_info['accident_id'])
        if not accident:
            return HTTPNotFound()
        return Response(accident.to_json())
