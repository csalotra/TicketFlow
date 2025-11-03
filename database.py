from sqlmodel import create_engine, SQLModel, Session
import os

# SQLite database file path
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the database engine
engine = create_engine(DATABASE_URL, echo=False)

# Dependency to get DB session
def get_session():
    with Session(engine) as session:
        yield session

# Initialize database and create all tables
def init_db():
    from models import User, Ticket
    SQLModel.metadata.create_all(engine)
