from app import app
from models import db, User
from services.auth_service import AuthService

with app.app_context():
    # Check if an admin user already exists
    admin_user = User.query.filter_by(role='techfix').first()
    if admin_user:
        print("An admin user already exists. Skipping creation.")
    else:
        # Create a new admin user
        AuthService.create_user(
            username='admin',  
            password='password',  
            role='techfix'
        )
        db.session.commit()
        print("Admin user created successfully.")