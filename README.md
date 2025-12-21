**BU PROJEDE :**

Uşak Teknik Ekip Rota Optimizasyon Sistemi (ACO tabanlı)
Bu proje, Uşak ilindeki 15 farklı mahallede görev yapan teknik ekiplerin günlük iş planlarını en verimli şekilde organize etmek için geliştirilmiş bir Karar Destek Sistemi'dir. Sistem, Karınca Kolonisi Optimizasyonu (ACO) algoritmasını kullanarak, Google Maps'ten alınan gerçek zamanlı trafik verileriyle en kısa süreli rotayı hesaplar.


**ÖNE ÇIKAN ÖZELLİKLER:**

**Gerçek Zamanlı Veri**: Google Maps Distance Matrix API entegrasyonu ile mahalleler arası mesafe ve süre verileri anlık çekilir.

**Gelişmiş Algoritma:** Karınca Kolonisi Optimizasyonu (ACO) ile karmaşık rota problemleri saniyeler içinde çözülür.

**Dinamik Saha Koşulları:** Yağmurlu ve karlı hava gibi zorlu şartlar için özel katsayılarla seyahat süresi simülasyonu yapılır.

**İnteraktif Arayüz:** Streamlit tabanlı kullanıcı paneli üzerinden algoritma parametreleri (alpha, beta, karınca sayısı) anlık olarak değiştirilebilir.

**Görsel Analiz:** Pydeck ile harita üzerinde numaralandırılmış rota çizimi ve NetworkX ile dairesel iş akış şeması sunulur.

**PROJE YAPISI**


aco_proje_usak/
├── core/
│   ├── ant_algorithm.py    # ACO algoritmasının matematiksel motoru
│   └── gmaps_utils.py      # Google Maps API ve veri işleme araçları
├── data/
│   └── coordinates.py      # Uşak mahalle koordinat ve isim verileri
├── figure/
│   └── convergence.png     # Algoritmanın öğrenme sürecini gösteren grafik
│   └── route_map.png       # Optimize Edilmiş Rota Haritasını gösteren şema
├── .env                    # API anahtarı (Gizli tutulmalıdır)
├── config.py               # Varsayılan algoritma konfigürasyonları
├── main.py                 # Konsol üzerinden test dosyası
├── streamlit_app.py        # Ana görselleştirme paneli
└── requirements.txt        # Gerekli Python kütüphaneleri

**KURULUM VE ÇALIŞTIRMA:**

**Gerekli Kütüphaneleri Yükleyin:**


pip install -r requirements.txt
API Anahtarını Ayarlayın: .env dosyası oluşturun ve içine geçerli Google Maps API anahtarınızı ekleyin:

Plaintext

GOOGLE_MAPS_API_KEY="ANAHTARINIZI_BURAYA_YAZIN"
Uygulamayı Başlatın:


streamlit run streamlit_app.py

**ALGORİTMA NASIL ÇALIŞIR?**

Sistem, doğadaki karıncaların yiyecek bulurken bıraktıkları feromon izlerini taklit eder.

**Başlangıç:** Her iterasyonda 15 sanal karınca rastgele noktalardan yola çıkar.

**Karar Verme:** Karıncalar bir sonraki mahalleyi seçerken hem yolun kısalığına (Beta) hem de önceki karıncaların tecrübesine (Alpha) bakar.

**Güncelleme:** En kısa yolu bulan karıncanın geçtiği yollara daha fazla feromon bırakılır, kötü yollardaki izler ise zamanla buharlaşır (Evaporation).

**Sonuç:** Belirlenen iterasyon sonunda sistem, Uşak için teorik olarak en verimli rotayı dairesel olarak tamamlar.

**ANALİZ VE ÇIKTILAR:**

**Süre İyileşme Grafiği:** Algoritmanın her denemede daha hızlı bir rota bulduğunu kanıtlar.

**İş Planı Tablosu:** Teknik ekibe hangi sırayla hangi mahalleye gitmesi gerektiğini, kaç km yol yapacağını ve tahmini varış süresini raporlar.

Bu proje, optimizasyon algoritmalarının gerçek hayat problemlerine (Lojistik ve Saha Yönetimi) uygulanabilirliğini göstermek amacıyla geliştirilmiştir.