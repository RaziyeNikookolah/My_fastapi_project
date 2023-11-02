import sqlalchemy
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm

DB_URL="sqlite:///./dbfile.db"

"""
connect_args={"check_same_thread"} is a parameter used when creating a SQLAlchemy database engine for SQLite. This parameter is specific to SQLite and controls how SQLite handles multiple threads accessing the same database connection.

SQLite is designed as a serverless, self-contained database engine, and by default, it doesn't support concurrent access from multiple threads. 
If you try to use a single SQLite database connection from multiple threads simultaneously, it can lead to issues or errors.

"""

engine=sqlalchemy.create_engine(DB_URL,connect_args={"check_same_thread":False})

SessionLocal = orm.sessionmaker(autocommit=False,autoflush=False,bind=engine)
"""
By defining models based on the Base class, you create a structured and consistent way to work with your database tables using Python objects and SQLAlchemy's ORM features.
"""
Base = declarative.declarative_base()