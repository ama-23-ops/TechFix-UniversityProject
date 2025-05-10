from models import User, db
import bcrypt

class AuthService:

    @staticmethod
    def create_user(username, password, role, supplier_id=None):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_user = User(username=username, password_hash=hashed_password.decode('utf-8'), role=role, supplier_id=supplier_id)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def authenticate_user(username, password):
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            return user
        return None

    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()