import asyncio
import datetime
import logging

import functools
from io import BytesIO

import aiohttp
import lxml.etree
#import opengraph
import pytz
import rdflib

from icw.api.db.citation import Citation

logger = logging.getLogger(__name__)

SCHEMA = rdflib.Namespace('http://schema.org/')

def first_non_null(func):
    @functools.wraps(func)
    def f(*args, **kwargs):
        for item in func(*args, **kwargs):
            if item is not None:
                return item
    return f

@first_non_null
def get_citation_title(doc, uri, og, graph):
    if uri:
        yield graph.value(uri, SCHEMA.headline)
    yield og.get('og:title')
    for title in doc.xpath('/html/head/title'):
        yield (title.text or ''.strip()) or None

@first_non_null
def get_citation_description(doc, uri, og, graph):
    if uri:
        yield graph.value(uri, SCHEMA.articleBody)
    yield og.get('og:description')

@first_non_null
def get_citation_published(doc, uri, og, graph):
    if uri:
        published = graph.value(uri, SCHEMA.datePublished)
        if published:
            yield published.toPython()

@first_non_null
def get_citation_publisher(doc, uri, og, graph):
    if uri:
        publisher = graph.value(uri, SCHEMA.publisher)
        if publisher:
            yield graph.value(uri, SCHEMA.name)
    yield og.get('og:site_name')

@asyncio.coroutine
def fetch_citation(session, citation):
    print(citation.url)
    response = yield from aiohttp.client.get(citation.url)
    if response.status != 200:
        logger.warning("Couldn't retrieve %s (status %d)", citation.url, response.status)

    body = yield from response.read()

 #   og = opengraph.OpenGraph()
 #   og.parser(body)

    doc = lxml.etree.fromstring(body, parser=lxml.etree.HTMLParser())
    graph = rdflib.Graph()
    for jsonld in doc.xpath("//script[@type='application/ld+json']"):
        graph.parse(BytesIO(jsonld.text.encode()), response.url, format='json-ld')

    og = doc.xpath("//meta[starts-with(@property, 'og:')]")
    og = {e.attrib['property']: e.attrib['content'] for e in og}

    uri = graph.value(None, SCHEMA.url, rdflib.URIRef(response.url))

    citation.title = get_citation_title(doc, uri, og, graph)
    citation.description = get_citation_description(doc, uri, og, graph)
    citation.published = get_citation_published(doc, uri, og, graph)
    citation.publisher = get_citation_publisher(doc, uri, og, graph)

    citation.image_url = og.get('og:image')

    citation.last_crawled = pytz.utc.localize(datetime.datetime.utcnow())

    session.add(citation)

if __name__ == '__main__':
    from .app import get_app

    app = get_app()
    session = app['db-session']()
    citations = session.query(Citation).filter(Citation.last_crawled == None).all()

    for citation in citations:
        try:
            app.loop.run_until_complete(fetch_citation(session, citation))
        except Exception:
            pass

    session.commit()