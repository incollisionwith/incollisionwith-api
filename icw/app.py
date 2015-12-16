import functools
import os

import aiohttp.web
from SPARQLWrapper import SPARQLWrapper2
import sqlalchemy
import sqlalchemy.orm

def get_app():
    app = aiohttp.web.Application()

    app['dbpedia-sparql'] = functools.partial(SPARQLWrapper2,
                                              os.environ.get('DBPEDIA_ENDPOINT',
                                                             'http://dbpedia.org/sparql'))
    app['db-engine'] = sqlalchemy.create_engine(os.environ['DB_URL'])
    app['db-session'] = sqlalchemy.orm.sessionmaker(app['db-engine'])

    return app