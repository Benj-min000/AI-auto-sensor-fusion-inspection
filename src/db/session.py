from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.models import Base

# Define the SQLite database URL
# This will create a file named 'quality_platform.db' in your project root
SQLALCHEMY_DATABASE_URL = "sqlite:///./quality_platform.db"

# Create the SQLAlchemy engine
# connect_args={"check_same_thread": False} is needed only for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# When this script is run directly, it will create the tables
if __name__ == "__main__":
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
