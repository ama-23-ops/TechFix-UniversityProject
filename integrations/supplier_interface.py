from abc import ABC, abstractmethod

class SupplierInterface(ABC):
    @abstractmethod
    def fetch_price(self, product_id):
        """Fetches the price of a product from the supplier."""
        pass

    @abstractmethod
    def get_supplier_name(self) -> str:
        """Return supplier name"""
        pass

    @abstractmethod
    def fetch_discount(self, product_id) -> float:
        """Fetches the discount of the supplier"""
        pass