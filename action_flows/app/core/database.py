from sqlmodel import create_engine, SQLModel, Session
from app.core.config import settings

database_url = "postgresql://postgresql@localhost/flow_mile"

#engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

def get_engine():
    try:
        engine = create_engine(database_url)
        print('egnine created')
        return engine
    except Exception as e:
        print(e)
    
    return None
        
engine = get_engine()

def create_db_and_tables():
    SQLModel.metadata.create_all(get_engine)
    
    
    