from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    Enum,
    Text,
    Float,
    ForeignKey,
    Table
)
from sqlalchemy.orm import relationship

from database import Base


class UserRoleEnum(Enum):
    SELLER = 'продавец'
    BUYER = 'покупатель'
    ADMIN = 'администратор'


class OrderStatusEnum(Enum):
    NEW = 'новый'
    PROCESSING = 'в обработке'
    SHIPPED = 'отправлен'
    DELIVERED = 'доставлен'


class User(Base):
    """
    Модель пользователя.

    Пользователь может быть продавцом, покупателем или администратором.
    По умолчанию: покупатель.
    Пользователь может делать заказы и оставлять отзывы на продукты.

    Связана с моделью магазина отношением один-к-одному (один пользователь
    может владеть одним магазином, у одного магазина может быть один владелец).
    Связана с моделью отзывов отношением один-ко-многим (один пользователь
    может оставить несколько отзывов).
    Связана с моделью заказов отношением один-ко-многим (один пользователь
    может сделать несколько заказов).
    """

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(50))
    add_date = Column(DateTime(), default=datetime.now)
    image_path = Column(String)
    user_role = Column(Enum(UserRoleEnum), default='покупатель')
    shop = relationship('Shop', backref='owner', uselist=False)
    reviews = relationship('Review', backref='review')
    orders = relationship('Order', backref='order')


class Shop(Base):
    """
    Модель магазина.

    Магазин принадлежит пользователю-продавцу и предоставляет продукты
    различных категорий.

    Связана с моделью пользователя отношением один-к-одному (один пользователь
    может владеть одним магазином, у одного магазина может быть один владелец).
    Связана с моделью продукта отношением один-ко-многим (в магазине может
    быть несколько товаров).
    """

    __tablename__ = 'shops'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(50))
    add_date = Column(DateTime(), default=datetime.now)
    image_path = Column(String)
    description = Column(Text)
    rating = Column(Float, nullable=False)
    user_id = Column(Integer(), ForeignKey('users.id'))
    owner = relationship('User', uselist=False)
    products = relationship('Product', backref='product')


class Category(Base):
    """
    Модель категории.

    Каждый продукт принадлежит определенной категории.

    Связана с моделью продукта отношением один-ко-многим (к одной категории
    может принадлежать несколько продуктов).
    """

    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False)
    products = relationship('Product', backref='product')


product_order = Table(
    'product_order',
    Base.metadata,
    Column('product_id', Integer(), ForeignKey('products.id')),
    Column('order_id', Integer(), ForeignKey('orders.id'))
)


class Product(Base):
    """
    Модель продукта.

    Продукты представлены в магазинах. Каждый продукт относится к определенной
    категории, может иметь несколько отзывов, оставленных пользователями, и
    может быть неоднократно заказан.

    Связана с моделью магазина отнощением один-ко-многим (в магазине может быть
    несколько товаров).
    Связана с моделью категории отношением один-ко-многим (один продукт
    относится к одной категории, в одной категории может быть несколько
    продуктов).
    Связана с моделью отзывов отношением один-ко многим (у одного продукта
    может быть несколько отзывов, один отзыв оставляется на один продукт).
    Связана с моделью заказов отношением многие-ко-многим (в одном заказе
    может быть несколько продуктов, один продукт может быть заказан много раз).
    """

    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    image_path = Column(String)
    rating = Column(Float, nullable=False)
    shop_id = Column(Integer(), ForeignKey('shops.id'))
    shop = relationship('Shop')
    category_id = Column(Integer(), ForeignKey('categories.id'))
    category = relationship('Category')
    reviews = relationship('Review', backref='review')
    orders = relationship('Order', secondary=product_order, backref='order')


class Order(Base):
    """
    Модель для заказов.

    Пользователь делает заказ продукта.

    Связана с моделью пользователя отношением один-ко-многим (один
    пользователь может сделать несколько заказов, конкретный заказ принадлежит
    конкретному пользователю).
    Связана с моделью продукта отношением многие-ко-многим (в одном заказе
    может быть несколько продуктов, один продукт может быть заказан много раз).
    """

    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    add_date = Column(DateTime(), default=datetime.now)
    delivery_date = Column(DateTime())
    order_status = Column(Enum(OrderStatusEnum), default='новый')
    user_id = Column(Integer(), ForeignKey('users.id'))
    user = relationship('User')
    ordered_products = relationship('Product', secondary=product_order)


class Review(Base):
    """
    Модель отзыва.

    Пользователь может оставить отзыв на продукт.

    Модель отзыва имеет связи один-ко-многим с моделью пользователя (один
    пользователь может оставить несколько отзывов) и один-ко-многим с моделью
    продукта (один продукт может иметь несколько отзывов).
    """

    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    review_text = Column(Text)
    add_date = Column(DateTime(), default=datetime.now)
    user_id = Column(Integer(), ForeignKey('users.id'))
    user = relationship('User')
    product_id = Column(Integer(), ForeignKey('products.id'))
    product = relationship('Product')
