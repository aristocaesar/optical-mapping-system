def piecewise_linear(x, points):
    """
    Menghitung nilai Y berdasarkan interpolasi linear (piecewise linear)
    dari titik-titik koordinat (X, Y) yang diberikan.
    points: list of tuples [(x1, y1), (x2, y2), ...] yang diurutkan berdasarkan x
    """
    # Jika di luar batas bawah
    if x <= points[0][0]:
        return points[0][1]
    
    # Jika di luar batas atas
    if x >= points[-1][0]:
        return points[-1][1]
    
    # Interpolasi linear di antara dua titik
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i+1]
        if x1 <= x <= x2:
            return y1 + (x - x1) * (y2 - y1) / (x2 - x1)
            
    return 0

def calculate_piecewise_score(data):
    """
    Menghitung skor kelayakan lahan berdasarkan 4 parameter utama
    (pH, Kelembaban, Suhu, EC) menggunakan fungsi piecewise linear.
    Kategori Nilai Dasar: Baik (100), Cukup (50), Buruk (0)
    Bobot dibagi rata: masing-masing parameter memiliki bobot 25% (0.25).
    """
    
    # Titik interpolasi berdasarkan ambang batas: (Batas Nilai IoT X, Skor Y)
    
    # 1. pH Tanah
    # <5.5 (Buruk), 5.5-6.4 (Cukup->Baik), 6.5-8.5 (Baik), 8.6-9.0 (Baik->Cukup), >9.0 (Buruk)
    ph_points = [
        (4.5, 0), (5.5, 50), (6.5, 100), 
        (8.5, 100), (9.0, 50), (10.0, 0)
    ]
    
    # 2. Kelembaban Tanah
    # 0-5 (Buruk), 5-10 (Cukup), 10-15 (Cukup->Baik), 15-25 (Baik), >25 (Baik->Buruk)
    hum_points = [
        (0, 0), (5, 50), (10, 50), 
        (15, 100), (25, 100), (30, 50), (35, 0)
    ]
    
    # 3. Suhu Tanah
    # <10 (Buruk->Baik), 10-35 (Baik), 36-45 (Baik->Cukup), >45 (Buruk)
    temp_points = [
        (0, 0), (5, 50), (10, 100), 
        (35, 100), (45, 50), (55, 0)
    ]
    
    # 4. Electrical Conductivity (EC)
    # <0.2 (Baik), 0.2-2.0 (Baik->Cukup), >2.0 (Buruk)
    ec_points = [
        (0, 100), (0.2, 100), 
        (2.0, 50), (3.0, 0)
    ]
    
    try:
        ph_val = float(data.get('ph', 0))
        hum_val = float(data.get('hum', 0))
        temp_val = float(data.get('temp', 0))
        ec_val = float(data.get('ec', 0))
    except (TypeError, ValueError):
        # Jika nilai tidak dapat dikonversi, default menjadi 0
        ph_val = hum_val = temp_val = ec_val = 0
    
    # Hitung skor (0-100) untuk masing-masing parameter
    score_ph = piecewise_linear(ph_val, ph_points)
    score_hum = piecewise_linear(hum_val, hum_points)       
    score_temp = piecewise_linear(temp_val, temp_points)
    score_ec = piecewise_linear(ec_val, ec_points)
    
    # Hitung skor total dengan bobot 25% untuk masing-masing
    total_score = (score_ph * 0.35) + (score_hum * 0.20) + (score_temp * 0.15) + (score_ec * 0.30)
    
    return round(total_score, 2)
