from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL connection URL format:
# postgresql://<username>:<password>@<host>:<port>/<database>
DATABASE_URL = "postgresql://postgres:mysecretpassword@localhost:5432/gamesdb"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "SessionLocal" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for the ORM models
Base = declarative_base()
