import asyncio

import math
from urllib.parse import urlencode

from aiohttp.web_exceptions import HTTPNotFound, HTTPBadRequest
from aiohttp_utils import Response
import dateutil.parser
from sqlalchemy.dialects.postgresql import BIT
from sqlalchemy.orm import joinedload

from ..db import Accident, Vehicle, Casualty
from . import BaseHandler

__all__ = ['AccidentListHandler', 'AccidentDetailHandler']


class AccidentListHandler(BaseHandler):
    page_size = 100

    @asyncio.coroutine
    def get(self, request):
        query = request.session.query(Accident) #.options(joinedload('citations').joinedload('citation'),
                                                #         joinedload('vehicles').joinedload('casualties'))

        try:
            page = int(request.GET.get('p') or 1)
            if page < 1:
                raise HTTPNotFound
        except ValueError:
            raise HTTPBadRequest

        if request.GET.get('news') == 'yes':
            query = query.filter(Accident.citations.any())

        if 'sort' in request.GET:
            query = query.order_by(*request.GET.getall('sort'))

        if request.GET.get('dateTimeLower'):
            try:
                datetime_lower = dateutil.parser.parse(request.GET['dateTimeLower'])
            except ValueError:
                raise HTTPBadRequest
            else:
                query = query.filter(Accident.date_and_time >= datetime_lower)
        if request.GET.get('dateTimeUpper'):
            try:
                datetime_upper = dateutil.parser.parse(request.GET['dateTimeUpper'])
            except ValueError:
                raise HTTPBadRequest
            else:
                query = query.filter(Accident.date_and_time < datetime_upper)

        if 'severity' in request.GET:
            query = query.filter(Accident.severity_id.in_(request.GET.getall('severity')))

        highway_authorities = list(filter(None, request.GET.getall('highwayAuthority', ())))
        if highway_authorities:
            query = query.filter(Accident.highway_authority_id.in_(highway_authorities))

        police_forces = list(filter(None, request.GET.getall('policeForce', ())))
        if police_forces:
            query = query.filter(Accident.police_force_id.in_(police_forces))

        if 'policeAttended' in request.GET:
            query = query.filter(Accident.police_attended == (request.GET.get('policeAttended') == 'yes'))

        if 'involvedVehicleType' in request.GET:
            vehicle_types = set(map(int, request.GET.getall('involvedVehicleType')))
            vehicle_types = '{:0100b}'.format(sum(1 << vt for vt in vehicle_types))
            query = query.filter((Accident.involved_vehicle_types.op('&')(vehicle_types)) == vehicle_types)

        if 'involvedCasualtyType' in request.GET:
            casualty_types = set(map(int, request.GET.getall('involvedCasualtyType')))
            casualty_types = '{:0100b}'.format(sum(1 << ct for ct in casualty_types))
            query = query.filter((Accident.involved_casualty_types.op('&')(casualty_types)) == casualty_types)

        if 'bbox' in request.GET:
            x1, y1, x2, y2 = map(float, request.GET['bbox'].split(','))
            query = query.filter(Accident.location.contained(
                'SRID=4326;POLYGON(({x1} {y1}, {x1} {y2}, {x2} {y2}, {x2} {y1}, {x1} {y1}))'.format(x1=x1,
                                                                                                    y1=y1,
                                                                                                    x2=x2,
                                                                                                    y2=y2)))

        count = query.count()
        page_count = max(1, math.ceil(count / self.page_size))

        query = query.offset((page - 1) * self.page_size).limit(self.page_size)

        data = {
            'page': page,
            'count': count,
            'pageCount': page_count,
            '_links': {
                'self': {'href': request.path_qs},
            },
            '_embedded': {
                'item': [a.to_json(request.app) for a in query.all()]
            },
        }

        # Add pagination links
        qs = request.GET.copy()
        qs.pop('p', None)
        qs = tuple(qs.items())
        if page > 1:
            data['_links']['prev'] = {'href': '?' + urlencode(qs + (('p', str(page - 1)),))}
        if page < page_count:
            data['_links']['next'] = {'href': '?' + urlencode(qs + (('p', str(page + 1)),))}

        return Response(data)


class AccidentDetailHandler(BaseHandler):
    @asyncio.coroutine
    def get(self, request):
        accident = request.session.query(Accident) \
            .options(joinedload('citations').joinedload('citation'),
                     joinedload('vehicles').joinedload('casualties')) \
            .get(request.match_info['accident_id'])
        if not accident:
            return HTTPNotFound()
        return Response(accident.to_json(request.app))
