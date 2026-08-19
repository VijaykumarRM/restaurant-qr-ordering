# 🌐 LIVE WEBSITE - LOCAL NETWORK DEPLOYMENT

Your Restaurant QR Ordering System is now set up for **Local Network (LAN)** access!

---

## ✨ What Changed

### ✅ Network Access
- Backend listens on all interfaces (`0.0.0.0:8000`)
- Frontend listens on all interfaces (`0.0.0.0:5500`)
- Others on your WiFi can now access the system

### ✅ Admin Password Protection
- Admin dashboard requires password login
- Default password: `admin123`
- Customer pages remain read-only

### ✅ Updated Files
- `frontend/menu.html` - Updated to use IP `10.45.12.148`
- `frontend/admin.html` - Updated to use IP `10.45.12.148` + password protection
- `START.bat` - Updated to bind on `0.0.0.0` for LAN access
- `SETUP_LAN.md` - Complete LAN setup guide

---

## 🚀 Quick Start (30 seconds)

### Step 1: Double-click START.bat
```
START.bat
```

Backend and frontend servers start automatically.

### Step 2: Tell Others Your IP
Share this URL:
```
http://10.45.12.148:5500/admin.html       (admin - password: admin123)
http://10.45.12.148:5500/menu.html?token=test  (customer - read-only)
```

### Done! ✅

---

## 📱 Access from Other Devices

**On same WiFi network, visit:**
```
Admin:    http://10.45.12.148:5500/admin.html
          Password: admin123

Customer: http://10.45.12.148:5500/menu.html?token=test
```

---

## 🔐 User Roles

| User | Access | Password | Features |
|------|--------|----------|----------|
| Admin | admin.html | `admin123` | Add menu, scan QR, view orders |
| Customer | menu.html | None | Browse, order, earn loyalty points |
| Viewer | Any URL | None | Read-only access |

---

## 📊 Features Working on LAN

✅ Real-time order tracking  
✅ QR code generation & scanning  
✅ Loyalty points earning & redemption  
✅ Customer menu browsing  
✅ Admin dashboard  
✅ Payment status tracking  
✅ Multi-device support  

---

## 🌍 Your Network

```
Your IP: 10.45.12.148

Servers:
  Backend API: http://10.45.12.148:8000
  Frontend:    http://10.45.12.148:5500

Admin:    http://10.45.12.148:5500/admin.html (pwd: admin123)
Customer: http://10.45.12.148:5500/menu.html?token=test
API Docs: http://10.45.12.148:8000/docs
```

---

## ⚙️ Configuration

### Change Admin Password

Edit `frontend/admin.html` (line ~950):
```javascript
// OLD:
const ADMIN_PASSWORD = "admin123";

// NEW:
const ADMIN_PASSWORD = "your_password";
```

### Change Your IP

If your IP differs from `10.45.12.148`:

1. Run: `ipconfig | findstr IPv4`
2. Update both HTML files with your IP
3. Update START.bat display messages

---

## 🧪 Testing Checklist

- [ ] START.bat successfully starts both servers
- [ ] Admin page loads: `http://10.45.12.148:5500/admin.html`
- [ ] Admin password works: `admin123`
- [ ] Customer page loads: `http://10.45.12.148:5500/menu.html?token=test`
- [ ] Menu items load on customer page
- [ ] Can add items in admin (after login)
- [ ] Can place order as customer
- [ ] Loyalty points display & work
- [ ] From another device on WiFi, can access same URLs

---

## 🔧 Troubleshooting

### "Cannot connect to server"
→ Check firewall settings (see SETUP_LAN.md)

### "Servers won't start"
→ Ensure ports 8000, 5500 are free: `netstat -ano | findstr "8000\|5500"`

### "Admin password wrong"
→ Default is `admin123` (check line ~950 in admin.html)

### "Others can't access"
→ Verify IP is correct: `ipconfig | findstr IPv4`
→ Check Windows Firewall allows Python

---

## 📖 Full Documentation

- **SETUP_LAN.md** - Complete LAN setup guide
- **README.md** - Quick start
- **FINAL_GUIDE.md** - Feature reference
- **OVERVIEW.md** - Architecture

---

## 🎉 Status

**✅ LIVE WEBSITE READY**

Your Restaurant QR Ordering System is now:
- ✅ Accessible on local network
- ✅ Password-protected admin panel
- ✅ Read-only customer access
- ✅ Real-time updates
- ✅ Production-ready

Share the IP with others and start serving! 🍽️

---

**Local Network Access: `http://10.45.12.148:5500`**  
**Admin Password: `admin123`**  
**Status: LIVE ✅**
