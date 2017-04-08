import logging
import sqlalchemy
import sqlalchemy.orm
import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ActonKeyRing(Base):
    __tablename__ = 'actonsession'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    access_token = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    refresh_token = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    lease_start = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)

    def get_token(self):

        return self.access_token


class DBmanager:
    def __init__(self):
        # Create engine to manage the stuff
        self.engine = sqlalchemy.create_engine('sqlite:///actonsession.db')
        # Create table
        Base.metadata.create_all(self.engine)
        # Base.metadata.bind(self.engine)
        db_session = sqlalchemy.orm.sessionmaker(bind=self.engine)
        self.session = db_session()
        # self.keyring = ActonKeyRing()

    def insert_tokens(self, access_token, refresh_token):
        new_tokens = ActonKeyRing(
            access_token=access_token,
            refresh_token=refresh_token,
            lease_start=datetime.datetime.now()
        )
        self.session.add(new_tokens)
        self.session.commit()

    def get_token(self):
        result = self.session.query(ActonKeyRing).all()
        token = result[0].access_token
        print("Current token is: {}".format(token))
        return token


