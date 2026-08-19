"""
Restaurant QR Ordering - Startup Script
Run this file to start both backend API + frontend on http://localhost:8080
"""
import uvicorn
import webbrowser
import threading
import time


def open_browser():
    time.sleep(2)
    webbrowser.open("http://localhost:8080")


if __name__ == "__main__":
    print("=" * 60)
    print("  Restaurant QR Ordering System")
    print("=" * 60)
    print()
    print("  Admin Dashboard : http://localhost:8080/admin")
    print("  API Docs        : http://localhost:8080/docs")
    print("  Health Check    : http://localhost:8080/health")
    print()
    print("  Password: admin123")
    print()
    print("=" * 60)
    print()

    threading.Thread(target=open_browser, daemon=True).start()

    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
    )
