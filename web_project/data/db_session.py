import sqlalchemy
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as declarative

SqlAlchemyBase = declarative.declarative_base()

__factory = None


def global_init(database):
    global __factory

    if __factory:
        return

    if not database.strip():
        raise Exception("You must specify the database file.")

    connect_string = f'sqlite:///{database.strip()}?check_same_thread=False'
    print(f"Connecting to the database at \"{connect_string}\"")

    engine = sqlalchemy.create_engine(connect_string, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory

    return __factory()
