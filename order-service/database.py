from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection URL
DATABASE_URL = "postgresql://postgres:mysecretpassword@localhost:5433/ordersdb"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

# Order model definition
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    items = Column(JSON, nullable=False)
    total_price = Column(Integer, nullable=False)
    status = Column(String, nullable=False)

# Create the tables in the database
Base.metadata.create_all(bind=engine)
