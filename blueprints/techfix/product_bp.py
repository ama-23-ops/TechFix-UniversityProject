# blueprints/techfix/product_bp.py
from flask import Blueprint, jsonify, render_template
from services.product_service import ProductService
from flask_login import login_required

product_bp = Blueprint('techfix_product', __name__, url_prefix='/techfix')

@product_bp.route('/products', methods=['GET'])
@login_required
def get_products_page():  
    products = ProductService.get_products()
    return render_template('techfix/products.html', products = products)  

@product_bp.route('/products/api', methods=['GET'])  
@login_required
def get_products_api():
    try:
        products = ProductService.get_products()
        product_list = [product.to_dict() for product in products]  
        return jsonify({"products": product_list}) 
    except RuntimeError as e:
        return jsonify({"error": str(e)}, 500) 