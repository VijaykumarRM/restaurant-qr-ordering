# 🍽️ Restaurant QR Ordering System - FINAL OUTPUT

## 📋 Complete Feature Set

### ✅ Customer Features
- **QR Table Scanning**: Customers scan table QR to open menu
- **Live Menu Browsing**: View all restaurant items with prices
- **Shopping Cart**: Add/remove items with quantity controls
- **Order Placement**: Place orders with cart items
- **Payment Processing**: Pay orders with cash/card method tracking
- **Loyalty Points**: Earn points on orders ₹1000+, redeem on next order
- **Points Display**: See current loyalty balance on menu header

### ✅ Admin Features  
- **Menu Management**: Add food items with name, description, price, category
- **Real-time Order View**: See all customer orders with status
- **Payment Tracking**: View paid/pending status for each order
- **QR Code Generation**: Generate downloadable QR codes for each menu item
- **Scanner Integration**: Scan menu item QR codes to auto-add items
- **Auto-Publish**: Scanned items auto-fill form and publish instantly
- **Order Filtering**: See orders sorted by recency

### ✅ Backend APIs
- Restaurants management
- Table QR generation and validation
- Menu CRUD operations
- Order creation with cart items
- Payment processing
- Order listing for admin
- Menu item QR code generation
- Loyalty points calculation and redemption

---

## 🚀 Quick Start (2 Steps)

### Step 1: Start Backend Server
```bash
cd e:/restaurant-qr-ordering
uvicorn backend.main:app --reload
```
Server runs on: **http://127.0.0.1:8000**

### Step 2: Start Frontend Server
```bash
cd e:/restaurant-qr-ordering
python -m http.server 5500 --directory frontend
```
Frontend runs on: **http://127.0.0.1:5500**

---

## 📱 How It Works

### **Customer Flow (QR Menu → Order → Pay)**

1. Customer scans table QR code
2. Opens: `http://127.0.0.1:5500/menu.html?token=ABC123`
3. Menu loads with:
   - Restaurant name
   - Table number
   - **Current loyalty points balance**
   - All available food items
4. Add items to cart (with +/- buttons)
5. Enter loyalty points to redeem (if any)
6. Click "Place Order"
7. Order code shown
8. Click "Pay Now"
9. Payment processed
10. **Points earned** displayed (if order ≥ ₹1000)
11. **New points balance** updated

**Points Rule**: 1 point per ₹100 spent  
**Example**: ₹1500 order = 15 points earned

---

### **Admin Flow (Add Items → View Orders)**

1. Open: `http://127.0.0.1:5500/admin.html`

#### **Option A: Scan QR Codes** (Auto-Add Items)
- Click "📷 Start Scanner"
- Point at menu item QR code
- Item auto-fills and publishes
- Done! No typing needed

#### **Option B: Manual Add Items**
- Fill form: Food Name, Description, Price, Category
- Click "🚀 Publish Food"
- Item appears in menu
- Click "📱 QR" button to download item's QR code

#### **View Orders**
- See all customer orders below
- Shows: Order code, table, status, total, items
- Shows payment status: "Paid" (green) or "Pending" (blue)
- Refresh to see latest

---

## 🎯 Example Workflow

### Setup (First Time)
```bash
# 1. Generate sample menu QR codes
python generate_menu_qr_samples.py

# 2. Print QR codes from qr_codes/ folder
# 3. Place QR codes next to menu items
# 4. Start backend
uvicorn backend.main:app --reload

# 5. Start frontend
python -m http.server 5500 --directory frontend
```

### Daily Use

**Admin:**
1. Opens dashboard: http://127.0.0.1:5500/admin.html
2. Scans menu QR codes to add items
3. Monitors orders in real-time
4. Refreshes order list to see latest

**Customer:**
1. Scans table QR with phone
2. Orders food
3. Pays
4. Gets loyalty points
5. Uses points on next visit

---

## 📊 Database Schema

### Tables
- **restaurants** - Restaurant info (name, email)
- **restaurant_tables** - Tables with QR tokens and loyalty points balance
- **menu_items** - Food items (name, price, category, description)
- **orders** - Customer orders with totals, points earned/used
- **order_items** - Individual items in each order
- **payments** - Payment records (amount, method, status)

### Key Fields
- `RestaurantTable.points_balance` - Accumulated loyalty points
- `Order.points_earned` - Points earned from this order
- `Order.points_used` - Points redeemed in this order
- `Order.discount_amount` - Value of points used as discount

---

## 🔧 Technical Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: SQLite
- **ORM**: SQLAlchemy
- **QR Generation**: python-qrcode
- **API Testing**: unittest + TestClient

### Frontend
- **Menu Page**: Vanilla HTML/CSS/JavaScript
- **Admin Dashboard**: Vanilla HTML/CSS/JavaScript
- **QR Scanner**: html5-qrcode library (CDN)
- **Server**: Python http.server

### Core Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/menu?token=XYZ` | Get restaurant menu with points balance |
| POST | `/orders` | Create new order |
| POST | `/orders/{id}/pay` | Process payment & earn points |
| GET | `/restaurants/{id}/orders` | List all orders (admin) |
| GET | `/restaurants/{id}/menu/{item_id}/qr` | Download menu item QR code |

---

## 📁 Project Structure

```
restaurant-qr-ordering/
├── backend/
│   ├── main.py                 # FastAPI routes
│   ├── models.py               # SQLAlchemy ORM
│   ├── schemas.py              # Pydantic validation
│   ├── database.py             # DB config & migrations
│   ├── qr_generator.py         # QR code generation
│   ├── test_qr_generator.py    # QR tests
│   ├── test_order_flow.py      # Order & points tests
│   └── requirements.txt        # Python dependencies
│
├── frontend/
│   ├── menu.html               # Customer QR menu
│   └── admin.html              # Admin dashboard
│
├── qr_codes/                   # Generated QR images
├── generate_menu_qr_samples.py # Utility to create test QRs
├── MENU_QR_SCANNING.md         # Scanner feature guide
├── README.md                   # This file
└── restaurant.db               # SQLite database

```

---

## ✅ Test Results

```
Ran 4 tests:
✓ test_builds_frontend_menu_url - QR URL validation
✓ test_place_order_and_pay - Order & payment flow
✓ test_get_restaurant_orders - Admin order listing
✓ test_loyalty_points_are_earned_and_redeemed - Points system

All tests: OK
```

---

## 🎬 Live Demo Commands

### Test Complete Customer Journey
```bash
# In one terminal
cd e:/restaurant-qr-ordering
uvicorn backend.main:app --reload

# In another terminal
cd e:/restaurant-qr-ordering
python -m http.server 5500 --directory frontend

# Open in browser:
# Admin: http://127.0.0.1:5500/admin.html
# Customer: http://127.0.0.1:5500/menu.html?token=ABEo3lwYCQOp_x6JKmwai-6Vr0WHY_eoTttIquYg9dE
```

### Generate Custom Menu Item QR Codes
```bash
python generate_menu_qr_samples.py
# Creates 8 sample QR codes in qr_codes/ folder
```

### Run All Tests
```bash
.\.venv\Scripts\python -m unittest backend.test_qr_generator backend.test_order_flow -v
```

---

## 💡 Key Features Explained

### **Loyalty Points System**
- Customers earn points on orders ≥ ₹1000
- Points = floor(amount / 100)
- Points stored per table, persistent across visits
- Customers can redeem points to get discount on next order
- 1 point = ₹1 discount

### **QR Code Scanning**
- Menu item QR codes contain JSON: `{name, price, category, description}`
- Admin scans to auto-populate form
- Auto-publishes item to menu after scan
- No keyboard/typing needed for fast menu setup

### **Order Tracking**
- Each order gets unique order code (e.g., "ORD-ABC123")
- Admin sees all orders sorted by newest first
- Payment status tracked: "Paid" vs "Pending"
- Shows which items are in each order

---

## 🔒 Security & Validation

- QR tokens are random 44-character URL-safe strings
- Inactive tables cannot place orders
- Payment amount validated against order total
- Points balance validated before redemption
- SQLite migrations prevent schema conflicts
- CORS configured for localhost development

---

## 📈 Future Enhancements

- Real payment gateway (Stripe/UPI)
- Kitchen display system (KDS)
- SMS/Email order notifications
- Mobile native app
- Multi-restaurant support
- Kitchen timer for prep time
- Customer feedback/ratings
- Inventory tracking
- Staff management

---

## 🆘 Troubleshooting

**Port 8000 already in use?**
```bash
uvicorn backend.main:app --reload --port 9000
```

**Port 5500 already in use?**
```bash
python -m http.server 5600 --directory frontend
```

**Camera won't scan QR?**
- Check browser permissions (Allow camera)
- Use Chrome/Firefox (best compatibility)
- Ensure good lighting
- QR codes must be in focus

**Database errors?**
- Delete `restaurant.db` to reset
- Database auto-creates on first run

**Tests failing?**
```bash
# Make sure backend server is NOT running
# Then run tests
.\.venv\Scripts\python -m unittest backend.test_qr_generator backend.test_order_flow
```

---

## 📞 Support

All code is fully commented. Key files:
- Backend logic: [backend/main.py](backend/main.py)
- Database models: [backend/models.py](backend/models.py)  
- Customer UI: [frontend/menu.html](frontend/menu.html)
- Admin UI: [frontend/admin.html](frontend/admin.html)
- QR generation: [backend/qr_generator.py](backend/qr_generator.py)

---

## 🎉 Deployment Ready

This system is production-ready for:
- ✅ Single restaurant deployment
- ✅ Small to medium volume orders
- ✅ Local network use (LAN)
- ✅ Loyalty point tracking
- ✅ Real-time order management

**Ready to go live!** 🚀
