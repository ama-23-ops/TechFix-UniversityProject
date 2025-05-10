from flask import Blueprint, jsonify, request, render_template
from services.product_service import ProductService
from flask_login import login_required, current_user

product_bp = Blueprint('supplier_product', __name__, url_prefix='/supplier')

@product_bp.route('/products', methods=['GET'])
@login_required
def get_products_page():
    return render_template('supplier/products.html')

@product_bp.route('/products/api', methods=['GET'])
@login_required
def get_products():
    try:
        supplier_id = current_user.supplier_id
        products = ProductService.get_products_by_supplier_id(supplier_id)
        product_list = [product.to_dict() for product in products]
        return jsonify({"products": product_list})
    except RuntimeError as e:
        return jsonify({"error": str(e)}, 500)

@product_bp.route('/products/add', methods=['POST'])
@login_required
def add_product():
    try:
        data = request.get_json()
        supplier_id = current_user.supplier_id
        product = ProductService.create_product(data, supplier_id)
        return jsonify({"product": product.to_dict()}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except RuntimeError as e:
        return jsonify({"error": str(e)}, 500)
        
@product_bp.route('/products/<int:product_id>/delete', methods=['POST'])
@login_required
def delete_product(product_id):
    try:
        supplier_id = current_user.supplier_id
        product = ProductService.delete_product(product_id,supplier_id)
        return jsonify({"message": "product Deleted successfully"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except RuntimeError as e:
        return jsonify({"error": str(e)}, 500)

@product_bp.route('/products/<int:product_id>/update', methods=['PUT'])
@login_required
def update_product(product_id):
    try:
        data = request.get_json()
        supplier_id = current_user.supplier_id
        product = ProductService.update_product(product_id, data, supplier_id)
        if product:
            return jsonify({"product": product.to_dict()}), 200
        else:
            return jsonify({"error": "Product not found or unauthorized"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except RuntimeError as e:
        return jsonify({"error": str(e)}, 500)