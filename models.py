from database import Base,Session, engine
from sqlalchemy import Column,Integer,Boolean,Text,String,ForeignKey, Enum, Numeric
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy.orm import relationship

session = Session(bind=engine)

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    email = Column(String(80), unique=True, nullable=False)
    firstname = Column(String(25), nullable=False)
    lastname = Column(String(25), nullable=False)
    password = Column(Text, nullable=False)
    phone_number = Column(String(10), nullable=True)
    is_seller = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)
    is_buyer = Column(Boolean, default=True)
    profile_picture = Column(String, nullable=True)

    sellers = relationship("Seller", back_populates="user")

    def __repr__(self):
        return f"<User {self.email}>"
    
class Seller(Base):
    __tablename__ = "sellers"

    seller_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    location = Column(String)
    subcounty = Column(String)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="sellers")
    products = relationship("Product", back_populates="seller")

    def __repr__(self):
        return f"<Seller {self.seller_id}>" 
           
class Image(Base):
    __tablename__ = 'images'

    image_id = Column(Integer, primary_key=True)
    file_path = Column(String(255))
    product_id = Column(Integer, ForeignKey('products.product_id'))

    product = relationship("Product", back_populates="images")
    
    def __repr__(self):
        return f"<Image {self.image_id}>"
      
class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String(80), nullable=False)
    description = Column(String(255), nullable=False)
    category = Column(String(25), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
    county = Column(String(25), nullable=False)
    subcounty = Column(String(25), nullable=False)
    image = Column(String(255), nullable=False)
    negotiable = Column(Boolean, default=False)
    per_type = Enum('seedling', 'kg', 'bulk', name='per', create_type=False)
    per = Column(per_type, nullable=False, default='seedling')
    seller_id = Column(Integer, ForeignKey('sellers.seller_id'))

    seller = relationship("Seller", back_populates="products")
    images = relationship("Image", back_populates="product")

    def __repr__(self):
        return f"<Product {self.product_id}>"

