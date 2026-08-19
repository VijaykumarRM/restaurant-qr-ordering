import qrcode
from pathlib import Path
from urllib.parse import urlencode
import json


def build_table_qr_url(
    qr_token: str,
    restaurant_id: int,
    table_number: int,
    frontend_base_url: str = "http://127.0.0.1:5500/frontend/menu.html",
):
    params = urlencode({"token": qr_token})
    return f"{frontend_base_url}?{params}"


def generate_table_qr(
    qr_token: str,
    restaurant_id: int,
    table_number: int,
    frontend_base_url: str = "http://127.0.0.1:5500/frontend/menu.html",
):
    url = build_table_qr_url(
        qr_token,
        restaurant_id=restaurant_id,
        table_number=table_number,
        frontend_base_url=frontend_base_url,
    )

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )

    qr.add_data(url)
    qr.make(fit=True)

    image = qr.make_image()

    output_dir = Path("qr_codes")
    output_dir.mkdir(exist_ok=True)

    filename = (
        f"restaurant_{restaurant_id}"
        f"_table_{table_number}.png"
    )

    output_path = output_dir / filename

    image.save(output_path)


def generate_menu_item_qr(
    name: str,
    price: float,
    category: str = "Snacks",
    description: str = "",
    restaurant_id: int = 1,
    menu_item_id: int = None,
):
    """Generate a QR code that contains menu item JSON data."""
    menu_data = {
        "name": name,
        "price": price,
        "category": category,
        "description": description,
    }

    qr_text = json.dumps(menu_data)

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )

    qr.add_data(qr_text)
    qr.make(fit=True)

    image = qr.make_image()

    output_dir = Path("qr_codes")
    output_dir.mkdir(exist_ok=True)

    safe_name = name.replace(" ", "_").replace("/", "_")[:30]
    filename = f"menu_item_{restaurant_id}_{safe_name}.png"

    output_path = output_dir / filename

    image.save(output_path)

    return str(output_path)

    return str(output_path)