# 🍽️ Setup Restaurant QR Ordering System for Local Network (LAN)

This guide explains how to make your Restaurant QR Ordering System accessible to others on your local network (WiFi).

---

## 🎯 What This Does

After setup, others on your WiFi can:
- ✅ Access admin dashboard (with password)
- ✅ Browse customer menu
- ✅ Place orders
- ✅ See real-time updates

**Your IP Address**: `10.45.12.148`

---

## 📋 Setup Steps

### Step 1: Get Your Local IP Address

Open PowerShell and run:
```bash
ipconfig | findstr "IPv4"
```

**You'll see something like:**
```
IPv4 Address . . . . . . . . . . : 10.45.12.148
```

**Remember this IP!** You'll share it with others.

---

### Step 2: Update Frontend Configuration

Edit both HTML files to use your IP instead of localhost:

#### `frontend/menu.html` - Line 2 (in JavaScript section):
**Find:**
```javascript
const API_URL = "http://127.0.0.1:8000";
```

**Replace with:**
```javascript
const API_URL = "http://10.45.12.148:8000";
```

#### `frontend/admin.html` - Line 2 (in JavaScript section):
**Find:**
```javascript
const API_URL = "http://127.0.0.1:8000";
```

**Replace with:**
```javascript
const API_URL = "http://10.45.12.148:8000";
```

---

### Step 3: Start the Servers

#### Option A: Using START.bat (Windows)
Simply double-click:
```
START.bat
```

This will automatically:
- Start FastAPI backend on `0.0.0.0:8000` (all interfaces)
- Start HTTP server on `0.0.0.0:5500` (all interfaces)

#### Option B: Manual Start (Windows)

**Terminal 1 - Backend:**
```bash
cd e:\restaurant-qr-ordering
.\.venv\Scripts\python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Frontend:**
```bash
cd e:\restaurant-qr-ordering\frontend
python -m http.server 5500 --bind 0.0.0.0
```

---

### Step 4: Test on Your Computer

Open browser and test:

**Admin Dashboard:**
```
http://10.45.12.148:5500/admin.html
```
- Password: `admin123`
- Can add menu items, scan QRs, view orders

**Customer Menu:**
```
http://10.45.12.148:5500/menu.html?token=test
```
- Can browse, add to cart, place orders, earn loyalty points

**API (Development):**
```
http://10.45.12.148:8000/docs
```
- Interactive API documentation

---

### Step 5: Share IP with Others

Tell others to visit:
```
http://10.45.12.148:5500/admin.html    (Admin panel - password protected)
http://10.45.12.148:5500/menu.html?token=test    (Customer menu)
```

---

## 🔐 Admin Access

### Default Admin Password
```
admin123
```

### Change Password

Edit `frontend/admin.html` and find this line (around line 950):
```javascript
const ADMIN_PASSWORD = "admin123";
```

Change to your desired password:
```javascript
const ADMIN_PASSWORD = "your_new_password";
```

**Note:** Password is visible in browser source code. For production, use proper backend authentication.

---

## 👥 User Roles

### Admin Users
- Password: `admin123`
- Can: Add menu items, scan QRs, view all orders, download QR codes
- Cannot: Delete items (read-only view for non-admin)

### Customer Users (Read-Only)
- No password needed
- Can: Browse menu, add to cart, place orders, earn loyalty points
- Cannot: Edit menu, view other orders

---

## 🌐 Network Access

### Who Can Access?
- ✅ Anyone on the same WiFi network
- ✅ Anyone with your IP address
- ✅ Other computers/phones on your LAN

### Who Cannot Access?
- ❌ Internet users (not exposed publicly)
- ❌ Users outside your WiFi network
- ❌ Unless you configure port forwarding

---

## ⚠️ Firewall Settings

If others can't connect, allow ports in Windows Firewall:

### For Windows Defender Firewall:
1. Go to **Windows Security** > **Firewall & network protection**
2. Click **"Allow an app through firewall"**
3. Click **"Change settings"**
4. Click **"Allow another app"**
5. Browse to `python.exe` (in `.venv\Scripts`)
6. Click **"Add"**
7. Ensure it's checked for "Private" networks

---

## 🧪 Testing on LAN

### From Another Computer on WiFi:

1. **Get your IP**: Run `ipconfig` (e.g., `10.45.12.148`)

2. **Admin visits:**
   ```
   http://10.45.12.148:5500/admin.html
   ```
   - Enter password: `admin123`
   - Can view/manage menu and orders

3. **Customer visits:**
   ```
   http://10.45.12.148:5500/menu.html?token=test
   ```
   - Can browse, order, see loyalty points
   - Cannot edit anything

---

## 📱 Mobile Testing

### From Smartphone on Same WiFi:

1. **Make sure phone is on the same WiFi**

2. **Admin on mobile:**
   ```
   http://10.45.12.148:5500/admin.html
   ```
   - Test QR scanning with phone camera
   - Add items, view orders

3. **Customer on mobile:**
   ```
   http://10.45.12.148:5500/menu.html?token=test
   ```
   - Responsive design works on mobile
   - Can order from phone

---

## 🔧 Troubleshooting

### Issue: "Cannot connect to backend"
**Solution:** 
- Ensure FastAPI is running: `http://10.45.12.148:8000/docs` should open
- Check if firewall is blocking Python
- Ensure both terminals are still running

### Issue: "Others can't access my IP"
**Solution:**
- Verify IP is correct: Run `ipconfig` again
- Check if on same WiFi network
- Check Windows Firewall (see above)
- Temporarily disable firewall to test
- Ensure ports 8000 and 5500 are open

### Issue: "Admin password doesn't work"
**Solution:**
- Default password is: `admin123`
- Check caps lock
- Verify HTML file has correct password (line ~950 in admin.html)
- Clear browser cache and try again

### Issue: "QR scanner not working on mobile"
**Solution:**
- Allow camera permission when prompted
- Use Safari on iPhone (more reliable)
- Use Chrome on Android
- Ensure HTTPS if accessing from outside LAN (not needed for LAN)

---

## 📊 Example Network Setup

```
WiFi Router (10.45.12.0/24)
    │
    ├─ Your Computer (10.45.12.148)
    │   ├─ Backend: 10.45.12.148:8000
    │   ├─ Frontend: 10.45.12.148:5500
    │   └─ Admin accesses: http://10.45.12.148:5500/admin.html
    │
    ├─ Admin Phone/Laptop
    │   └─ Accesses: http://10.45.12.148:5500/admin.html (with password)
    │
    └─ Customer Phone/Laptop
        └─ Accesses: http://10.45.12.148:5500/menu.html?token=test
```

---

## 🚀 For Public Deployment

To deploy **beyond local network** to the internet:

1. **Get public domain** or fixed IP
2. **Use HTTPS** (Let's Encrypt free certificates)
3. **Add proper authentication** (database-backed)
4. **Use PostgreSQL** instead of SQLite
5. **Deploy to cloud** (Heroku, AWS, DigitalOcean, Render)
6. **Configure environment variables** for security
7. **Add rate limiting** and bot protection
8. **Setup monitoring** and logging
9. **Add payment gateway** integration
10. **Backup database** regularly

---

## ✅ Quick Checklist

- [ ] Found your local IP address
- [ ] Updated `frontend/menu.html` with your IP
- [ ] Updated `frontend/admin.html` with your IP
- [ ] Started backend server
- [ ] Started frontend server
- [ ] Tested admin: `http://YOUR_IP:5500/admin.html` (password: admin123)
- [ ] Tested customer: `http://YOUR_IP:5500/menu.html?token=test`
- [ ] Tested from another device on same WiFi
- [ ] Allowed Windows Firewall (if needed)

---

## 🎉 Ready to Serve!

Your Restaurant QR Ordering System is now accessible to all devices on your local network.

**Share the IP address**: `http://10.45.12.148`

Enjoy! 🍽️ 🚀
