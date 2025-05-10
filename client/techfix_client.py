# client/techfix_client.py
import requests

class TechFixClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_products(self):
        response = requests.get(f"{self.base_url}/api/products")
        return response.json()

    def create_product(self, name, price, category="General"):
        payload = {"name": name, "price": price, "category": category}
        response = requests.post(f"{self.base_url}/api/products", json=payload)
        return response.json()

    def get_suppliers(self):
        response = requests.get(f"{self.base_url}/api/suppliers")
        return response.json()

    def create_supplier(self, name, contact_email):
        payload = {"name": name, "contact_email": contact_email}
        response = requests.post(f"{self.base_url}/api/suppliers", json=payload)
        return response.json()

# Example Usage
if __name__ == '__main__':
    client = TechFixClient("http://127.0.0.1:5000")
    print(client.get_products())
    print(client.create_supplier("Supplier A", "contact@suppA.com"))