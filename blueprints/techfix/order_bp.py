from flask import Blueprint, request, jsonify
from services.order_service import OrderService  
from flask import Blueprint, render_template

order_bp = Blueprint('order', __name__)

@order_bp.route('/create', methods=['POST'])
def create_order():
    data = request.json
    quotation_id = data.get('quotation_id')
    order = OrderService.create_order(quotation_id)
    return jsonify(order.to_dict())

@order_bp.route('/list', methods=['GET'])
def list_orders():
    orders = OrderService.get_orders()
    return render_template('techfix/orders.html', orders=orders)