from .connection import Base, SessionLocal, engine

def get_db():
    """
    Helper function used to get a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()