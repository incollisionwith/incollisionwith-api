import asyncio

from aiohttp.web_exceptions import HTTPNotFound, HTTPBadRequest
from aiohttp_utils import Response

from ..db import Accident, Vehicle, Casualty
from . import BaseHandler

__all__ = ['AccidentListHandler', 'AccidentDetailHandler']


class AccidentListHandler(BaseHandler):
    page_size = 50

    @asyncio.coroutine
    def get(self, request):
        query = request.session.query(Accident)

        try:
            page = int(request.GET.get('p') or 1)
        except ValueError:
            raise HTTPBadRequest

        if request.GET.get('news') == 'yes':
            query = query.filter(Accident.citations.any())

        if 'sort' in request.GET:

            query = query.order_by(*request.GET.getall('sort'))

        if 'severity' in request.GET:
            query = query.filter(Accident.severity_id.in_(request.GET.getall('severity')))

        if 'involvedVehicleType' in request.GET:
            query = query.filter(Accident.vehicles.any(Vehicle.type_id.in_(request.GET.getall('involvedVehicleType'))))

        if 'involvedCasualtyType' in request.GET:
            query = query.filter(Accident.casualties.any(Casualty.type_id.in_(request.GET.getall('involvedCasualtyType'))))

        if 'bbox' in request.GET:
            x1, y1, x2, y2 = map(float, request.GET['bbox'].split(','))
            query = query.filter(Accident.location.contained(
                'SRID=4326;POLYGON(({x1} {y1}, {x1} {y2}, {x2} {y2}, {x2} {y1}, {x1} {y1}))'.format(x1=x1,
                                                                                                    y1=y1,
                                                                                                    x2=x2,
                                                                                                    y2=y2)))

        query = query.offset((page - 1) * self.page_size).limit(self.page_size)

        return Response([a.to_json() for a in query.all()])

class AccidentDetailHandler(BaseHandler):
    @asyncio.coroutine
    def get(self, request):
        accident = request.session.query(Accident).get(request.match_info['accident_id'])
        if not accident:
            return HTTPNotFound()
        return Response(accident.to_json())
