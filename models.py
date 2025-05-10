from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Instantiate the database

# User Model
class User(UserMixin, db.Model):  # Inherit from UserMixin
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'techfix' or 'supplier'
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'supplier_id': self.supplier_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

# Supplier Model
class Supplier(db.Model):
    __tablename__ = 'suppliers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_email = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    contact_person = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Supplier {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'contact_email': self.contact_email,
            'phone_number': self.phone_number,
            'address': self.address,
            'contact_person': self.contact_person,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

# Product Model
class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "category": self.category,
            "supplier_id": self.supplier_id,
            "created_at": self.created_at.isoformat()
        }

# Inventory Model
class Inventory(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    supplier = db.relationship('Supplier', backref=db.backref('inventories', lazy=True))
    product = db.relationship('Product', backref=db.backref('inventories', lazy=True))

    def __repr__(self):
        return f'<Inventory {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'supplier_id': self.supplier_id,
            'product_id': self.product_id,
            'stock_quantity': self.stock_quantity,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

# Quotation Model
class Quotation(db.Model):
    __tablename__ = 'quotations'

    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    product_ids = db.Column(db.JSON, nullable=False)  # List of product IDs
    quantities = db.Column(db.JSON, nullable=False)  # List of quantities
    total_cost = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="Pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "supplier_id": self.supplier_id,
            "product_ids": self.product_ids,
            "quantities": self.quantities,
            "total_cost": self.total_cost,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

# Order Model
class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    quotation_id = db.Column(db.Integer, db.ForeignKey('quotations.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="Placed")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "quotation_id": self.quotation_id,
            "supplier_id": self.supplier_id,
            "total_cost": self.total_cost,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }