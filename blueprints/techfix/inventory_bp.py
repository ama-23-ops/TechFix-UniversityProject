from flask import Blueprint, jsonify, render_template
from services.inventory_service import InventoryService
from flask_login import login_required

# Initialize the blueprint
inventory_bp = Blueprint('techfix_inventory', __name__, url_prefix='/techfix')

# Route to display the inventory page
@inventory_bp.route('/inventory', methods=['GET'])
@login_required
def get_inventory_page():
    # Fetch inventory for all suppliers 
    inventory_items = InventoryService.get_inventory()
    return render_template('techfix/inventory.html', inventory_items=inventory_items)

# API route to get inventory data as JSON
@inventory_bp.route('/inventory/api', methods=['GET'])
@login_required
def get_inventory_api():
    try:
        # Fetch inventory for all suppliers 
        inventory_items = InventoryService.get_inventory()
        inventory_list = [item.to_dict() for item in inventory_items]
        return jsonify({"inventory": inventory_list})  
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500