from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from crud import QuoteCRUD
from models import Quote, QuoteCreate, QuoteUpdate, QuoteResponse

router = APIRouter(prefix="/quotes", tags=["quotes"])

@router.get("/", response_model=List[Quote])
def read_quotes(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    crud = QuoteCRUD(db)
    if category:
        return crud.get_quotes_by_category(category)
    return crud.get_all_quotes(skip=skip, limit=limit)

@router.get("/random", response_model=QuoteResponse)
def get_random_quote(
    category: Optional[str] = Query(None, description="Filter by category"),
    db: Session = Depends(get_db)
):
    crud = QuoteCRUD(db)
    if category:
        quote = crud.get_random_quote_by_category(category)
        if not quote:
            return QuoteResponse(
                success=False,
                message=f"No quotes found in category: {category}"
            )
    else:
        quote = crud.get_random_quote()
        if not quote:
            return QuoteResponse(
                success=False,
                message="No quotes available"
            )
    
    return QuoteResponse(
        success=True,
        data=quote,
        message="Random quote retrieved successfully"
    )

@router.get("/{quote_id}", response_model=QuoteResponse)
def read_quote(quote_id: int, db: Session = Depends(get_db)):
    crud = QuoteCRUD(db)
    quote = crud.get_quote(quote_id)
    if not quote:
        return QuoteResponse(
            success=False,
            message=f"Quote with ID {quote_id} not found"
        )
    
    return QuoteResponse(
        success=True,
        data=quote,
        message="Quote retrieved successfully"
    )

@router.post("/", response_model=QuoteResponse)
def create_quote(quote: QuoteCreate, db: Session = Depends(get_db)):
    crud = QuoteCRUD(db)
    db_quote = crud.create_quote(quote)
    return QuoteResponse(
        success=True,
        data=db_quote,
        message="Quote created successfully"
    )

@router.put("/{quote_id}", response_model=QuoteResponse)
def update_quote(
    quote_id: int, 
    quote_update: QuoteUpdate, 
    db: Session = Depends(get_db)
):
    crud = QuoteCRUD(db)
    updated_quote = crud.update_quote(quote_id, quote_update)
    if not updated_quote:
        return QuoteResponse(
            success=False,
            message=f"Quote with ID {quote_id} not found"
        )
    
    return QuoteResponse(
        success=True,
        data=updated_quote,
        message="Quote updated successfully"
    )

@router.delete("/{quote_id}")
def delete_quote(quote_id: int, db: Session = Depends(get_db)):
    crud = QuoteCRUD(db)
    success = crud.delete_quote(quote_id)
    if not success:
        raise HTTPException(status_code=404, detail="Quote not found")
    
    return {"success": True, "message": "Quote deleted successfully"}

@router.get("/categories/list")
def get_categories(db: Session = Depends(get_db)):
    crud = QuoteCRUD(db)
    categories = crud.get_categories()
    return {
        "success": True,
        "categories": categories,
        "count": len(categories)
    }