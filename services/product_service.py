from models import Product, db
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import Schema, fields, ValidationError

class ProductSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str()
    price = fields.Float(required=True, validate=lambda p: p > 0)
    category = fields.Str()

class ProductService:

    @staticmethod
    def create_product(data, supplier_id):
        try:
            schema = ProductSchema()
            validated_data = schema.load(data)
            new_product = Product(
                name=validated_data['name'],
                description=validated_data.get('description'),
                price=validated_data['price'],
                category=validated_data.get('category', 'General'),
                supplier_id = supplier_id
            )
            db.session.add(new_product)
            db.session.commit()
            return new_product
        except ValidationError as e:
            db.session.rollback()
            raise ValueError(f"Validation error: {str(e)}")
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RuntimeError(f"Database error: {str(e)}")

    @staticmethod
    def get_product(product_id):
        try:
            return Product.query.get(product_id)
        except SQLAlchemyError as e:
            raise RuntimeError(f"Database error: {str(e)}")

    @staticmethod
    def get_products():
        try:
            return Product.query.all()
        except SQLAlchemyError as e:
            raise RuntimeError(f"Database error: {str(e)}")

    @staticmethod
    def get_products_by_supplier_id(supplier_id):
        try:
            return Product.query.filter_by(supplier_id=supplier_id).all()
        except SQLAlchemyError as e:
            raise RuntimeError(f"Database error: {str(e)}")

    @staticmethod
    def update_product(product_id, data, supplier_id):
        try:
            schema = ProductSchema()
            validated_data = schema.load(data)
            product = Product.query.get(product_id)
            if product and product.supplier_id == supplier_id:
                product.name = validated_data.get('name', product.name)
                product.description = validated_data.get('description', product.description)
                product.price = validated_data.get('price', product.price)
                product.category = validated_data.get('category', product.category)
                db.session.commit()
                return product
            else:
                return None  # Product not found or doesn't belong to supplier
        except ValidationError as e:
            db.session.rollback()
            raise ValueError(f"Validation error: {str(e)}")
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RuntimeError(f"Database error: {str(e)}")

    @staticmethod
    def delete_product(product_id, supplier_id):
        try:
            product = Product.query.get(product_id)
            if product and product.supplier_id == supplier_id:
                db.session.delete(product)
                db.session.commit()
                return product
            else:
                return None #product doesnt belong to user
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RuntimeError(f"Database error: {str(e)}")