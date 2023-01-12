from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///inventory.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True)
    product_name = Column("Product Name", String)
    product_quantity = Column("Amount", Integer)
    product_price = Column("Price", Integer)
    date_updated = Column("Updated", Date)


def __repr__(self):
    return f'Name: {self.product_name}\nAmount: {self.product_quantity}\nPrice: {self.product_price}\nDate: {self.date_updated}'
