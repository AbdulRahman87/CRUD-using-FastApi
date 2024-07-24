from sqlalchemy.orm import Session
from . import models, schemas


def get_item(db: Session, item_id: int):
    """Fetches the Item from the database based on the item's id"""
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 100):
    """Fetches all the Items from the database"""
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_item(db: Session, item: schemas.ItemCreate):
    """Used to insert a row in the Item table"""
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item: schemas.ItemCreate):
    """Used to update the existing row in the Item table"""
    db_item = get_item(db, item_id)
    db_item.name = item.name # type: ignore
    db_item.description = item.description # type: ignore
    db_item.price = item.price # type: ignore
    db_item.quantity = item.quantity # type: ignore
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    """Used to delete the existing row from the Item table"""
    db_item = get_item(db, item_id)
    db.delete(db_item)
    db.commit()
    
def search_items(db: Session, query: str):
    """Used to search the Items based on name, description, quantity (partial match for name & description and exact match for quantity of Items"""
    try:
        quantity = int(query)
        return db.query(models.Item).filter(models.Item.quantity == quantity).all()
    except Exception as e:
        query1 = db.query(models.Item).filter(models.Item.name.contains(query))
        query2 = db.query(models.Item).filter(models.Item.description.contains(query))
        return query1.union(query2).all()
    
def filter_items_by_id_range(db: Session, min_range: int, max_range: int):
    """User to filter the Items from minimum price range to maximum price range"""
    return db.query(models.Item).filter(models.Item.price >= min_range, models.Item.price <= max_range).all()