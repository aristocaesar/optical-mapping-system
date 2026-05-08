from app import create_app, db
from app.models.users import User
from app.models.sessions import Session
from app.models.session_data import SessionData
from werkzeug.security import generate_password_hash

app = create_app()

def seed_data():
    with app.app_context():
        # Clear existing data
        db.session.query(User).delete()
        
        users_data = [
            {'fullname': 'Dermawan Hadi Putra', 'email': 'dermawan@ocm.web.id'},
            {'fullname': 'Fauzan Hakim', 'email': 'fauzan@ocm.web.id'},
            {'fullname': 'Gabriel Caubatji Chatay', 'email': 'gabriel@ocm.web.id'}
        ]
        
        for u in users_data:
            new_user = User(
                fullname=u['fullname'],
                email=u['email'],
                password=generate_password_hash('cablemap123')
            )
            db.session.add(new_user)
        
        db.session.commit()
        
        print("Database seeded successfully!")
        
if __name__ == '__main__':
    seed_data()
