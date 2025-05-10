from models import Quotation, Product, db

class QuotationService:
    @staticmethod
    def request_quotation(product_ids, quantities, supplier_id):
        """
        Request a quotation from a supplier.
        """
        # Validate input
        if not product_ids or not quantities or len(product_ids) != len(quantities):
            raise ValueError("Invalid input: product_ids and quantities must be provided and of equal length")

        # Ensure quantities are numbers
        try:
            quantities = [float(q) for q in quantities]  # Convert quantities to floats
        except (ValueError, TypeError):
            raise ValueError("Invalid quantities: must be numbers")

        # Fetch product details
        products = Product.query.filter(Product.id.in_(product_ids)).all()
        if len(products) != len(product_ids):
            raise ValueError("Invalid product IDs provided")

        # Calculate total cost
        total_cost = sum(product.price * quantity for product, quantity in zip(products, quantities))

        # Create and save the quotation
        quotation = Quotation(
            supplier_id=supplier_id,
            product_ids=product_ids,
            quantities=quantities,
            total_cost=total_cost,
            status="Pending"
        )
        db.session.add(quotation)
        db.session.commit()
        return quotation

    @staticmethod
    def get_quotations():
        """
        Retrieve all quotations.
        """
        return Quotation.query.all()

class SupplierQuotationService:
    @staticmethod
    def respond_to_quotation(quotation_id, response_data):
        """
        Supplier responds to a quotation request.
        """
        quotation = Quotation.query.get(quotation_id)
        if not quotation:
            return None

        quotation.status = "Responded"
        quotation.total_cost = response_data.get("final_price")
        db.session.commit()
        return quotation

    @staticmethod
    def get_quotations_for_supplier(supplier_id):
        """
        Retrieve all quotations for a specific supplier.
        """
        return Quotation.query.filter_by(supplier_id=supplier_id).all()