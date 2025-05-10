from flask import Flask
from models import db
from blueprints.auth_bp import auth_bp
from blueprints.techfix.product_bp import product_bp as techfix_product_bp
from blueprints.techfix.order_bp import order_bp as techfix_order_bp
from blueprints.techfix.inventory_bp import inventory_bp as techfix_inventory_bp
from blueprints.techfix.quotation_bp import quotation_bp as techfix_quotation_bp
from blueprints.techfix.dashboard_bp import dashboard_bp as techfix_dashboard_bp
from blueprints.techfix.supplier_management_bp import supplier_management_bp
from blueprints.supplier.product_bp import product_bp as supplier_product_bp
from blueprints.supplier.quotation_bp import quotation_bp as supplier_quotation_bp
from blueprints.supplier.inventory_bp import inventory_bp as supplier_inventory_bp
from blueprints.supplier.dashboard_bp import dashboard_bp as supplier_dashboard_bp
from blueprints.supplier.order_bp import order_bp as supplier_order_bp
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/techfix_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key' 

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # Redirect to login if not authenticated

@login_manager.user_loader
def load_user(user_id):
    from models import User  # Import inside the function to avoid circular imports
    return User.query.get(int(user_id))  # Assuming user_id is an integer

# Register Blueprints
app.register_blueprint(auth_bp)

# Register TechFix Blueprints
app.register_blueprint(techfix_product_bp, url_prefix='/techfix')
app.register_blueprint(techfix_order_bp, url_prefix='/techfix/orders')
app.register_blueprint(techfix_inventory_bp, url_prefix='/techfix')
app.register_blueprint(techfix_quotation_bp, url_prefix='/techfix/quotations')
app.register_blueprint(techfix_dashboard_bp, url_prefix='/techfix')
app.register_blueprint(supplier_management_bp, url_prefix='/techfix')

# Register Supplier Blueprints
app.register_blueprint(supplier_product_bp, url_prefix='/supplier')
app.register_blueprint(supplier_quotation_bp, url_prefix='/supplier/quotations')
app.register_blueprint(supplier_inventory_bp, url_prefix='/supplier')
app.register_blueprint(supplier_dashboard_bp, url_prefix='/supplier')
app.register_blueprint(supplier_order_bp, url_prefix='/supplier/orders')

# Create tables in the database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)