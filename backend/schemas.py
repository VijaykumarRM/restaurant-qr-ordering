from pydantic import BaseModel, EmailStr


# -------------------------
# Restaurant
# -------------------------

class RestaurantCreate(BaseModel):
    name: str
    email: EmailStr


class RestaurantResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


# -------------------------
# Table
# -------------------------

class TableCreate(BaseModel):
    table_number: int


class TableResponse(BaseModel):
    id: int
    restaurant_id: int
    table_number: int
    qr_token: str
    active: bool

    class Config:
        from_attributes = True


# -------------------------
# Order
# -------------------------

class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int = 1


class OrderCreate(BaseModel):
    token: str
    items: list[OrderItemCreate]
    points_to_use: int = 0


class OrderItemResponse(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    unit_price: float
    total_price: float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    restaurant_id: int
    table_id: int
    order_code: str
    status: str
    total_amount: float
    points_used: int = 0
    discount_amount: float = 0.0
    points_earned: int = 0
    items: list[OrderItemResponse]

    class Config:
        from_attributes = True


class PaymentCreate(BaseModel):
    amount: float
    payment_method: str = "cash"


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    amount: float
    payment_method: str
    status: str

    class Config:
        from_attributes = True


class PayOrderResponse(BaseModel):
    order: OrderResponse
    payment: PaymentResponse

    class Config:
        from_attributes = True


# -------------------------
# Menu Item
# -------------------------

class MenuItemCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    category: str
    image_url: str | None = None
    available: bool = True


class MenuItemResponse(BaseModel):
    id: int
    restaurant_id: int
    name: str
    description: str | None = None
    price: float
    category: str
    image_url: str | None = None
    available: bool

    class Config:
        from_attributes = True