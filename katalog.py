import streamlit as st
import pandas as pd
from datetime import datetime

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Warehouse Digital Catalog", page_icon="📦", layout="wide")

# 2. DATA KARYAWAN
DATA_KARYAWAN = {
    "84200082": "JAMALUDDIN",
    "84200061": "ENNI ROSDAENI",
    "85400228": "PUTRI",
    "84300997": "MUH. TAWAKKAL",
    "84102172": "WAHYU DWI SETYAN",
    "80519113": "UMI KHOLIFA"
}

# 3. SETTING NOMOR WA & CLOUDINARY
NOMOR_WA_BAPAK = "6285222452777" # <-- GANTI DENGAN NOMOR WA BAPAK (awali 62)
CLOUD_NAME = "dj4xyen1s"
BASE_URL = f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/f_auto,q_auto/"

# 4. CSS (Hapus Sidebar agar tidak bingung)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}
    .stDeployButton {display:none;} [data-testid="stSidebar"] {display: none;}
    .stImage img { max-height: 250px; width: auto; border-radius: 10px; object-fit: contain; }
    .product-card { background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 25px; border-top: 4px solid #25D366; }
    </style>
    """, unsafe_allow_html=True)

# 5. LOGIN
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("#")
        st.image("https://cdn-icons-png.flaticon.com/512/408/408710.png", width=100)
        st.title("🔒 Akses Gudang")
        nik_input = st.text_input("NIK Karyawan:", type="password")
        if st.button("Masuk", use_container_width=True):
            if nik_input in DATA_KARYAWAN:
                st.session_state.logged_in = True
                st.session_state.nama_user = DATA_KARYAWAN[nik_input]
                st.session_state.nik_user = nik_input
                st.rerun()
            else: st.error("NIK Tidak Terdaftar")
else:
    # --- TAMPILAN SETELAH LOGIN ---
    c_nama, c_logout = st.columns([4, 1])
    with c_nama:
        st.info(f"👤 **{st.session_state.nama_user}**")
    with c_logout:
        if st.button("Keluar"):
            st.session_state.logged_in = False
            st.rerun()

    st.title("📦 Katalog Digital")
    
    # LOAD DATA
    def load_data():
        for enc in ['utf-8-sig', 'gb18030', 'cp1252']:
            try: return pd.read_csv("data_barang.csv", encoding=enc).fillna('')
            except: continue
        return pd.DataFrame()

    df = load_data()
    search = st.text_input("", placeholder="🔍 Cari Nama Barang...")
    
    if search:
        hasil = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
        for i, row in hasil.iterrows():
            with st.container():
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                cf, ct = st.columns([1, 2.5])
                with cf:
                    foto = str(row.get('Foto', '')).strip()
                    st.image(f"{BASE_URL}{foto}.jpg" if foto else "https://via.placeholder.com/300", use_container_width=True)
                with ct:
                    st.markdown(f"### {row.get('Nama_Indo')}")
                    st.write(f"**Kode:** {row.get('Kode')}")
                    
                    # TOMBOL WHATSAPP
                    msg = f"Halo Pak Jamaluddin, saya {st.session_state.nama_user} ingin bertanya stok: {row.get('Nama_Indo')}"
                    link_wa = f"https://wa.me/{NOMOR_WA_BAPAK}?text={msg.replace(' ', '%20')}"
                    st.markdown(f'[📲 Tanya Stok via WA]({link_wa})')
                st.markdown('</div>', unsafe_allow_html=True)