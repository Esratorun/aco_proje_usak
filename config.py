"""
Bu dosyada (config.py) Karınca Kolonisi Algoritmasının (ACO) genetik kodlarını ve çalışma alanını belirleyen ayar dosyasıdır.
Bu değerler , algoritmanın rotayı ne kadar hızlı keşfedeceğini belirler.

karinca_sayisi : Her döngüde 15 farklı karınca(sanal ekip) sahaya salınır.Bu değer çok düşük olsaydı en iyi yol gözden kaçabilirdi,çok büyük olsaydı bilgisayar gereksiz yorulurdu.
iterasyon_sayisi : Algoritmanın toplam öğrenme sayısıdır.
alpha (Tecrübe) : Karıncaların önceki karıncaları takip etme isteğidir. Yüksek olursa karıncalar sürü psikolojisi ile hareket etme eğilimine girerler , çok düşük olursa karıncalar kendi bildiğini okuma eğilimine girerler.
beta (Mantık) :En yakın mahalleye gitme isteğidir .(Açgözlülük)
buharlasma_orani: Yollardaki feromonların her adımda ne kadar silineceğini belirler. Algoritmanın eski kötü yolları unutup yeni ve kısa mesafedeki yollara odaklanabilmesini sağlar.
Q : İyi bir rota bulan karıncanın yola bırakacağı ödük miktarı çarpanıdır.Feromon miktarının aşırı yükselip algoritmayı kör etmesimi engeller.

"""

ACO_CONFIG = {
    "karinca_sayisi": 15,
    "iterasyon_sayisi": 50,
    "alpha": 1.0,
    "beta": 2.0,
    "buharlasma_orani": 0.5,
    "Q": 1.0
}