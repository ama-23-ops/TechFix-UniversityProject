from flask import Blueprint, request, jsonify
from services.quotation_service import QuotationService 
from flask import Blueprint, render_template

quotation_bp = Blueprint('supplier_quotation', __name__)

@quotation_bp.route('/list', methods=['GET'])
def get_quotations():
    quotations = QuotationService.get_quotations() 
    return render_template('supplier/quotations.html', quotations=quotations)

@quotation_bp.route('/respond', methods=['POST'])
def respond_to_quotation():
    data = request.json
    quotation_id = data.get('quotation_id')
    response_data = data.get('response_data')
    quotation = SupplierQuotationService.respond_to_quotation(quotation_id, response_data)
    return jsonify(quotation.to_dict())