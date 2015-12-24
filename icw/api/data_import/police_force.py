import pkgutil

import rdflib
import yaml
from SPARQLWrapper import JSON

from ..db import PoliceForce

__all__ = ['load_police_force']

query_pattern = """\
SELECT * WHERE {{
    VALUES ?uri {{ {uris} }}
    OPTIONAL {{ ?uri rdfs:label ?label . FILTER (LANG(?label) = "en") }}
    OPTIONAL {{ ?uri rdfs:comment ?comment . FILTER (LANG(?comment) = "en") }}
    OPTIONAL {{ ?uri foaf:homepage ?homepage }}
    OPTIONAL {{ ?uri foaf:depiction ?logo_url }}
}}
"""

dbpedia_resource_prefix = 'http://dbpedia.org/resource/'

def load_police_force(app):
    data = yaml.load(pkgutil.get_data('icw', 'data/police_force.yaml'))
    for datum in data:
        datum['uri'] = rdflib.URIRef(dbpedia_resource_prefix + datum.pop('dbpedia'))

    ids = {str(datum['uri']): datum['id'] for datum in data}

    sparql = app['dbpedia-sparql']()
    sparql.setQuery(query_pattern.format(uris=' '.join(d['uri'].n3() for d in data)))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    import pprint
    pprint.pprint(results)

    session = app['db-session']()

    for binding in results.bindings:
        police_force = PoliceForce(id=ids[binding['uri'].value],
                                 **{k: v.value for k, v in binding.items()})
        session.merge(police_force)

    session.commit()

if __name__ == '__main__':
    from ..app import get_app
    app = get_app()
    load_police_force(app)
