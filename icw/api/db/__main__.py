
if __name__ == '__main__':
    from ..app import get_app
    from . import Base

    app = get_app(with_reference_data=False)
    Base.metadata.create_all(app['db-engine'])