from models import Order, Quotation, db  

class OrderService:
    @staticmethod
    def create_order(quotation_id):
        """
        Convert a quotation into an order.
        """
        quotation = Quotation.query.get(quotation_id)
        if not quotation:
            return None

        order = Order(
            quotation_id=quotation.id,
            supplier_id=quotation.supplier_id,
            total_cost=quotation.total_cost,
            status="Placed"
        )
        db.session.add(order)
        db.session.commit()
        return order

    @staticmethod
    def get_orders():
        """
        Retrieve all orders.
        """
        return Order.query.all()


class SupplierOrderService:
    @staticmethod
    def acknowledge_order(order_id):
        """
        Supplier acknowledges an order.
        """
        order = Order.query.get(order_id)
        if not order:
            return None

        order.status = "Acknowledged"
        db.session.commit()
        return order

    @staticmethod
    def update_order_status(order_id, status):
        """
        Supplier updates the order status.
        """
        order = Order.query.get(order_id)
        if not order:
            return None

        order.status = status
        db.session.commit()
        return order

    @staticmethod
    def get_orders_for_supplier(supplier_id):
        """
        Retrieve all orders for a specific supplier.
        """
        return Order.query.filter_by(supplier_id=supplier_id).all()