
"""
Bu dosya, projede kullanılan Karınca Kolonisi Optimizasyonu (ACO) algoritmasını barındırır.
ACO : Teknik ekibin Uşak mahalleleri arasındaki en hızlı rotayı bulması için doğadaki karıncaların iz bırakma davranışını matematiksel olarak simüle etmektir.

"""

import numpy as np
import random
from core.gmaps_utils import hesapla_cekicilik

"""
Olasılık Hesaplama Fonksiyonu ( olasilik_hesapla ): Karıncanın gideceği bir sonraki durağına karar verme işlemidir.
mevcut: Karıncanın bulunduğu mahallenin indeksidir.
ziyaret_edilmemisler:Karıncaların henüz uğramadığı mahallelerin listesidir.
feromon : Karıncaların yollara bıraktığı kokudur.Daha kısa yollarda feromon kokusu daha baskın olacaktır.
cekicilik : Yolun ne kadar cazip olduğudur (1/mesafe)
alpha : Feromonun  ne kadar önemli olduğunu belirleyen değerdir. Alpha değeri yüksekse ,karıncalar sürü psikolojisi ile hareket ederler.
beta : Çekiciliğin önemini belirten değerdir. Beta değeri yüksekse karıncalar en kısa yolu tercih ederler.

"""
def olasilik_hesapla(mevcut, ziyaret_edilmemisler, feromon, cekicilik, alpha, beta):
    toplam = 0
    olasiliklar = {}
    for j in ziyaret_edilmemisler:
        deger = (feromon[mevcut][j] ** alpha) * (cekicilik[mevcut][j] ** beta) # Karıncanın karar denklemi
        olasiliklar[j] = deger
        toplam += deger
    for j in olasiliklar:
        olasiliklar[j] /= toplam if toplam > 0 else 1
    return olasiliklar

"""
Karınca Gezi Fonksiyonu (karinca_gezi) : Bu fonksiyon karıncanın tüm mahalleleri gezip tekrar başlangıç mahallesine geldiği turu temsil eden fonksiyondur.

"""
def karinca_gezi(baslangic, mesafe, feromon, cekicilik, alpha, beta):
    n = len(mesafe)
    yol = [baslangic]
    toplam_sure = 0
    while len(yol) < n:
        mevcut = yol[-1]
        ziyaret_edilmemisler = list(set(range(n)) - set(yol))
        olasiliklar = olasilik_hesapla(mevcut, ziyaret_edilmemisler, feromon, cekicilik, alpha, beta)
        secilen = np.random.choice(list(olasiliklar.keys()), p=list(olasiliklar.values()))
        toplam_sure += mesafe[mevcut][secilen]
        yol.append(secilen)
    toplam_sure += mesafe[yol[-1]][yol[0]]
    yol.append(yol[0])
    return yol, toplam_sure


"""
ACO Run Fonksiyonu (run_aco) :Tüm karıncaları kullanarak en iyi mesafeyi güncelleyen fonksiyondur.
Q (Feromon Sabiti ) :Bir karınca turunu tamamladığında, geçtiği yollara ne kadar feromon bırakacağını belirleyen temel değerdir.
"""

def run_aco(mesafe, karinca_sayisi, iterasyon_sayisi, alpha, beta, buharlasma_orani, Q):
    feromon = np.ones_like(mesafe) * 0.1 #Başlangıçta her karıncanın bıraktığı feromon miktarı.
    cekicilik = hesapla_cekicilik(mesafe)
    en_iyi_yol, en_kisa_sure = None, float("inf")
    gecmis = []

    for _ in range(iterasyon_sayisi):
        yollar = []
        for _ in range(karinca_sayisi):
            yol, sure = karinca_gezi(random.randint(0, len(mesafe) - 1), mesafe, feromon, cekicilik, alpha, beta)
            yollar.append((yol, sure))
            if sure < en_kisa_sure:
                en_kisa_sure, en_iyi_yol = sure, yol

        feromon *= (1 - buharlasma_orani)
        for yol, sure in yollar:
            katki = Q / sure
            for i in range(len(yol) - 1):
                feromon[yol[i]][yol[i + 1]] += katki
        gecmis.append(en_kisa_sure)
    return en_iyi_yol, en_kisa_sure, gecmis