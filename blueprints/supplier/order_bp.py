from flask import Blueprint, jsonify
from services.order_service import OrderService  
from flask import Blueprint, render_template

order_bp = Blueprint('supplier_order', __name__)  

@order_bp.route('/list', methods=['GET'])
def list_orders():
    orders = OrderService.get_orders()  
    return jsonify([o.to_dict() for o in orders])

@order_bp.route('/get_orders', methods=['GET'])
def get_orders():
    orders = OrderService.get_orders()  
    return render_template('supplier/orders.html', orders=orders)