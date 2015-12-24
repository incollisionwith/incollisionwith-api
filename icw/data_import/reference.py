import csv
import pkgutil

import yaml

import icw.db
import icw.db.reference

def load_generic(app, filename, model):
    session = app['db-session']()

    data = yaml.load(pkgutil.get_data('icw', filename))
    for datum in data:
        accident_severity = model(**datum)
        session.merge(accident_severity)

    session.commit()


if __name__ == '__main__':
    import sys
    from ..app import get_app
    app = get_app()

    for name in dir(icw.db):
        cls = getattr(icw.db, name)
        if isinstance(cls, type) and \
           issubclass(cls, icw.db.reference.ReferenceTable) and \
           cls is not icw.db.reference.ReferenceTable:
            load_generic(app, 'data/{}.yaml'.format(cls.__tablename__), cls)
