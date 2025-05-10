from flask import Blueprint, render_template, redirect, url_for, request, flash
from services.auth_service import AuthService
from services.supplier_service import SupplierService
from flask_login import login_required

supplier_management_bp = Blueprint('supplier_management', __name__, url_prefix='/suppliers')

@supplier_management_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_supplier():
    if request.method == 'POST':
        name = request.form.get('name')
        contact_email = request.form.get('contact_email')
        phone_number = request.form.get('phone_number')
        address = request.form.get('address')
        contact_person = request.form.get('contact_person')
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            # Create the supplier first
            supplier = SupplierService.create_supplier({
                'name': name,
                'contact_email': contact_email,
                'phone_number': phone_number,
                'address': address,
                'contact_person': contact_person
            })

            # Then create the user, linking to the supplier
            AuthService.create_user(username, password, 'supplier', supplier.id)

            flash('Supplier created successfully!', 'success')
            return redirect(url_for('supplier_management.list_suppliers'))
        except Exception as e:
            flash(f'Error creating supplier: {str(e)}', 'error')
            return render_template('techfix/supplier_management/create_supplier.html')

    return render_template('techfix/supplier_management/create_supplier.html')

@supplier_management_bp.route('/')
@login_required
def list_suppliers():
    suppliers = SupplierService.get_suppliers()
    return render_template('techfix/supplier_management/list_suppliers.html', suppliers=suppliers)

@supplier_management_bp.route('/<int:supplier_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_supplier(supplier_id):
    supplier = SupplierService.get_supplier(supplier_id)
    if not supplier:
        flash('Supplier not found.', 'error')
        return redirect(url_for('supplier_management.list_suppliers'))

    if request.method == 'POST':
        name = request.form.get('name')
        contact_email = request.form.get('contact_email')
        phone_number = request.form.get('phone_number')
        address = request.form.get('address')
        contact_person = request.form.get('contact_person')

        try:
            SupplierService.update_supplier(supplier_id, {
                'name': name,
                'contact_email': contact_email,
                'phone_number': phone_number,
                'address': address,
                'contact_person': contact_person
            })
            flash('Supplier updated successfully!', 'success')
            return redirect(url_for('supplier_management.list_suppliers'))
        except Exception as e:
            flash(f'Error updating supplier: {str(e)}', 'error')
            return render_template('techfix/supplier_management/edit_supplier.html', supplier=supplier)

    return render_template('techfix/supplier_management/edit_supplier.html', supplier=supplier)

@supplier_management_bp.route('/<int:supplier_id>/delete', methods=['POST'])
@login_required
def delete_supplier(supplier_id):
    try:
        SupplierService.delete_supplier(supplier_id)
        flash('Supplier deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting supplier: {str(e)}', 'error')
    return redirect(url_for('supplier_management.list_suppliers'))