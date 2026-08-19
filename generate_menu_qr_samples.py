#!/usr/bin/env python3
"""
Generate sample menu item QR codes for testing the admin scanner.
Run this to create QR codes that can be printed and scanned by the admin.
"""

from backend.qr_generator import generate_menu_item_qr

# Sample menu items to generate QR codes for
menu_items = [
    {"name": "Masala Dosa", "price": 250, "category": "South Indian", "description": "Crispy dosa with spiced potato filling"},
    {"name": "Idli", "price": 60, "category": "South Indian", "description": "Steamed rice cakes served with chutney"},
    {"name": "Butter Chicken", "price": 350, "category": "North Indian", "description": "Tender chicken in creamy butter gravy"},
    {"name": "Naan", "price": 80, "category": "North Indian", "description": "Soft flatbread from tandoor"},
    {"name": "Chow Mein", "price": 180, "category": "Chinese", "description": "Stir-fried noodles with vegetables"},
    {"name": "Spring Rolls", "price": 120, "category": "Snacks", "description": "Crispy rolls with vegetable filling"},
    {"name": "Lassi", "price": 100, "category": "Beverages", "description": "Traditional yogurt drink"},
    {"name": "Gulab Jamun", "price": 90, "category": "Desserts", "description": "Soft milk solids in sugar syrup"},
]

print("🎯 Generating sample menu item QR codes...\n")

for item in menu_items:
    qr_path = generate_menu_item_qr(
        name=item["name"],
        price=item["price"],
        category=item["category"],
        description=item["description"],
        restaurant_id=1,
    )
    print(f"✅ Generated QR for {item['name']:20} → {qr_path}")

print(f"\n✅ All QR codes generated! Check the 'qr_codes' folder.")
print("\n📱 How to use:")
print("1. Print the QR codes")
print("2. Place them next to each menu item")
print("3. Open admin.html in your browser")
print("4. Click 'Start Scanner' and scan any QR code")
print("5. Menu item details auto-fill and publish automatically!")
