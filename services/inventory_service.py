from models import Inventory, db
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import Schema, fields, ValidationError

class InventorySchema(Schema):
    product_id = fields.Integer(required=True)
    stock_quantity = fields.Integer(required=True, validate=lambda q: q >= 0)

class InventoryService:
    @staticmethod
    def create_inventory(data, supplier_id):
        try:
            validated_data = InventorySchema().load(data)
            new_inventory = Inventory(
                supplier_id=supplier_id,
                product_id=validated_data['product_id'],
                stock_quantity=validated_data['stock_quantity']
            )
            db.session.add(new_inventory)
            db.session.commit()
            return new_inventory
        except ValidationError as e:
            db.session.rollback()
            raise ValueError(f"Validation error: {str(e)}")
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RuntimeError(f"Database error: {str(e)}")

    @staticmethod
    def get_inventory(supplier_id=None):
        try:
            if supplier_id:
                # Fetch inventory for a specific supplier
                return Inventory.query.filter_by(supplier_id=supplier_id).all()
            else:
                # Fetch inventory for all suppliers (for TechFix)
                return Inventory.query.all()
        except SQLAlchemyError as e:
            raise RuntimeError(f"Database error: {str(e)}")

    @staticmethod
    def update_inventory(inventory_id, data, supplier_id):
        try:
            validated_data = InventorySchema().load(data)
            inventory = Inventory.query.filter_by(id=inventory_id, supplier_id=supplier_id).first()
            if inventory:
                inventory.stock_quantity = validated_data.get('stock_quantity', inventory.stock_quantity)
                db.session.commit()
                return inventory
            return None
        except ValidationError as e:
            db.session.rollback()
            raise ValueError(f"Validation error: {str(e)}")
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RuntimeError(f"Database error: {str(e)}")

    @staticmethod
    def delete_inventory(inventory_id, supplier_id):
        try:
            inventory = Inventory.query.filter_by(id=inventory_id, supplier_id=supplier_id).first()
            if inventory:
                db.session.delete(inventory)
                db.session.commit()
                return inventory
            return None
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RuntimeError(f"Database error: {str(e)}")