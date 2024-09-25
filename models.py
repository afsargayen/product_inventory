from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from urllib.parse import quote_plus

pwd = quote_plus("ows@123")

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://root:{pwd}@mysql_container/test_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), index=True)
    description = Column(String(255), index=True)
    price = Column(Float, index=True)
    inventory_count = Column(Integer)
    category = Column(String(64), index=True)

    product_sales = relationship("Sale", back_populates="product")



class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    total_price = Column(Float, index=True)

    product = relationship("Product", back_populates="product_sales")
