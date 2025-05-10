# services/supplier_service.py
from marshmallow import Schema, fields, ValidationError
from models import Supplier, db
from sqlalchemy.exc import SQLAlchemyError

class SupplierSchema(Schema):
    name = fields.Str(required=True)
    contact_email = fields.Email(required=True)
    phone_number = fields.Str()
    address = fields.Str()
    contact_person = fields.Str()

class SupplierService:
    @staticmethod
    def create_supplier(data):
        new_supplier = Supplier(
            name=data['name'],
            contact_email=data['contact_email'],
            phone_number=data.get('phone_number'),
            address=data.get('address'),
            contact_person=data.get('contact_person')
        )
        db.session.add(new_supplier)
        db.session.commit()
        return new_supplier

    @staticmethod
    def get_supplier(supplier_id):
      return Supplier.query.get(supplier_id)

    @staticmethod
    def get_suppliers():
        return Supplier.query.all()

    @staticmethod
    def update_supplier(supplier_id, data):
        try:
            schema = SupplierSchema()
            validated_data = schema.load(data)
            supplier = Supplier.query.get(supplier_id)
            if supplier:
                supplier.name = validated_data.get('name', supplier.name)
                supplier.contact_email = validated_data.get('contact_email', supplier.contact_email)
                supplier.phone_number = validated_data.get('phone_number', supplier.phone_number)
                supplier.address = validated_data.get('address', supplier.address)
                supplier.contact_person = validated_data.get('contact_person', supplier.contact_person)
                db.session.commit()
                return supplier
            else:
                return None  # Supplier not found
        except ValidationError as e:
            db.session.rollback()
            raise ValueError(f"Validation error: {str(e)}")
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RuntimeError(f"Database error: {str(e)}")

    @staticmethod
    def delete_supplier(supplier_id):
        supplier = Supplier.query.get(supplier_id)
        if supplier:
            db.session.delete(supplier)
            db.session.commit()
        return supplier