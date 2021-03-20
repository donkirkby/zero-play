from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.orm

Base = declarative_base()  # base class for models
Session = sqlalchemy.orm.sessionmaker()  # connection to database
SessionBase = sqlalchemy.orm.Session  # Use as type hint for Session objects.
