from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required, current_user
from services.inventory_service import InventoryService
from models import db, Product 
from sqlalchemy.exc import SQLAlchemyError  

# Initialize the blueprint
inventory_bp = Blueprint('supplier_inventory', __name__, url_prefix='/supplier')

# Route to render the HTML template
@inventory_bp.route('/inventory', methods=['GET'])
@login_required
def get_inventory_page():
    supplier_id = current_user.supplier_id
    inventory_items = InventoryService.get_inventory(supplier_id)
    return render_template('supplier/inventory.html', inventory_items=inventory_items)

# Route to return JSON data 
@inventory_bp.route('/inventory/api', methods=['GET'])
@login_required
def get_inventory_api():
    try:
        supplier_id = current_user.supplier_id
        inventory_items = InventoryService.get_inventory(supplier_id)
        inventory_list = [item.to_dict() for item in inventory_items]
        return jsonify({"inventory": inventory_list})
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

# Route to add inventory
@inventory_bp.route('/inventory/add', methods=['POST'])
@login_required
def add_inventory():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Ensure the supplier_id matches the logged-in supplier
        supplier_id = current_user.supplier_id

        # Validate product_id exists for this supplier
        product = Product.query.filter_by(id=data['product_id'], supplier_id=supplier_id).first()
        if not product:
            return jsonify({"error": "Product not found for this supplier."}), 400

        # Create the inventory item
        inventory = InventoryService.create_inventory(data, supplier_id)
        return jsonify({"inventory": inventory.to_dict()}), 201
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

# Route to update inventory
@inventory_bp.route('/inventory/<int:inventory_id>/update', methods=['PUT'])
@login_required
def update_inventory_item(inventory_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Ensure the supplier_id matches the logged-in supplier
        supplier_id = current_user.supplier_id

        # Update the inventory item
        inventory = InventoryService.update_inventory(inventory_id, data, supplier_id)
        if inventory is None:
            return jsonify({"error": "Inventory item not found or not owned by this supplier"}), 404
        return jsonify({"inventory": inventory.to_dict()})
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

# Route to delete inventory
@inventory_bp.route('/inventory/<int:inventory_id>/delete', methods=['DELETE'])
@login_required
def delete_inventory_item(inventory_id):
    try:
        supplier_id = current_user.supplier_id

        # Delete the inventory item
        inventory = InventoryService.delete_inventory(inventory_id, supplier_id)
        if inventory is None:
            return jsonify({"error": "Inventory item not found or not owned by this supplier"}), 404
        return jsonify({"message": "Inventory item deleted successfully"})
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500