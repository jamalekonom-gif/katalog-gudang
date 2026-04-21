import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. KONFIGURASI
st.set_page_config(page_title="Warehouse Digital Catalog", page_icon="📦", layout="wide")

# 2. DATA KARYAWAN
DATA_KARYAWAN = {"84200082": "JAMALUDDIN", "84200061": "ENNI ROSDAENI", "85400228": "PUTRI", "84300997": "MUH. TAWAKKAL", "84102172": "WAHYU DWI SETYAN", "80519113": "UMI KHOLIFA"}

# 3. DATABASE MEMORI
if "log_kunjungan" not in st.session_state: st.session_state.log_kunjungan = []
if "kotak_saran" not in st.session_state: st.session_state.kotak_saran = []

# 4. CLOUDINARY
CLOUD_NAME = "dj4xyen1s"
BASE_URL = f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/f_auto,q_auto,w_150,h_150,c_pad,b_white/"

# 5. CSS
st.markdown("""<style>
    #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}
    .product-card { background-color: white; padding: 10px; border-radius: 8px; box-shadow: 0 1px 4px rgba(0,0,0,0.05); margin-bottom: 8px; border-left: 4px solid #007bff; }
    .img-box { width: 75px; height: 75px; overflow: hidden; border-radius: 6px; border: 1px solid #f0f0f0; display: flex; align-items: center; justify-content: center; background-color: white; flex-shrink: 0; }
    .img-box img { max-width: 100%; max-height: 100%; object-fit: contain; }
    </style>""", unsafe_allow_html=True)

# 6. LOGIN
if "logged_in" not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    nik_input = st.text_input("NIK Karyawan:", type="password")
    if st.button("Masuk"):
        if nik_input in DATA_KARYAWAN:
            st.session_state.logged_in, st.session_state.nama_user, st.session_state.nik_user = True, DATA_KARYAWAN[nik_input], nik_input
            st.rerun()
else:
    st.markdown(f"### 📦 Catalog - {st.session_state.nama_user}")
    
    # MUAT DATA
    NAMA_FILE = "Data_barang.csv" if os.path.exists("Data_barang.csv") else "data_barang.csv"
    
    if os.path.exists(NAMA_FILE):
        df = pd.read_csv(NAMA_FILE, encoding='utf-8-sig').fillna('')
        st.caption(f"✅ Berhasil memuat {len(df)} data.")
        
        search = st.text_input("🔍 Ketik Nama Barang atau Kode:")
        
        if search:
            # KODE PINTAR: Cari di semua kolom tanpa peduli nama kolomnya
            hasil = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
            
            if not hasil.empty:
                for i, row in hasil.iterrows():
                    # Ambil data berdasarkan urutan kolom (Kolom 1=Nama, Kolom 2=Mandarin, Kolom 3=Kode, Kolom 4=Foto)
                    # Ini lebih aman jika judul kolom Bapak berbeda
                    v_nama = row.iloc[0] if len(row) > 0 else "N/A"
                    v_mand = row.iloc[1] if len(row) > 1 else ""
                    v_kode = row.iloc[2] if len(row) > 2 else ""
                    v_foto = str(row.iloc[3]).strip() if len(row) > 3 else ""
                    
                    if v_foto and not v_foto.lower().endswith(('.jpg', '.png')):
                        v_foto = f"{v_foto}.jpg"
                    
                    st.markdown(f'''
                    <div class="product-card">
                        <div style="display: flex; gap: 12px; align-items: center;">
                            <div class="img-box"><img src="{BASE_URL}{v_foto}"></div>
                            <div style="flex: 1;">
                                <h5 style="margin: 0;">{v_nama}</h5>
                                <div style="color: #e67e22; font-size: 0.8em;">{v_mand}</div>
                                <div style="background: #34495e; color: white; display: inline-block; padding: 0 5px; border-radius: 3px; font-size: 0.7em;">{v_kode}</div>
                            </div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
            else:
                st.warning(f"Data '{search}' tidak ditemukan.")
    else:
        st.error("File CSV tidak ditemukan!")