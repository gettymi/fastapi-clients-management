from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import BASE


DATABASE_URL = "sqlite:///./data.db"

engine = create_engine(DATABASE_URL,connect_args={'check_same_thread':False})

SessionLocal =sessionmaker(bind=engine)


def init_db():

    BASE.metadata.create_all(bind=engine)