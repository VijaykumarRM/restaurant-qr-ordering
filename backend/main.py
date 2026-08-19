from fastapi import FastAPI, Depends, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import secrets
import os
import json
import urllib.request

from .database import Base, engine, get_db
from .models import Restaurant, RestaurantTable, MenuItem, Order, OrderItem, Payment
from .qr_generator import generate_menu_item_qr
from .schemas import (
    RestaurantCreate,
    RestaurantResponse,
    TableCreate,
    TableResponse,
    OrderCreate,
    OrderResponse,
    OrderItemResponse,
    PaymentCreate,
    PaymentResponse,
    PayOrderResponse,
    MenuItemCreate,
    MenuItemResponse,
)


# ============================================================
# DATABASE
# ============================================================

Base.metadata.create_all(bind=engine)


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="Restaurant QR Ordering API",
    description="QR-based restaurant ordering and loyalty platform",
    version="1.0.0",
)


# ============================================================
# CORS — allow everything for local dev
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")


# ============================================================
# AUTO-SEED ON STARTUP (Render has ephemeral storage)
# ============================================================

@app.on_event("startup")
def auto_seed():
    """Auto-seed demo data on startup so Render deployments always have data."""
    from .database import SessionLocal
    db = SessionLocal()
    try:
        existing = db.query(Restaurant).first()
        if not existing:
            print("⚡ No data found — auto-seeding demo restaurant...")
            restaurant = Restaurant(name="Vijay Cafe", email="vijay@cafe.com", upi_id="vijaycafe@upi")
            db.add(restaurant)
            db.flush()

            for i in range(1, 6):
                qr_token = secrets.token_urlsafe(32)
                table = RestaurantTable(
                    restaurant_id=restaurant.id,
                    table_number=i,
                    qr_token=qr_token,
                )
                db.add(table)

            items = [
                ("Masala Dosa", "Crispy crepe with spiced potato filling", 120.0, "South Indian", "https://images.unsplash.com/photo-1630383249896-424e482df921?w=400"),
                ("Idli Sambar", "Steamed rice cakes with lentil soup", 80.0, "South Indian", "https://images.unsplash.com/photo-1589301760014-d929f39ce9b1?w=400"),
                ("Medu Vada", "Crispy lentil donuts", 90.0, "South Indian", "https://images.unsplash.com/photo-1626132647523-66f5bf380027?w=400"),
                ("Paneer Tikka", "Grilled cottage cheese marinated in spices", 240.0, "Starters", "https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=400"),
                ("Chicken 65", "Spicy, deep-fried chicken starter", 280.0, "Starters", "https://images.unsplash.com/photo-1610057099443-fde8c4d50f91?w=400"),
                ("Crispy Corn", "Fried sweet corn tossed in spices", 180.0, "Starters", "https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=400"),
                ("Gobi Manchurian", "Indo-Chinese fried cauliflower", 200.0, "Starters", "https://images.unsplash.com/photo-1645177628172-a94c1f96e6db?w=400"),
                ("Butter Chicken", "Rich creamy tomato chicken curry", 350.0, "Main Course", "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=400"),
                ("Paneer Butter Masala", "Cottage cheese in rich tomato gravy", 300.0, "Main Course", "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=400"),
                ("Dal Makhani", "Slow-cooked black lentils", 220.0, "Main Course", "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=400"),
                ("Garlic Naan", "Flatbread baked with minced garlic", 60.0, "Main Course", "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400"),
                ("Hyderabadi Chicken Biryani", "Authentic dum biryani with raita", 380.0, "Biryani", "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=400"),
                ("Mutton Dum Biryani", "Slow-cooked tender mutton biryani", 450.0, "Biryani", "https://images.unsplash.com/photo-1642821373181-696a54913e93?w=400"),
                ("Margherita Pizza", "Classic cheese and tomato pizza", 299.0, "Fast Food", "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400"),
                ("Premium Veg Burger", "Crispy veg patty with cheese and fries", 199.0, "Fast Food", "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400"),
                ("Cold Coffee", "Chilled milk blended with rich coffee", 150.0, "Beverages", "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=400"),
                ("Oreo Shake", "Thick shake blended with Oreo cookies", 180.0, "Beverages", "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=400"),
                ("Fresh Lime Soda", "Refreshing sweet and salty lime soda", 90.0, "Beverages", "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=400"),
                ("Gulab Jamun", "Soft cottage cheese dumplings in sugar syrup", 120.0, "Desserts", "https://images.unsplash.com/photo-1666190020823-53629626d89f?w=400"),
                ("Sizzling Brownie", "Hot brownie with vanilla ice cream", 250.0, "Desserts", "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=400"),
            ]

            for name, desc, price, category, img in items:
                db.add(MenuItem(
                    restaurant_id=restaurant.id, name=name, description=desc,
                    price=price, category=category, image_url=img, available=True,
                ))

            db.commit()
            print("✅ Demo data seeded successfully!")
        else:
            print("✅ Database already has data — skipping seed.")
    except Exception as e:
        print(f"⚠️ Auto-seed error: {e}")
        db.rollback()
    finally:
        db.close()


# ============================================================
# FRONTEND HTML ROUTES
# ============================================================

@app.get("/", response_class=HTMLResponse)
def serve_home():
    """Redirect to admin dashboard."""
    return """
    <!DOCTYPE html>
    <html>
    <head><meta http-equiv="refresh" content="0; url=/admin"></head>
    <body><p>Redirecting to <a href="/admin">Admin Dashboard</a>...</p></body>
    </html>
    """


@app.get("/admin", response_class=HTMLResponse)
def serve_admin():
    """Serve the admin dashboard."""
    admin_path = os.path.join(FRONTEND_DIR, "admin.html")
    if os.path.exists(admin_path):
        with open(admin_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Admin page not found</h1>", status_code=404)


@app.get("/customer-menu", response_class=HTMLResponse)
def serve_menu():
    """Serve the customer menu page."""
    menu_path = os.path.join(FRONTEND_DIR, "menu.html")
    if os.path.exists(menu_path):
        with open(menu_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Menu page not found</h1>", status_code=404)


@app.get("/kitchen", response_class=HTMLResponse)
def serve_kitchen():
    """Serve the kitchen display system page."""
    kitchen_path = os.path.join(FRONTEND_DIR, "kitchen.html")
    if os.path.exists(kitchen_path):
        with open(kitchen_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Kitchen page not found</h1>", status_code=404)

@app.get("/manifest.json")
def serve_manifest():
    return FileResponse(os.path.join(FRONTEND_DIR, "manifest.json"))

@app.get("/sw.js")
def serve_sw():
    return FileResponse(os.path.join(FRONTEND_DIR, "sw.js"))


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


# ============================================================
# SEED DATA — creates demo restaurant, tables, and menu items
# ============================================================

@app.post("/seed")
def seed_data(db: Session = Depends(get_db)):
    """Create sample restaurant, tables, and menu items for demo."""
    # Check if already seeded
    existing = db.query(Restaurant).first()
    if existing:
        return {"success": True, "message": "Data already exists", "restaurant_id": existing.id}

    # Create restaurant
    restaurant = Restaurant(
        name="Vijay Cafe",
        email="vijay@cafe.com",
        upi_id="vijaycafe@upi",
    )
    db.add(restaurant)
    db.flush()

    # Create tables
    tables_data = []
    for i in range(1, 6):
        qr_token = secrets.token_urlsafe(32)
        table = RestaurantTable(
            restaurant_id=restaurant.id,
            table_number=i,
            qr_token=qr_token,
        )
        db.add(table)
        tables_data.append({"table_number": i, "qr_token": qr_token})

    # Create menu items
    if not db.query(MenuItem).first():
        items = [
            # South Indian
            ("Masala Dosa", "Crispy crepe with spiced potato filling", 120.0, "South Indian", "https://images.unsplash.com/photo-1630383249896-424e482df921?w=400"),
            ("Idli Sambar", "Steamed rice cakes with lentil soup", 80.0, "South Indian", "https://images.unsplash.com/photo-1589301760014-d929f39ce9b1?w=400"),
            ("Medu Vada", "Crispy lentil donuts", 90.0, "South Indian", "https://images.unsplash.com/photo-1626132647523-66f5bf380027?w=400"),
            
            # Starters
            ("Paneer Tikka", "Grilled cottage cheese marinated in spices", 240.0, "Starters", "https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=400"),
            ("Chicken 65", "Spicy, deep-fried chicken starter", 280.0, "Starters", "https://images.unsplash.com/photo-1610057099443-fde8c4d50f91?w=400"),
            ("Crispy Corn", "Fried sweet corn tossed in spices", 180.0, "Starters", "https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=400"),
            ("Gobi Manchurian", "Indo-Chinese fried cauliflower", 200.0, "Starters", "https://images.unsplash.com/photo-1645177628172-a94c1f96e6db?w=400"),
            
            # North Indian / Main Course
            ("Butter Chicken", "Rich creamy tomato chicken curry", 350.0, "Main Course", "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=400"),
            ("Paneer Butter Masala", "Cottage cheese in rich tomato gravy", 300.0, "Main Course", "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=400"),
            ("Dal Makhani", "Slow-cooked black lentils", 220.0, "Main Course", "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=400"),
            ("Garlic Naan", "Flatbread baked with minced garlic", 60.0, "Main Course", "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400"),
            ("Jeera Rice", "Basmati rice tempered with cumin", 150.0, "Main Course", "https://images.unsplash.com/photo-1596560548464-f010549b84d7?w=400"),
            
            # Biryani
            ("Hyderabadi Chicken Biryani", "Authentic dum biryani with raita", 380.0, "Biryani", "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=400"),
            ("Mutton Dum Biryani", "Slow-cooked tender mutton biryani", 450.0, "Biryani", "https://images.unsplash.com/photo-1642821373181-696a54913e93?w=400"),
            ("Paneer Biryani", "Fragrant rice with spiced paneer cubes", 300.0, "Biryani", "https://images.unsplash.com/photo-1633945274405-b6c8069047b0?w=400"),

            # Fast Food
            ("Margherita Pizza", "Classic cheese and tomato pizza", 299.0, "Fast Food", "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400"),
            ("Premium Veg Burger", "Crispy veg patty with cheese and fries", 199.0, "Fast Food", "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400"),
            ("Spicy Chicken Burger", "Fried chicken breast with spicy mayo", 249.0, "Fast Food", "https://images.unsplash.com/photo-1553979459-d2229ba7433b?w=400"),

            # Beverages & Shakes
            ("Cold Coffee", "Chilled milk blended with rich coffee", 150.0, "Beverages", "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=400"),
            ("Oreo Shake", "Thick shake blended with Oreo cookies", 180.0, "Beverages", "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=400"),
            ("Fresh Lime Soda", "Refreshing sweet and salty lime soda", 90.0, "Beverages", "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=400"),
            
            # Desserts
            ("Gulab Jamun", "Soft cottage cheese dumplings in sugar syrup", 120.0, "Desserts", "https://images.unsplash.com/photo-1666190020823-53629626d89f?w=400"),
            ("Sizzling Brownie", "Hot brownie with vanilla ice cream", 250.0, "Desserts", "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=400")
        ]
        
        for name, desc, price, category, img in items:
            menu_item = MenuItem(
                restaurant_id=restaurant.id,
                name=name,
                description=desc,
                price=price,
                category=category,
                image_url=img,
                available=True,
            )
            db.add(menu_item)

    db.commit()
    db.refresh(restaurant)

    return {
        "success": True,
        "message": "Demo data seeded successfully!",
        "restaurant_id": restaurant.id,
        "tables": tables_data,
        "menu_items_count": len(items),
    }


# ============================================================
# GET ALL RESTAURANTS
# ============================================================

@app.get("/restaurants")
def get_restaurants(
    db: Session = Depends(get_db)
):
    restaurants = db.query(Restaurant).all()

    return {
        "success": True,
        "restaurants": [
            {
                "id": restaurant.id,
                "name": restaurant.name,
                "email": restaurant.email,
                "upi_id": getattr(restaurant, "upi_id", "vijaycafe@upi") or "vijaycafe@upi",
            }
            for restaurant in restaurants
        ],
    }


# ============================================================
# CREATE RESTAURANT
# ============================================================

@app.post(
    "/restaurants",
    response_model=RestaurantResponse,
)
def create_restaurant(
    restaurant: RestaurantCreate,
    db: Session = Depends(get_db),
):
    existing = (
        db.query(Restaurant)
        .filter(Restaurant.email == restaurant.email)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Restaurant with this email already exists",
        )

    new_restaurant = Restaurant(
        name=restaurant.name,
        email=restaurant.email,
        upi_id=restaurant.upi_id,
    )

    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)

    return new_restaurant

# ============================================================
# UPDATE RESTAURANT
# ============================================================

@app.patch("/restaurants/{restaurant_id}")
def update_restaurant_settings(
    restaurant_id: int,
    payload: dict,
    db: Session = Depends(get_db)
):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    if "upi_id" in payload:
        restaurant.upi_id = payload["upi_id"]
    if "name" in payload:
        restaurant.name = payload["name"]
    if "email" in payload:
        restaurant.email = payload["email"]
        
    db.commit()
    db.refresh(restaurant)
    return {
        "success": True,
        "restaurant": {
            "id": restaurant.id,
            "name": restaurant.name,
            "email": restaurant.email,
            "upi_id": restaurant.upi_id
        }
    }


# ============================================================
# TABLES
# ============================================================

@app.get("/restaurants/{restaurant_id}/tables")
def get_tables(
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == restaurant_id)
        .first()
    )

    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    tables = (
        db.query(RestaurantTable)
        .filter(RestaurantTable.restaurant_id == restaurant_id)
        .all()
    )

    return {
        "success": True,
        "restaurant_id": restaurant_id,
        "tables": [
            {
                "id": table.id,
                "table_number": table.table_number,
                "qr_token": table.qr_token,
                "active": table.active
            }
            for table in tables
        ]
    }


@app.post(
    "/restaurants/{restaurant_id}/tables",
    response_model=TableResponse,
)
def create_table(
    restaurant_id: int,
    table: TableCreate,
    db: Session = Depends(get_db),
):
    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == restaurant_id)
        .first()
    )

    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found",
        )

    if table.table_number <= 0:
        raise HTTPException(
            status_code=400,
            detail="Table number must be greater than zero",
        )

    existing_table = (
        db.query(RestaurantTable)
        .filter(
            RestaurantTable.restaurant_id == restaurant_id,
            RestaurantTable.table_number == table.table_number,
        )
        .first()
    )

    if existing_table:
        raise HTTPException(
            status_code=400,
            detail="This table already exists",
        )

    qr_token = secrets.token_urlsafe(32)

    new_table = RestaurantTable(
        restaurant_id=restaurant_id,
        table_number=table.table_number,
        qr_token=qr_token,
    )

    db.add(new_table)
    db.commit()
    db.refresh(new_table)

    return new_table


# ============================================================
# QR TOKEN → VERIFY TABLE → GET RESTAURANT + MENU
# ============================================================

@app.get("/menu")
def get_menu(
    token: str,
    db: Session = Depends(get_db),
):
    table = (
        db.query(RestaurantTable)
        .filter(
            RestaurantTable.qr_token == token,
            RestaurantTable.active == True,
        )
        .first()
    )

    if not table:
        raise HTTPException(
            status_code=404,
            detail="Invalid or inactive table QR code",
        )

    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == table.restaurant_id)
        .first()
    )

    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found",
        )

    menu_items = (
        db.query(MenuItem)
        .filter(
            MenuItem.restaurant_id == restaurant.id,
            MenuItem.available == True,
        )
        .all()
    )

    menu = []

    for item in menu_items:
        menu.append(
            {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "price": item.price,
                "category": item.category,
                "image_url": item.image_url,
                "available": item.available,
            }
        )

    return {
        "success": True,
        "restaurant": {
            "id": restaurant.id,
            "name": restaurant.name,
            "upi_id": getattr(restaurant, "upi_id", "vijaycafe@upi") or "vijaycafe@upi",
        },
        "table": {
            "id": table.id,
            "number": table.table_number,
        },
        "points_balance": table.points_balance,
        "menu": menu,
        "message": "Table verified successfully",
    }


# ============================================================
# ADD MENU ITEM
# ============================================================

@app.post(
    "/restaurants/{restaurant_id}/menu",
    response_model=MenuItemResponse,
)
def create_menu_item(
    restaurant_id: int,
    item: MenuItemCreate,
    db: Session = Depends(get_db),
):
    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == restaurant_id)
        .first()
    )

    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found",
        )

    if item.price <= 0:
        raise HTTPException(
            status_code=400,
            detail="Price must be greater than zero",
        )

    new_item = MenuItem(
        restaurant_id=restaurant_id,
        name=item.name,
        description=item.description,
        price=item.price,
        category=item.category,
        image_url=item.image_url,
        available=item.available,
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


# ============================================================
# GENERATE MENU ITEM QR CODE
# ============================================================

@app.get("/restaurants/{restaurant_id}/menu/{menu_item_id}/qr")
def get_menu_item_qr(
    restaurant_id: int,
    menu_item_id: int,
    db: Session = Depends(get_db),
):
    """Generate and return a QR code image for a menu item."""
    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == restaurant_id)
        .first()
    )

    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found",
        )

    menu_item = (
        db.query(MenuItem)
        .filter(
            MenuItem.id == menu_item_id,
            MenuItem.restaurant_id == restaurant_id,
        )
        .first()
    )

    if not menu_item:
        raise HTTPException(
            status_code=404,
            detail="Menu item not found",
        )

    qr_path = generate_menu_item_qr(
        name=menu_item.name,
        price=menu_item.price,
        category=menu_item.category,
        description=menu_item.description or "",
        restaurant_id=restaurant_id,
        menu_item_id=menu_item_id,
    )

    return FileResponse(qr_path, media_type="image/png")


# ============================================================
# GET RESTAURANT MENU
# ============================================================

@app.get("/menu/{restaurant_id}")
def get_restaurant_menu(
    restaurant_id: int,
    db: Session = Depends(get_db),
):
    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == restaurant_id)
        .first()
    )

    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found",
        )

    menu_items = (
        db.query(MenuItem)
        .filter(
            MenuItem.restaurant_id == restaurant_id,
            MenuItem.available == True,
        )
        .all()
    )

    menu = []

    for item in menu_items:
        menu.append(
            {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "price": item.price,
                "category": item.category,
                "image_url": item.image_url,
                "available": item.available,
            }
        )

    return {
        "success": True,
        "restaurant": {
            "id": restaurant.id,
            "name": restaurant.name,
        },
        "menu": menu,
    }


# ============================================================
# ORDERS
# ============================================================

@app.get("/restaurants/{restaurant_id}/orders")
def get_restaurant_orders(
    restaurant_id: int,
    db: Session = Depends(get_db),
):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    orders = (
        db.query(Order)
        .filter(Order.restaurant_id == restaurant_id)
        .order_by(Order.created_at.desc())
        .all()
    )

    result = []
    for order in orders:
        payment = db.query(Payment).filter(Payment.order_id == order.id).first()
        result.append({
            "id": order.id,
            "order_code": order.order_code,
            "table_number": order.table.table_number,
            "status": order.status,
            "total_amount": order.total_amount,
            "payment_status": payment.status if payment else "pending",
            "items": [
                {
                    "name": item.menu_item.name,
                    "quantity": item.quantity,
                    "total_price": item.total_price,
                }
                for item in order.items
            ],
        })

    return {
        "success": True,
        "restaurant_id": restaurant_id,
        "orders": result,
    }


def notify_n8n(event_type: str, data: dict):
    n8n_url = os.getenv("N8N_WEBHOOK_URL", "https://your-n8n-domain.com/webhook/restaurant-event")
    try:
        payload = json.dumps({"event": event_type, "data": data}).encode("utf-8")
        req = urllib.request.Request(n8n_url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        print(f"Failed to send webhook to n8n: {e}")


@app.post("/orders", response_model=OrderResponse)
def create_order(
    order_data: OrderCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    table = (
        db.query(RestaurantTable)
        .filter(
            RestaurantTable.qr_token == order_data.token,
            RestaurantTable.active == True,
        )
        .first()
    )

    if not table:
        raise HTTPException(
            status_code=404,
            detail="Invalid or inactive table token",
        )

    if not order_data.items:
        raise HTTPException(
            status_code=400,
            detail="Order must contain at least one item",
        )

    if order_data.points_to_use < 0:
        raise HTTPException(
            status_code=400,
            detail="Points to use cannot be negative",
        )

    if order_data.points_to_use > table.points_balance:
        raise HTTPException(
            status_code=400,
            detail="Not enough loyalty points available",
        )

    order = Order(
        restaurant_id=table.restaurant_id,
        table_id=table.id,
        order_code=f"ORD-{secrets.token_urlsafe(6).upper()}",
        status="pending",
        total_amount=0.0,
        points_used=0,
        discount_amount=0.0,
        points_earned=0,
    )

    db.add(order)
    db.flush()

    total_amount = 0.0
    order_items = []

    for item_data in order_data.items:
        menu_item = (
            db.query(MenuItem)
            .filter(
                MenuItem.id == item_data.menu_item_id,
                MenuItem.restaurant_id == table.restaurant_id,
                MenuItem.available == True,
            )
            .first()
        )

        if not menu_item:
            raise HTTPException(
                status_code=404,
                detail=f"Menu item {item_data.menu_item_id} not found",
            )

        if item_data.quantity <= 0:
            raise HTTPException(
                status_code=400,
                detail="Quantity must be greater than zero",
            )

        unit_price = menu_item.price
        total_price = unit_price * item_data.quantity
        total_amount += total_price

        order_item = OrderItem(
            order_id=order.id,
            menu_item_id=menu_item.id,
            quantity=item_data.quantity,
            unit_price=unit_price,
            total_price=total_price,
        )
        db.add(order_item)
        order_items.append(order_item)

    order.total_amount = total_amount
    
    # 10% discount for orders above ₹1000
    extra_discount = 0.0
    if total_amount >= 1000:
        extra_discount = total_amount * 0.10

    order.points_used = min(order_data.points_to_use, table.points_balance)
    order.discount_amount = float(order.points_used) + extra_discount
    order.total_amount = max(0.0, total_amount - order.discount_amount)
    order.status = "pending"
    db.commit()
    db.refresh(order)

    for order_item in order_items:
        db.refresh(order_item)

    response_data = {
        "id": order.id,
        "restaurant_id": order.restaurant_id,
        "table_id": order.table_id,
        "order_code": order.order_code,
        "status": order.status,
        "total_amount": order.total_amount,
        "points_used": order.points_used,
        "discount_amount": order.discount_amount,
        "points_earned": order.points_earned,
        "items": [
            {
                "id": item.id,
                "menu_item_id": item.menu_item_id,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "total_price": item.total_price,
            }
            for item in order_items
        ],
    }

    # Notify n8n in background
    background_tasks.add_task(notify_n8n, "order_created", response_data)

    return response_data


# ============================================================
# PAY ORDER
# ============================================================

@app.patch("/orders/{order_id}/status")
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = status
    db.commit()
    db.refresh(order)
    return {"status": "success", "new_status": order.status}


@app.post("/orders/{order_id}/pay", response_model=PayOrderResponse)
def pay_order(
    order_id: int,
    payment_data: PaymentCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )

    if payment_data.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Payment amount must be greater than zero",
        )

    if payment_data.amount < order.total_amount:
        raise HTTPException(
            status_code=400,
            detail="Payment amount is less than order total",
        )

    payment = (
        db.query(Payment)
        .filter(Payment.order_id == order.id)
        .first()
    )

    if payment:
        raise HTTPException(
            status_code=400,
            detail="Order is already paid",
        )

    payment = Payment(
        order_id=order.id,
        amount=payment_data.amount,
        payment_method=payment_data.payment_method,
        status="paid",
    )
    db.add(payment)

    if payment_data.amount >= 1000.0:
        earned_points = int(payment_data.amount // 100.0)
    else:
        earned_points = 0

    order.points_earned = earned_points
    order.status = "paid"

    if order.points_used > 0:
        table = db.query(RestaurantTable).filter(RestaurantTable.id == order.table_id).first()
        if table:
            table.points_balance = max(0, table.points_balance - order.points_used)

    table = db.query(RestaurantTable).filter(RestaurantTable.id == order.table_id).first()
    if table:
        table.points_balance += order.points_earned

    db.commit()
    db.refresh(order)
    db.refresh(payment)

    order_response = {
        "id": order.id,
        "restaurant_id": order.restaurant_id,
        "table_id": order.table_id,
        "order_code": order.order_code,
        "status": order.status,
        "total_amount": order.total_amount,
        "points_used": order.points_used,
        "discount_amount": order.discount_amount,
        "points_earned": order.points_earned,
        "items": [
            {
                "id": item.id,
                "menu_item_id": item.menu_item_id,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "total_price": item.total_price,
            }
            for item in order.items
        ],
    }

    payment_response = {
        "id": payment.id,
        "order_id": payment.order_id,
        "amount": payment.amount,
        "payment_method": payment.payment_method,
        "status": payment.status,
    }

    response_payload = {
        "order": order_response,
        "payment": payment_response,
    }

    # Notify n8n in background
    background_tasks.add_task(notify_n8n, "payment_successful", response_payload)

    return response_payload