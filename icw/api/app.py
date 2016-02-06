import functools
import os

import aiohttp.web
from SPARQLWrapper import SPARQLWrapper2
import sqlalchemy
import sqlalchemy.orm
from aiohttp_utils import negotiation

from icw.api import middleware
from . import handlers


def get_reference_data(app):
    from icw.api import db
    session = app['db-session']()

    data = {}
    for name in dir(db):
        cls = getattr(db, name)
        if cls is db.PoliceForce or (
                        isinstance(cls, type) and \
                        issubclass(cls, db.ReferenceTable) and \
                        cls is not db.ReferenceTable):
            data[cls.__name__] = {d.id: d.to_json() for d in session.query(cls).all()}

    session.close()

    return data


def get_app(with_reference_data=True):
    app = aiohttp.web.Application(middlewares=[middleware.session_middleware])

    app['dbpedia-sparql'] = functools.partial(SPARQLWrapper2,
                                              os.environ.get('DBPEDIA_ENDPOINT',
                                                             'http://dbpedia.org/sparql'))
    app['db-engine'] = sqlalchemy.create_engine(os.environ['DB_URL'])
    app['db-session'] = sqlalchemy.orm.sessionmaker(app['db-engine'])

    app.router.add_route('*', '/accident',
                         handlers.AccidentListHandler())
    app.router.add_route('*', '/accident/{accident_id}',
                         handlers.AccidentDetailHandler())
    app.router.add_route('*', '/citation',
                         handlers.CitationSubmissionHandler())
    app.router.add_route('*', '/statistics',
                         handlers.StatisticsHandler())
    app.router.add_route('*', '/reference-data',
                         handlers.ReferenceDataHandler())

    if with_reference_data:
        app['reference-data'] = get_reference_data(app)

    negotiation.setup(app)

    return app