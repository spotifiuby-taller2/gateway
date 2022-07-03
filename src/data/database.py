from datetime import datetime
from sqlalchemy import and_, create_engine
from constants import DATABASE_URI
from apikey import Apikey, Base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

engine = create_engine(DATABASE_URI)

#session factory
Session = sessionmaker(bind=engine)

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        #remove changes
        session.rollback()
        raise
    finally:
        session.close()


def initialize_apikey_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def create_apikey_table_in_engine():
    Base.metadata.create_all(engine)

def drop_apikey_table_in_engine():
    Base.metadata.drop_all(engine)

def add_new_apikey_to_db(id, name, active, date, description):
    apikey = Apikey(
        id = id,
        name = name,
        active = active,
        creationDate = date,
        description = description
    )
    with session_scope() as s:
            s.add(apikey)

def get_all_apikeys():
    with session_scope() as s:
        all = s.query(Apikey).all()
        print(all)

def get_apikey_by_id(id):
    with session_scope() as s:
        result = s.query(Apikey).filter_by(id=id).first()
        print(result)

def get_apikeys_created_between_dates(start_date, end_date, qty_apikeys):
    with session_scope() as s:
        result = s.query(Apikey).filter(Apikey.creationDate.between(start_date, end_date)).limit(qty_apikeys).all()
        print(result)

def get_apikeys_created_between_dates_and_active(start_date, end_date):
    with session_scope() as s:
        result = s.query(Apikey).filter(and_(Apikey.creationDate.between(start_date, end_date)),Apikey.active == True).all()
        print(result)


#TESTING
#initialize_apikey_database()
#apikey1_date = datetime(2022,2,2)
#apikey2_date = datetime(2022,2,10)
#add_new_apikey_to_db(2022,"apikey1",True,apikey1_date, "the first apikey created for the table of apikeys")
#add_new_apikey_to_db(2023,"apikey2",False,apikey2_date, "the second apikey created for the table of apikeys")

#get_all_apikeys()
#VER COMO MANEJAR EL CIERRE DE SESION PORQUE NO ME DEVUELVE EL OBJETO SI DICHA SESION CERRO
#COMMENT: ESTOY CERRANDO LA SESION EN LA FUNCION session_scope()
#get_apikey_by_id("2023")
#start_date = datetime(2022,2,1)
#end_date = datetime(2022,2,13)
#qty_apikeys = 1

#get_apikeys_created_between_dates(start_date, end_date, qty_apikeys)