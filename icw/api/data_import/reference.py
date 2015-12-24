import csv
import pkgutil

import yaml

from .. import db

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

    for name in dir(db):
        cls = getattr(db, name)
        if isinstance(cls, type) and \
           issubclass(cls, db.ReferenceTable) and \
           cls is not db.ReferenceTable:
            load_generic(app, 'data/{}.yaml'.format(cls.__tablename__), cls)
