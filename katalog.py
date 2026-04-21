import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Warehouse Digital Catalog", page_icon="📦", layout="wide")

# 2. DATA KARYAWAN
DATA_KARYAWAN = {"84200082": "JAMALUDDIN", "84200061": "ENNI ROSDAENI", "85400228": "PUTRI", "84300997": "MUH. TAWAKKAL", "84102172": "WAHYU DWI SETYAN", "80519113": "UMI KHOLIFA"}

# 3. DATABASE MEMORI
if "log_kunjungan" not in st.session_state: st.session_state.log_kunjungan = []
if "kotak_saran" not in st.session_state: st.session_state.kotak_saran = []

# 4. SETTING CLOUDINARY
CLOUD_NAME = "dj4xyen1s"
BASE_URL = f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/f_auto,q_auto,w_150,h_150,c_pad,b_white/"

# 5. CSS (UKURAN 75PX)
st.markdown("""<style>
    #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}
    .product-card { background-color: white; padding: 10px; border-radius: 8px; box-shadow: 0 1px 4px rgba(0,0,0,0.05); margin-bottom: 8px; border-left: 4px solid #007bff; }
    .img-box { width: 75px; height: 75px; overflow: hidden; border-radius: 6px; border: 1px solid #f0f0f0; display: flex; align-items: center; justify-content: center; background-color: white; flex-shrink: 0; }
    .img-box img { max-width: 100%; max-height: 100%; object-fit: contain; }
    .mandarin-text { color: #e67e22; font-weight: bold; background-color: #fff5eb; padding: 0px 5px; border-radius: 3px; font-size: 0.8em; }
    .kode-badge { background-color: #34495e; color: white; padding: 0px 5px; border-radius: 3px; font-family: monospace; font-size: 0.75em; }
    </style>""", unsafe_allow_html=True)

# 6. LOGIKA LOGIN
if "logged_in" not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.title("🔒 Akses Gudang")
        nik_input = st.text_input("NIK Karyawan:", type="password")
        if st.button("Masuk", use_container_width=True):
            if nik_input in DATA_KARYAWAN:
                st.session_state.logged_in, st.session_state.nama_user, st.session_state.nik_user = True, DATA_KARYAWAN[nik_input], nik_input
                st.session_state.log_kunjungan.append({"Waktu": datetime.now().strftime("%d/%m/%Y %H:%M"), "Nama": st.session_state.nama_user})
                st.rerun()
            else: st.error("⚠️ NIK Salah")
else:
    # --- HEADER ---
    st.markdown(f"### 📦 Digital Catalog - {st.session_state.nama_user}")
    if st.button("Logout"): 
        st.session_state.logged_in = False
        st.rerun()

    # PANEL ADMIN
    if st.session_state.nik_user == "84200082":
        with st.expander("📊 PANEL ADMIN"):
            t1, t2 = st.tabs(["👥 Login", "📩 Saran"])
            if st.session_state.log_kunjungan: with t1: st.table(pd.DataFrame(st.session_state.log_kunjungan))
            if st.session_state.kotak_saran: with t2: st.table(pd.DataFrame(st.session_state.kotak_saran))

    st.divider()

    # --- BAGIAN PENCARIAN ---
    # Nama file disesuaikan dengan gambar Bapak (D-nya besar)
    NAMA_FILE = "Data_barang.csv" 
    
    if not os.path.exists(NAMA_FILE):
        # Jika tidak ada D besar, coba cari d kecil
        if os.path.exists("data_barang.csv"):
            NAMA_FILE = "data_barang.csv"
        else:
            st.error(f"❌ File '{NAMA_FILE}' tidak ditemukan di GitHub Bapak!")
            st.info("Pastikan nama file di GitHub sudah benar.")
            st.stop()

    # Muat Data
    df = pd.read_csv(NAMA_FILE, encoding='utf-8-sig').fillna('')
    st.caption(f"✅ Sistem siap. Berhasil memuat {len(df)} data material.")
    
    search = st.text_input("🔍 Cari Material (Nama/Kode):", placeholder="Ketik di sini...")
    
    if search:
        # Cari di semua kolom (Nama_Indo, Kode, dll)
        hasil = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
        
        if not hasil.empty:
            for i, row in hasil.iterrows():
                # Bersihkan nama foto
                foto_id = str(row.get('Foto', '')).strip()
                if foto_id and not foto_id.lower().endswith(('.jpg', '.png')):
                    foto_id = f"{foto_id}.jpg"
                
                st.markdown(f'''
                <div class="product-card">
                    <div style="display: flex; gap: 12px; align-items: center;">
                        <div class="img-box">
                            <img src="{BASE_URL}{foto_id}">
                        </div>
                        <div style="flex: 1;">
                            <h5 style="margin: 0; color: #2c3e50;">{row.get('Nama_Indo')}</h5>
                            <div style="margin-top: 3px;">
                                <span class="mandarin-text">{row.get('Nama_Mandarin')}</span>
                                <span class="kode-badge">Kode: {row.get('Kode')}</span>
                            </div>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.warning(f"Material '{search}' tidak ditemukan.")