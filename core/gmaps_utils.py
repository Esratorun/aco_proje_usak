"""
Bu dosya (gmaps_utils.py) projenin veri tedariği için oluşturulmuştur.
Google MapS API kullanarak Uşak ilindeki 15 mahallenin gerçek zamanlı sürüş sürelerini ve mesafeleri çeker.Bir matrise dönüştürür.

"""

import numpy as np
import googlemaps
import os
from dotenv import load_dotenv
from data.coordinates import MAHALLE_ADLARI

load_dotenv()
gmaps_key = os.getenv("GOOGLE_MAPS_API_KEY")

gmaps = None
if gmaps_key and gmaps_key.startswith("AIza"):
    try:
        gmaps = googlemaps.Client(key=gmaps_key)  #Burada Google Maps servislerine bağlanmak için bir client oluşturuyoruz.
    except:
        gmaps = None
"""
Mesafe Matrisi Oluşturma Fonksiyonu (mesafe_matrisi_olustur): Bu fonksiyonla bir mahallenin diğer mahallelere uzaklıkları hesaplanıp matris haline getirilir.

"""

def mesafe_matrisi_olustur():
    n = len(MAHALLE_ADLARI)
    sure_matrisi = np.zeros((n, n))
    km_matrisi = np.zeros((n, n))

    if not gmaps:
        for i in range(n):
            for j in range(n):
                if i == j:
                    sure_matrisi[i][j] = np.inf
                    km_matrisi[i][j] = 0
                else:
                    rastgele_sure = np.random.randint(5, 30)
                    sure_matrisi[i][j] = rastgele_sure
                    km_matrisi[i][j] = (rastgele_sure / 60) * 40 + np.random.uniform(0.1, 0.9)
        return sure_matrisi, km_matrisi

    for i in range(n):
        for j in range(n):
            if i == j:
                sure_matrisi[i][j] = np.inf
                km_matrisi[i][j] = 0
                continue
            try:
                #Adreslerin sonuna ", Uşak, Turkey" ekliyoruz.
                result = gmaps.distance_matrix(
                    origins=[f"{MAHALLE_ADLARI[i]}, Uşak, Turkey"],
                    destinations=[f"{MAHALLE_ADLARI[j]}, Uşak, Turkey"],
                    mode="driving"
                )

                # API'den gelen veriyi kontrol et (Eleman var mı?) yoksa eğer varsaydığım değerleri ata
                status = result['rows'][0]['elements'][0]['status']
                if status == "OK":
                    sure_saniye = result['rows'][0]['elements'][0]['duration']['value']
                    sure_matrisi[i][j] = sure_saniye / 60.0

                    metre_verisi = result['rows'][0]['elements'][0]['distance']['value']
                    km_matrisi[i][j] = metre_verisi / 1000.0
                else:
                    #Varsaydığım değerler
                    sure_matrisi[i][j] = 99
                    km_matrisi[i][j] = 5.0
            except Exception as e:
                #Herhangi bir hata olursa terminalde göster.
                print(f"Hata oluştu ({MAHALLE_ADLARI[i]} -> {MAHALLE_ADLARI[j]}): {e}")
                sure_matrisi[i][j] = 99
                km_matrisi[i][j] = 5.0

    return sure_matrisi, km_matrisi

"""
Çekicilik Hesaplama Fonksiyonu (hesapla_cekicilik): Bu fonksiyonla yolun çekiciliği hesaplanır.Mesafe küçükse yol daha çekicidir(1/mesafe).
Karıncalar çekiciliği yüksek olan yolu tercih etme eğilimi gösterirler.
"""

def hesapla_cekicilik(mesafe):
    cekicilik = np.zeros_like(mesafe)
    with np.errstate(divide='ignore'):
        cekicilik = 1 / mesafe
        cekicilik[mesafe == np.inf] = 0
    return cekicilik