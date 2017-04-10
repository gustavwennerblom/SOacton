import datetime
import logging
import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename="SOacton.log", format=FORMAT, level=logging.DEBUG)

class ActonKeyRing(Base):
    __tablename__ = 'actonsession'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    access_token = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    refresh_token = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    lease_start = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)

    logging.info("Table created in database for storage of keys")

    def get_token(self):
        return self.access_token


class DBmanager:
    def __init__(self):
        # Create engine to manage the stuff
        self.engine = sqlalchemy.create_engine('sqlite:///actonsession.db')
        # Create table
        Base.metadata.create_all(self.engine)
        db_session = sqlalchemy.orm.sessionmaker(bind=self.engine)
        self.session = db_session()
        logging.info("Database session established")

    def insert_tokens(self, access_token, refresh_token):
        new_tokens = ActonKeyRing(
            access_token=access_token,
            refresh_token=refresh_token,
            lease_start=datetime.datetime.now()
        )
        self.session.add(new_tokens)
        self.session.commit()
        logging.info("New set of tokens inserted into keyring in database")

    def get_token(self):
        result = self.session.query(ActonKeyRing).all()
        latest_token = result[-1].access_token
        logging.info("Current token {0} retrieved from database".format(latest_token))
        return latest_token

    def get_refresh_token(self):
        result = self.session.query(ActonKeyRing).all()
        latest_refresh_token = result[-1].refresh_token
        return latest_refresh_token

    def get_key_timestamp(self):
        result = self.session.query(ActonKeyRing).all()
        return result[-1].lease_start

