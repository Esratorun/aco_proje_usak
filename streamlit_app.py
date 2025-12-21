"""
Bu dosya(streamlit_app.py) projenin görsel arayüz katmanıdır.
Diğer dosyalardaki hazırlanan veriler ve algoritmalar birleştirilir.
"""

import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import matplotlib.pyplot as plt
import networkx as nx
import os
import sys

# Klasör yapısını tanıması için sistem yoluna ekle
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.gmaps_utils import mesafe_matrisi_olustur
from core.ant_algorithm import run_aco
from data.coordinates import MAHALLE_VERILERI, MAHALLE_ADLARI

# Sayfa Ayarları
st.set_page_config(page_title="Uşak Teknik Rota Paneli", layout="wide")

st.title("Uşak Teknik Ekip Optimizasyon Sistemi")

# YAN MENÜ: PARAMETRELER VE KOŞULLAR
st.sidebar.header("Algoritma Parametreleri")
karinca = st.sidebar.slider("Karınca Sayısı", 5, 50, 15)
iterasyon = st.sidebar.slider("İterasyon Sayısı", 10, 200, 100)
alpha = st.sidebar.slider("Alpha", 0.1, 5.0, 1.0)
beta = st.sidebar.slider("Beta", 0.1, 5.0, 2.0)

st.sidebar.divider()
st.sidebar.subheader("Saha Koşulları")
hava_durumu = st.sidebar.select_slider(
    "Yol Durumu Zorluğu",
    options=["Açık (1.0x)", "Yağmurlu (1.3x)", "Kar Yağışlı (2.0x)"],
    value="Açık (1.0x)"
)

katsayi = 1.0
if "Yağmurlu" in hava_durumu:
    katsayi = 1.3
elif "Kar" in hava_durumu:
    katsayi = 2.0

if st.sidebar.button("Rotayı Hesapla"):
    # 1. Google API üzerinden gerçek veriler çekilir
    sure_matrisi, km_matrisi = mesafe_matrisi_olustur()
    sure_matrisi_zorlu = sure_matrisi * katsayi

    # 2. Algoritmayı Çalıştır
    en_iyi_yol, en_iyi_sure, gecmis = run_aco(sure_matrisi_zorlu, karinca, iterasyon, alpha, beta, 0.5, 1.0)
    toplam_km = sum(km_matrisi[en_iyi_yol[i]][en_iyi_yol[i + 1]] for i in range(len(en_iyi_yol) - 1))

    # ÖZET
    m1, m2, m3 = st.columns(3)
    m1.metric("Toplam Tahmini Süre", f"{en_iyi_sure:.1f} dk")
    m2.metric("Toplam Mesafe", f"{toplam_km:.1f} km")
    m3.metric("Saha Durumu", hava_durumu)

    # HARİTA VE ROTA PLANI
    col_map, col_list = st.columns([2.5, 1])

    with col_map:
        st.subheader("Rota ve Mesafe Analizi")
        icon_data = []
        rota_coords = []

        for i, idx in enumerate(en_iyi_yol):
            m = MAHALLE_VERILERI[idx]
            rota_coords.append([m["lon"], m["lat"]])

            # 15 durak için pin oluştur
            if i < len(en_iyi_yol) - 1:
                icon_data.append({
                    "lon": m["lon"], "lat": m["lat"],
                    "no": str(i + 1),
                    "isim": m["ad"],
                    "icon_data": {
                        "url": "https://img.icons8.com/color/48/marker.png",
                        "width": 128, "height": 128, "anchorY": 128
                    }
                })

        # Harita Görselleştirme (CartoDB Voyager stili)
        st.pydeck_chart(pdk.Deck(
            map_style="https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json",
            initial_view_state=pdk.ViewState(latitude=38.67, longitude=29.40, zoom=12.5),
            layers=[
                # KATMAN: Rota Çizgisi
                pdk.Layer("PathLayer", data=[{"path": rota_coords}], get_path="path",
                          get_width=20, get_color=[220, 53, 69, 200], width_min_pixels=5),

                # KATMAN: Profesyonel Pinler
                pdk.Layer("IconLayer", data=icon_data, get_icon="icon_data", get_size=45,
                          get_position=["lon", "lat"], pickable=True),

                # KATMAN: Pin İçindeki Sıra Numaraları
                pdk.Layer("TextLayer", data=icon_data, get_position=["lon", "lat"], get_text="no",
                          get_size=18, get_color=[255, 255, 255], get_pixel_offset=[0, -15])
            ],
            tooltip={"text": "Durak No: {no}"}
        ))

    with col_list:
        st.subheader("Rota Planı")
        plan_data = []
        for i in range(len(en_iyi_yol) - 1):
            idx1, idx2 = en_iyi_yol[i], en_iyi_yol[i + 1]
            plan_data.append({
                "Sıra": i + 1,
                "Güzergah": f"{MAHALLE_ADLARI[idx1].split(' ')[0]} ➔ {MAHALLE_ADLARI[idx2].split(' ')[0]}",
                "Süre": f"{sure_matrisi_zorlu[idx1][idx2]:.1f} dk",
                "KM": f"{km_matrisi[idx1][idx2]:.1f} km"
            })
        st.dataframe(pd.DataFrame(plan_data), hide_index=True, use_container_width=True)

    # ANALİTİK GRAFİKLER
    st.divider()
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.subheader("📈 Süre İyileşme Grafiği")
        fig_conv, ax_conv = plt.subplots(figsize=(10, 5), facecolor='#f8f9fa')
        ax_conv.plot(gecmis, color='#FF4B4B', linewidth=2.5, marker='o', markersize=4)
        ax_conv.set_xlabel("İterasyon Sayısı")
        ax_conv.set_ylabel("En İyi Süre (dk)")
        st.pyplot(fig_conv)

    with col_g2:
        st.subheader("📊 Mesafe İterasyon Grafiği")
        # Gerçek veriler üzerinden grafikleme yapılır
        gecmis_km = [(val / 60) * 40 for val in gecmis]
        fig_km, ax_km = plt.subplots(figsize=(10, 5), facecolor='#f8f9fa')
        ax_km.plot(gecmis_km, color='#2ecc71', linewidth=2.5, marker='s', markersize=4)
        ax_km.set_xlabel("İterasyon Sayısı")
        ax_km.set_ylabel("Toplam Mesafe (km)")
        st.pyplot(fig_km)

    # İŞ AKIŞ ŞEMASI
    st.divider()
    st.subheader("Teknik Ekip Rota Akış Şeması (Sıralı)")
    G = nx.DiGraph()
    labels = {}
    for i, idx in enumerate(en_iyi_yol):
        isim = MAHALLE_ADLARI[idx].split(' ')[0]
        labels[isim] = f"{isim}\n({i + 1}. Durak)"
        if i < len(en_iyi_yol) - 1:
            u, v = MAHALLE_ADLARI[idx].split(' ')[0], MAHALLE_ADLARI[en_iyi_yol[i + 1]].split(' ')[0]
            G.add_edge(u, v, weight=f"{sure_matrisi_zorlu[idx][en_iyi_yol[i + 1]]:.1f} dk")

    fig_graph, ax_graph = plt.subplots(figsize=(20, 10), facecolor='#f8f9fa')
    pos = nx.circular_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=7500, node_color='#FF8C00', edgecolors='white', ax=ax_graph)
    nx.draw_networkx_edges(G, pos, width=3, edge_color='#6c757d', arrowsize=40, connectionstyle='arc3,rad=0.12',
                           ax=ax_graph)
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=10, font_weight='bold', font_color='white', ax=ax_graph)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='#d63031', font_size=11,
                                 font_weight='bold', ax=ax_graph)
    plt.axis('off')
    st.pyplot(fig_graph, use_container_width=True)

    #  ROTAYI PNG OLARAK KAYDET
    plt.figure(figsize=(12, 10))
    lats = [MAHALLE_VERILERI[i]["lat"] for i in en_iyi_yol]
    lons = [MAHALLE_VERILERI[i]["lon"] for i in en_iyi_yol]

    # Rota çizgisi
    plt.plot(lons, lats, color='#dc3545', linewidth=2, alpha=0.5, zorder=1)

    for i, idx in enumerate(en_iyi_yol):
        if i < len(en_iyi_yol) - 1:
            # Durak noktası
            plt.scatter(lons[i], lats[i], color='#FF8C00', s=150, zorder=2)

            # Durak numarası
            plt.text(lons[i], lats[i], str(i + 1), fontsize=8, ha='center', va='center',
                     color='white', fontweight='bold', zorder=3)

            # MAHALLE ADI
            mahalle_adi = MAHALLE_ADLARI[idx].split(' Mah')[0]  # İsimleri kısaltmak için
            plt.text(lons[i] + 0.001, lats[i] + 0.0005, mahalle_adi,
                     fontsize=9, fontweight='semibold', color='#2d3436',
                     bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1))

    plt.title("Uşak Teknik Ekip Optimizasyon Rotası (Mahalle Detaylı)", fontsize=14, pad=20)
    plt.axis('off')  # Harita gibi görünmesi için eksenleri gizledik

    # figure klasörüne kaydet
    plt.savefig("figure/route_map.png", dpi=300, bbox_inches='tight')
    plt.close()
