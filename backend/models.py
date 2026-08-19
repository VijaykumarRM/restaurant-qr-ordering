from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Float,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    upi_id = Column(String(100), nullable=True, default="vijaycafe@upi")
    created_at = Column(DateTime, default=datetime.utcnow)

    tables = relationship(
        "RestaurantTable",
        back_populates="restaurant",
        cascade="all, delete-orphan"
    )

    menu_items = relationship(
        "MenuItem",
        back_populates="restaurant",
        cascade="all, delete-orphan"
    )

    orders = relationship(
        "Order",
        back_populates="restaurant",
        cascade="all, delete-orphan"
    )


class RestaurantTable(Base):
    __tablename__ = "restaurant_tables"

    id = Column(Integer, primary_key=True, index=True)

    restaurant_id = Column(
        Integer,
        ForeignKey("restaurants.id"),
        nullable=False
    )

    table_number = Column(Integer, nullable=False)

    # Random secure token used by the QR code
    qr_token = Column(
        String(128),
        unique=True,
        nullable=False,
        index=True
    )

    active = Column(Boolean, default=True)
    points_balance = Column(Integer, default=0)

    restaurant = relationship(
        "Restaurant",
        back_populates="tables"
    )

    orders = relationship(
        "Order",
        back_populates="table",
        cascade="all, delete-orphan"
    )


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)

    restaurant_id = Column(
        Integer,
        ForeignKey("restaurants.id"),
        nullable=False
    )

    name = Column(String(150), nullable=False)

    description = Column(String(500), nullable=True)

    price = Column(Float, nullable=False)

    category = Column(String(100), nullable=False)

    image_url = Column(String(500), nullable=True)

    available = Column(Boolean, default=True)

    restaurant = relationship(
        "Restaurant",
        back_populates="menu_items"
    )

    order_items = relationship(
        "OrderItem",
        back_populates="menu_item",
        cascade="all, delete-orphan"
    )


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    table_id = Column(Integer, ForeignKey("restaurant_tables.id"), nullable=False)
    order_code = Column(String(50), unique=True, nullable=False, index=True)
    status = Column(String(50), default="pending")
    total_amount = Column(Float, default=0.0)
    points_used = Column(Integer, default=0)
    discount_amount = Column(Float, default=0.0)
    points_earned = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    restaurant = relationship("Restaurant", back_populates="orders")
    table = relationship("RestaurantTable", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payment = relationship("Payment", back_populates="order", uselist=False, cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem", back_populates="order_items")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True, nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(String(50), nullable=False, default="cash")
    status = Column(String(50), nullable=False, default="pending")
    paid_at = Column(DateTime, nullable=True)

    order = relationship("Order", back_populates="payment")