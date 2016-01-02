import functools
import os

import aiohttp.web
from SPARQLWrapper import SPARQLWrapper2
import sqlalchemy
import sqlalchemy.orm
from aiohttp_utils import negotiation

from icw.api import middleware
from . import handlers

def get_app():
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

    negotiation.setup(app)

    return app