import asyncio

from aiohttp_utils import Response
from sqlalchemy import extract, select, func, exists
from sqlalchemy.sql.functions import count

from icw.api.db import Accident, Vehicle
from icw.api.handlers import BaseHandler


class StatisticsHandler(BaseHandler):
    dimensions = {
        'year': extract('year', Accident.date),
        'month_of_year': extract('month', Accident.date),
        'hour': extract('hour', Accident.date_and_time),
        'quarter': extract('quarter', Accident.date),
        'week': extract('week', Accident.date),
        'day_of_week': extract('dow', Accident.date),
        'number_of_casualties': Accident.number_of_casualties,
        'number_of_vehicles': Accident.number_of_vehicles,
        'police_attended': Accident.police_attended,
        'police_force': Accident.police_force_id,
        'severity': Accident.severity_id,
    }

    filters = {
        'involved_bicycle': lambda q: q.where(Accident.vehicles.any(type_id=1)),
        'involved_motorcycle': (lambda q: q.join(Accident.vehicles).filter(Vehicle.type_id.in_(2, 3, 4, 5, 97))),
    }

    values = {
        'count': count('*'),
        'avg_severity': func.avg(Accident.severity_id),

    }

    @asyncio.coroutine
    def get(self, request):
        dimensions = [self.dimensions[d] for d in request.GET.getall('dimension')]
        filters = [self.filters[f] for f in request.GET.getall('filter')]
        values = [self.values[v] for v in request.GET.getall('value')]
        query = select(dimensions + values)
        for filter in filters:
            query = filter(query)
        query = query.group_by(*dimensions)
        query = query.order_by(*dimensions)
        query = query.limit(1000)
        a = request.session.execute(query).fetchall()
        print('\n'.join(','.join(map(str, x)) for x in a))

        return Response({})