import datetime

import pytz
from aiohttp.web_exceptions import HTTPNoContent, HTTPConflict
from sqlalchemy.exc import IntegrityError

from icw.api.db import Accident
from ..db.citation import Citation, CitationAccident
from . import BaseHandler

__all__ = ['CitationSubmissionHandler']


class CitationSubmissionHandler(BaseHandler):
    def post(self, request):
        yield from request.post()
        url = request.POST['url']
        request.session.begin_nested()
        try:
            citation = Citation(url=url,
                                added=pytz.utc.localize(datetime.datetime.utcnow()))
            request.session.add(citation)
            request.session.commit()
        except IntegrityError:
            request.session.rollback()
            citation = request.session.query(Citation).filter_by(url=url).one()

        if 'accident_id' in request.POST:
            accident = request.session.query(Accident).get(request.POST['accident_id'])
            if not accident:
                raise HTTPConflict()
            request.session.begin_nested()
            try:
                assoc = CitationAccident(accident=accident, citation=citation)
                citation.accidents.append(assoc)
                request.session.commit()
            except IntegrityError:
                request.session.rollback()

        return HTTPNoContent()
