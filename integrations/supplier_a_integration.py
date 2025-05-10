from integrations.supplier_interface import SupplierInterface

class SupplierAIntegration(SupplierInterface):
    def fetch_price(self, product_id):
        # Simulate fetching the price from Supplier A's API
        if product_id == 1:
            return 100.00
        elif product_id == 2:
            return 200.00
        else:
            return 150.00  # Default price

    def get_supplier_name(self) -> str:
        return "Supplier A"

    def fetch_discount(self, product_id) -> float:
        return 5.0