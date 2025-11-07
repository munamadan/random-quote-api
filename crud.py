from sqlalchemy.orm import Session
from models import QuoteDB, QuoteCreate, QuoteUpdate
from typing import List, Optional
import random

class QuoteCRUD:
    def __init__(self, db: Session):
        self.db = db
    
    def get_quote(self, quote_id: int) -> Optional[QuoteDB]:
        return self.db.query(QuoteDB).filter(QuoteDB.id == quote_id).first()
    
    def get_all_quotes(self, skip: int = 0, limit: int = 100) -> List[QuoteDB]:
        return self.db.query(QuoteDB).offset(skip).limit(limit).all()
    
    def get_quotes_by_category(self, category: str) -> List[QuoteDB]:
        return self.db.query(QuoteDB).filter(QuoteDB.category == category).all()
    
    def get_random_quote(self) -> Optional[QuoteDB]:
        all_quotes = self.db.query(QuoteDB).all()
        return random.choice(all_quotes) if all_quotes else None
    
    def get_random_quote_by_category(self, category: str) -> Optional[QuoteDB]:
        category_quotes = self.get_quotes_by_category(category)
        return random.choice(category_quotes) if category_quotes else None
    
    def create_quote(self, quote: QuoteCreate) -> QuoteDB:
        db_quote = QuoteDB(
            text=quote.text,
            author=quote.author,
            category=quote.category
        )
        self.db.add(db_quote)
        self.db.commit()
        self.db.refresh(db_quote)
        return db_quote
    
    def update_quote(self, quote_id: int, quote_update: QuoteUpdate) -> Optional[QuoteDB]:
        db_quote = self.get_quote(quote_id)
        if db_quote:
            update_data = quote_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_quote, field, value)
            self.db.commit()
            self.db.refresh(db_quote)
        return db_quote
    
    def delete_quote(self, quote_id: int) -> bool:
        db_quote = self.get_quote(quote_id)
        if db_quote:
            self.db.delete(db_quote)
            self.db.commit()
            return True
        return False
    
    def get_categories(self) -> List[str]:
        categories = self.db.query(QuoteDB.category).distinct().all()
        return [cat[0] for cat in categories]