"""
Bu dosya (coordinates.py) projenin coğrafi verilerini tutar.
Algoritmanın mahallelerdeki hangi noktalar arasında rota çizeceğinin bilgileri burada tutulur.

"""
MAHALLE_VERILERI = [
    {"ad": "Cumhuriyet Mahallesi", "lat": 38.6822, "lon": 29.4145},
    {"ad": "Atatürk Mahallesi", "lat": 38.6815, "lon": 29.3885},
    {"ad": "Kemalöz Mahallesi", "lat": 38.6655, "lon": 29.3952},
    {"ad": "Fatih Mahallesi", "lat": 38.6758, "lon": 29.4125},
    {"ad": "Karaağaç Mahallesi", "lat": 38.6845, "lon": 29.4082},
    {"ad": "Ünalan Mahallesi", "lat": 38.6728, "lon": 29.4048},
    {"ad": "İslice Mahallesi", "lat": 38.6745, "lon": 29.4015},
    {"ad": "Kurtuluş Mahallesi", "lat": 38.6772, "lon": 29.3985},
    {"ad": "Sarayaltı Mahallesi", "lat": 38.6885, "lon": 29.4012},
    {"ad": "Dikilitaş Mahallesi", "lat": 38.6785, "lon": 29.4105},
    {"ad": "Mehmet Akif Ersoy Mah.", "lat": 38.6620, "lon": 29.4215},
    {"ad": "Özdemir Mahallesi", "lat": 38.6710, "lon": 29.4090},
    {"ad": "Köme Mahallesi", "lat": 38.6735, "lon": 29.4120},
    {"ad": "Işık Mahallesi", "lat": 38.6690, "lon": 29.4150},
    {"ad": "Elmalıdere Mahallesi", "lat": 38.6580, "lon": 29.4050}
]

MAHALLE_ADLARI = [m["ad"] for m in MAHALLE_VERILERI]