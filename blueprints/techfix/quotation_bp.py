from flask import Blueprint, jsonify, render_template, request
from services.quotation_service import QuotationService
from services.product_service import ProductService
from flask_login import login_required

quotation_bp = Blueprint('techfix_quotation', __name__, url_prefix='/techfix')

@quotation_bp.route('/quotations', methods=['GET'])
@login_required
def get_quotations_page():
    """
    Render the Quotation Page with a list of quotations.
    """
    quotations = QuotationService.get_quotations()
    return render_template('techfix/quotations.html', quotations=quotations)

@quotation_bp.route('/quotations/api/products', methods=['GET'])
@login_required
def get_products_api():
    """
    Fetch all products for selection on the Quotation Page.
    """
    try:
        products = ProductService.get_products()
        product_list = [product.to_dict() for product in products]
        return jsonify({"products": product_list}), 200
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    
    from flask import Blueprint, render_template
from services.quotation_service import QuotationService

quotation_bp = Blueprint('quotation', __name__)

@quotation_bp.route('/list', methods=['GET'])
def list_quotations():
    """
    Render the Quotation Page with a list of quotations.
    """
    quotations = QuotationService.get_quotations()
    return render_template('techfix/quotations.html', quotations=quotations)

@quotation_bp.route('/api/products', methods=['GET'])
def get_products_route():
    """
    Fetch all products for selection on the Quotation Page.
    """
    try:
        products = ProductService.get_products()
        return jsonify({"products": [product.to_dict() for product in products]}), 200
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    
@quotation_bp.route('/request', methods=['POST'])
def request_quotation():
    """
    Handle quotation requests from the frontend.
    """
    data = request.json
    product_ids = data.get('product_ids')
    quantities = data.get('quantities')
    supplier_id = data.get('supplier_id')

    if not product_ids or not quantities or not supplier_id:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        quotation = QuotationService.request_quotation(product_ids, quantities, supplier_id)
        return jsonify(quotation.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400    
    