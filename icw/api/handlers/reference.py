import asyncio

from aiohttp_utils import Response

from . import BaseHandler

__all__ = ['ReferenceDataHandler']


class ReferenceDataHandler(BaseHandler):
    @asyncio.coroutine
    def get(self, request):
        return Response(request.app['reference-data'])