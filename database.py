from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# SQLite database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./quotes.db"

# Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize with sample data
def init_sample_data():
    db = SessionLocal()
    try:
        from models import QuoteDB
        
        # Check if we already have data
        existing_quotes = db.query(QuoteDB).count()
        if existing_quotes == 0:
            sample_quotes = [
                QuoteDB(
                    text="The only way to do great work is to love what you do.",
                    author="Steve Jobs",
                    category="inspiration"
                ),
                QuoteDB(
                    text="Life is what happens when you're busy making other plans.",
                    author="John Lennon",
                    category="life"
                ),
                QuoteDB(
                    text="The future belongs to those who believe in the beauty of their dreams.",
                    author="Eleanor Roosevelt",
                    category="dreams"
                ),
                QuoteDB(
                    text="It is during our darkest moments that we must focus to see the light.",
                    author="Aristotle",
                    category="motivation"
                ),
                QuoteDB(
                    text="Whoever is happy will make others happy too.",
                    author="Anne Frank",
                    category="happiness"
                )
            ]
            
            db.add_all(sample_quotes)
            db.commit()
            print("Sample data initialized!")
    except Exception as e:
        print(f"Error initializing sample data: {e}")
    finally:
        db.close()