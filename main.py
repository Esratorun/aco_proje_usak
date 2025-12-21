"""
Bu dosyada streamlit arayüzüne girilmeden tüm sistem terminal üzerinden çalıştırılıp kontrol edilecektir.

"""

from core.gmaps_utils import mesafe_matrisi_olustur
from core.ant_algorithm import run_aco
from data.coordinates import MAHALLE_ADLARI
from config import ACO_CONFIG
from visual.plotting import plot_convergence


def main():
    mesafe = mesafe_matrisi_olustur()
    en_iyi_yol, en_iyi_sure, gecmis = run_aco(mesafe, **ACO_CONFIG)

    print(f"\n En Kısa Süre: {en_iyi_sure:.2f} Dakika")
    print(" Rota:", " -> ".join([MAHALLE_ADLARI[i] for i in en_iyi_yol]))

    plot_convergence(gecmis, kaydet=True, dosya_yolu="figure/convergence.png")


if __name__ == "__main__":
    main()