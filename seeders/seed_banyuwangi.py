import sys
import os
import random
from datetime import datetime

# Add the parent directory to sys.path to allow imports from app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.sessions import Session
from app.models.session_data import SessionData

app = create_app()

def seed_banyuwangi():
    with app.app_context():
        # Create a session
        session_id_str = f"OCM-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        new_session = Session(session_id=session_id_str, name="Jalur Banyuwangi Kota", is_active=False)
        db.session.add(new_session)
        db.session.commit()
        
        session_id = new_session.id
        
        # Start coordinates near Banyuwangi City
        lat = -8.219233
        lon = 114.369227
        
        # Generate 25 points
        for i in range(25):
            # Move slightly south and east
            lat -= 0.00015
            lon += 0.00020
            
            # Generate random score to get a mix of categories
            # 0-49 (Buruk), 50-74 (Cukup Baik), 75-100 (Baik)
            rand_val = random.random()
            if rand_val < 0.33:
                score = random.uniform(30, 49)  # Merah
            elif rand_val < 0.66:
                score = random.uniform(55, 74)  # Kuning
            else:
                score = random.uniform(76, 95)  # Hijau
                
            # Create SessionData
            geom = f'SRID=4326;POINT({lon} {lat})'
            data = SessionData(
                session_id=session_id,
                lat=lat,
                lon=lon,
                ec=random.uniform(0.1, 2.5),
                ph=random.uniform(5.0, 8.0),
                hum=random.uniform(10, 30),
                temp=random.uniform(25, 35),
                n=random.randint(20, 100),
                p=random.randint(20, 100),
                k=random.randint(20, 100),
                score=round(score, 2)
            )
            db.session.add(data)
            
        db.session.commit()
        print(f"Berhasil menambahkan 1 Sesi ({session_id_str}) dan 25 Session Data di Banyuwangi.")

if __name__ == '__main__':
    seed_banyuwangi()
