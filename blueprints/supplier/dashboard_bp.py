from flask import Blueprint, render_template
from flask_login import login_required

dashboard_bp = Blueprint('supplier_dashboard', __name__, url_prefix='/supplier/dashboard')  

@dashboard_bp.route('/')
@login_required
def dashboard():
    return render_template('supplier/dashboard.html')