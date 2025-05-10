from flask import Blueprint, render_template, redirect, url_for, request, flash
from services.auth_service import AuthService
from flask_login import login_user, logout_user, login_required, current_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/') # Added root route
def index():
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = AuthService.authenticate_user(username, password)

        if user:
            login_user(user)
            if user.role == 'techfix':
                return redirect(url_for('techfix_dashboard.dashboard'))  #TechFix dashboard route
            elif user.role == 'supplier':
                return redirect(url_for('supplier_dashboard.dashboard'))  # Supplier dashboard route
            else:
                return 'something went wrong'
        else:
            flash('Invalid username or password', 'error')
            return render_template('auth/login.html')  # Stay on the login page with an error message

    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))