import unittest

from fastapi.testclient import TestClient

from backend.database import SessionLocal
from backend.main import app
from backend.models import Restaurant, RestaurantTable, MenuItem


class OrderFlowTest(unittest.TestCase):
    def setUp(self):
        self.db = SessionLocal()
        self.db.query(MenuItem).delete()
        self.db.query(RestaurantTable).delete()
        self.db.query(Restaurant).delete()
        self.db.commit()

        restaurant = Restaurant(name="Cafe Test", email="test@example.com")
        self.db.add(restaurant)
        self.db.commit()
        self.db.refresh(restaurant)

        table = RestaurantTable(
            restaurant_id=restaurant.id,
            table_number=7,
            qr_token="token-order-test",
            active=True,
        )
        self.db.add(table)
        self.db.commit()
        self.db.refresh(table)

        item = MenuItem(
            restaurant_id=restaurant.id,
            name="Pizza",
            description="Cheesy pizza",
            price=250.0,
            category="North Indian",
            image_url=None,
            available=True,
        )
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)

        self.restaurant = restaurant
        self.table = table
        self.item = item

    def tearDown(self):
        self.db.query(MenuItem).delete()
        self.db.query(RestaurantTable).delete()
        self.db.query(Restaurant).delete()
        self.db.commit()
        self.db.close()

    def test_place_order_and_pay(self):
        client = TestClient(app)

        response = client.post(
            "/orders",
            json={
                "token": self.table.qr_token,
                "items": [{"menu_item_id": self.item.id, "quantity": 2}],
            },
        )

        self.assertEqual(response.status_code, 200, response.text)
        payload = response.json()
        self.assertIn("order_code", payload)
        self.assertEqual(payload["total_amount"], 500.0)

        pay_response = client.post(
            f"/orders/{payload['id']}/pay",
            json={"amount": 500.0, "payment_method": "cash"},
        )

        self.assertEqual(pay_response.status_code, 200, pay_response.text)
        payment = pay_response.json()["payment"]
        self.assertEqual(payment["status"], "paid")
        self.assertEqual(payment["amount"], 500.0)

    def test_get_restaurant_orders(self):
        client = TestClient(app)

        create_response = client.post(
            "/orders",
            json={
                "token": self.table.qr_token,
                "items": [{"menu_item_id": self.item.id, "quantity": 1}],
            },
        )

        self.assertEqual(create_response.status_code, 200, create_response.text)
        order_id = create_response.json()["id"]

        list_response = client.get(f"/restaurants/{self.restaurant.id}/orders")

        self.assertEqual(list_response.status_code, 200, list_response.text)
        payload = list_response.json()
        self.assertEqual(payload["restaurant_id"], self.restaurant.id)
        self.assertGreaterEqual(len(payload["orders"]), 1)
        self.assertEqual(payload["orders"][0]["id"], order_id)

    def test_loyalty_points_are_earned_and_redeemed(self):
        client = TestClient(app)

        large_order = client.post(
            "/orders",
            json={
                "token": self.table.qr_token,
                "items": [{"menu_item_id": self.item.id, "quantity": 6}],
            },
        )

        self.assertEqual(large_order.status_code, 200, large_order.text)
        large_payload = large_order.json()
        self.assertEqual(large_payload["total_amount"], 1500.0)

        pay_response = client.post(
            f"/orders/{large_payload['id']}/pay",
            json={"amount": 1500.0, "payment_method": "cash"},
        )

        self.assertEqual(pay_response.status_code, 200, pay_response.text)
        self.assertGreaterEqual(pay_response.json()["order"]["points_earned"], 15)

        menu_response = client.get(f"/menu?token={self.table.qr_token}")
        self.assertEqual(menu_response.status_code, 200, menu_response.text)
        self.assertGreaterEqual(menu_response.json()["points_balance"], 15)

        second_order = client.post(
            "/orders",
            json={
                "token": self.table.qr_token,
                "items": [{"menu_item_id": self.item.id, "quantity": 2}],
                "points_to_use": 10,
            },
        )

        self.assertEqual(second_order.status_code, 200, second_order.text)
        second_payload = second_order.json()
        self.assertEqual(second_payload["points_used"], 10)
        self.assertEqual(second_payload["discount_amount"], 10.0)
        self.assertEqual(second_payload["total_amount"], 490.0)


if __name__ == "__main__":
    unittest.main()
