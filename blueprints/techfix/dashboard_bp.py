from flask import Blueprint, render_template
from flask_login import login_required

dashboard_bp = Blueprint('techfix_dashboard', __name__, url_prefix='')

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('techfix/dashboard.html')