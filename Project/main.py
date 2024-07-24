from fastapi import FastAPI, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """Inserts a new row in the Item table on POST Request"""
    return crud.create_item(db=db, item=item)

@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Fetches all the Items from the database"""
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    """Fetches the Item from database based on the Item's id"""
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.put("/items/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """Updates the existing row of Item table corresponding to the given Item's id"""
    return crud.update_item(db=db, item_id=item_id, item=item)

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Deletes the Item from Item table based on Item's id"""
    crud.delete_item(db=db, item_id=item_id)
    return {"message": "Item deleted successfully"}

@app.get("/items/search/", response_model=list[schemas.Item])
def search_items(query: str, db: Session = Depends(get_db)):
    """Searches the Item based on the Item's name, description & quantity"""
    items = crud.search_items(db, query)
    return items

@app.get("/items/filter/", response_model=list[schemas.Item])
def filter_items(min_range: int, max_range: int, db: Session = Depends(get_db)):
    """Filters the Item based on minimum and maximum price range"""
    items = crud.filter_items_by_id_range(db, min_range, max_range)
    return items