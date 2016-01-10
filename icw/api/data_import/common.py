import csv
from itertools import islice

from sqlalchemy import inspect


def indexed(row, name):
    value = int(row[name])
    if value != -1:
        return value


def split_every(n, iterable):
    i = iter(iterable)
    piece = list(islice(i, n))
    while piece:
        yield piece
        piece = list(islice(i, n))


def load_table(app, f, table, row_parser):
    pks = inspect(table).primary_key
    pk0 = pks[0]
    reader = csv.DictReader(f)

    session = app['db-session']()

    for i, accidents in enumerate(split_every(10000, map(row_parser, reader))):
        accident_ids = {tuple(accident[pk.name] for pk in pks) for accident in accidents}
        existing_accident_ids = set(session.query(table).filter(pk0.in_([aid[0] for aid in accident_ids])).values(*pks))

        insertions = [accident for accident in accidents if tuple(accident[pk.name] for pk in pks) not in existing_accident_ids]
        updates = [accident for accident in accidents if tuple(accident[pk.name] for pk in pks) in existing_accident_ids]

        print(i, len(insertions), len(updates))

        session.bulk_insert_mappings(table, insertions)
        session.bulk_update_mappings(table, updates)
        session.flush()
        session.commit()


def load_table_main(table, row_parser):
    import sys
    from ..app import get_app
    app = get_app()

    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            load_table(app, f, table, row_parser)
    else:
        load_table(app, sys.stdin, table, row_parser)