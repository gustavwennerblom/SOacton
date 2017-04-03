import logging
import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ActonKeyRing(Base):
    __tablename__ = 'actonsession'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    access_token = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    refresh_token = sqlalchemy.Column(sqlalchemy.String, nullable=True)

class DBmanager:
    def __init__(self):
        # Create engine to manage the stuff
        self.engine = sqlalchemy.create_engine('sqlite:///actonsession.db')
        # Create table
        Base.metadata.create_all(self.engine)
        # Base.metadata.bind(self.engine)
        db_session = sqlalchemy.orm.sessionmaker(bind=self.engine)
        self.session = db_session()

    def insert_tokens(self, access_token, refresh_token):
        new_tokens = ActonKeyRing(access_token=access_token, refresh_token=refresh_token)
        self.session.add(new_tokens)
        self.session.commit()

    def retrieve_tokens(self):
        pass
