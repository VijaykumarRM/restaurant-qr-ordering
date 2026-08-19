# Admin Menu QR Scanning Feature

## Overview
The admin can now quickly add menu items by scanning QR codes. Each menu item has a unique QR code that encodes its details (name, price, category, description). When scanned, the item is automatically added to the menu.

## How It Works

### For Setup (Restaurant Owner)
1. Run the sample QR generator:
   ```bash
   python generate_menu_qr_samples.py
   ```
   This creates QR code images in the `qr_codes/` folder

2. Print these QR codes and place them next to each physical menu item or ingredient

### For Admin Daily Use
1. Open the restaurant dashboard: `http://127.0.0.1:5500/admin.html`
2. Scroll to the **"📱 Scan Menu Item QR"** section
3. Click the **"📷 Start Scanner"** button
4. Allow camera permission when prompted
5. Point your device at a menu item QR code
6. The scanner will:
   - Read the QR code
   - Auto-fill the form fields (name, price, category, description)
   - Automatically publish the item to the menu
   - Stop the scanner

### QR Code Format
Each QR code contains JSON data:
```json
{
  "name": "Masala Dosa",
  "price": 250,
  "category": "South Indian",
  "description": "Crispy dosa with spiced potato filling"
}
```

## Generating Custom QR Codes

To generate QR codes for your own menu items, you can:

### Option 1: Use the Backend API
Call the endpoint to download a QR code for an existing menu item:
```
http://127.0.0.1:8000/restaurants/1/menu/{menu_item_id}/qr
```

The menu item must already exist in the database.

### Option 2: Create a Python Script
```python
from backend.qr_generator import generate_menu_item_qr

generate_menu_item_qr(
    name="My Dish",
    price=150,
    category="Appetizers",
    description="My dish description",
    restaurant_id=1
)
```

## Admin Panel Updates
- **QR Scanner Section**: New section at the top to start/stop scanning
- **QR Download Buttons**: Each menu item now has a "📱 QR" button to download its QR code
- **Auto-Publish Flow**: Scanned items are automatically added after 500ms confirmation

## Technical Details
- **Scanner Library**: `html5-qrcode` (via CDN)
- **QR Generation**: `python-qrcode` library
- **Supported Formats**: JSON text encoded in QR code
- **Backend Endpoint**: `GET /restaurants/{id}/menu/{item_id}/qr`

## Troubleshooting

**Camera won't start?**
- Check browser permissions for camera access
- Make sure you're using HTTPS or localhost
- Try a different browser (Chrome/Firefox work best)

**QR code doesn't scan?**
- Ensure good lighting
- Keep QR code steady and in frame
- Make sure QR code is not damaged/faded

**Item doesn't auto-publish?**
- Check browser console for errors (F12)
- Make sure FastAPI backend is running on port 8000
- Verify the JSON format is correct

## Future Enhancements
- Batch QR scanning (multiple items at once)
- Mobile app for admin scanning
- Integration with POS system
- Custom QR template designs
