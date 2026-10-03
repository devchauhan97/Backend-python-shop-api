from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker
import urllib.parse
# 1. Update this with your actual MySQL credentials
# Format: mysql+pymysql://USERNAME:PASSWORD@HOST:PORT/DATABASE_NAME

#local
#DATABASE_URL = "mysql+pymysql://root:my-secret-pw@localhost:3306/database_test"

password = urllib.parse.quote_plus("root-user")

## rds connectqion string with 
# DATABASE_URL=f"mysql+pymysql://admin:{password}@database-test.csd8q0c8sr1h.us-east-1.rds.amazonaws.com:3306/database_test"

## ec2 and rds connectqion string connection string 
DATABASE_URL = f"mysql+pymysql://admin:{password}@localhost:3307/database_test"

# 2. Create the engine that communicates with MySQL
engine = create_engine(DATABASE_URL)

# 3. Create a session factory to handle queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. The base class that our models will inherit from (Like Eloquent Model class)
Base = declarative_base()


def test_db_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except SQLAlchemyError as exc:
        raise RuntimeError(f"Database connection failed: {exc}") from exc


# Dependency to open/close DB connection per API request
def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as exc:
        db.rollback()
        raise RuntimeError(f"Database operation failed: {exc}") from exc
    finally:
        db.close()