from integrations.supplier_interface import SupplierInterface

class SupplierBIntegration(SupplierInterface):
    def fetch_price(self, product_id):
        # Simulate fetching the price from Supplier B's API
        if product_id == 1:
            return 95.00
        elif product_id == 2:
            return 210.00
        else:
            return 160.00  # Default price

    def get_supplier_name(self) -> str:
        return "Supplier B"

    def fetch_discount(self, product_id) -> float:
        return 0.0