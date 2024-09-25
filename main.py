from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from models import Product, Sale,  SessionLocal, Base, engine
from typing import Optional

# Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/products')
async def get_products(search_keyword: Optional[str] = None, db: Session = Depends(get_db)):
    if search_keyword is None:
        products = db.query(Product).all()
    else:
        search = "%{}%".format(search_keyword)
        products = db.query(Product).filter(
            Product.name.like(search) | Product.description.like(search) | Product.category.like(search)
        ).all()
    if len(products) == 0:
        raise HTTPException(status_code=404, detail="Products not available")
    return products


@app.post('/create-product')
async def create_products(item: dict, db: Session = Depends(get_db)):
    db_product = Product(**item)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.post('/product/{id}')
async def update_products(id: int, item: dict, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if 'name' in item:
        product.name = item.get('name')
    if 'description' in item:
        product.description = item.get('description')
    if 'inventory_count' in item:
        product.inventory_count = item.get('inventory_count')
    if 'price' in item:
        product.price = item.get('price')
    if 'category' in item:
        product.category = item.get('category')

    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@app.get('/product/{id}')
async def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.delete('/product/{id}')
async def delete_product(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"msg": "Product deleted successfully!"}
