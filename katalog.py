import streamlit as st
import pandas as pd
from datetime import datetime
import os
import urllib.parse

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Warehouse Digital Catalog", page_icon="📦", layout="wide")

# 2. DATA KARYAWAN RESMI
DATA_KARYAWAN = {
    "84200082": "JAMALUDDIN",
    "84200061": "ENNI ROSDAENI",
    "85400228": "PUTRI",
    "84300997": "MUH. TAWAKKAL",
    "84102172": "WAHYU DWI SETYAN",
    "80519113": "UMI KHOLIFA"
}

# 3. SETTING CLOUDINARY (Optimasi Gambar)
CLOUD_NAME = "dj4xyen1s"
# Menggunakan f_auto dan q_auto agar Cloudinary otomatis memilih format terbaik (JPG/PNG)
BASE_URL = f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/f_auto,q_auto/"

# 4. CSS
st.markdown("""<style>
    #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}
    .stDeployButton {display:none;} [data-testid="stSidebar"] {display: none;}
    .product-card { background-color: white; padding: 12px; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.05); margin-bottom: 10px; border-left: 5px solid #007bff; }
    .img-container { width: 85px; height: 85px; overflow: hidden; border-radius: 8px; border: 1px solid #eee; display: flex; align-items: center; justify-content: center; background-color: white; flex-shrink: 0; }
    .img-container img { max-width: 100%; max-height: 100%; object-fit: contain; }
    .mandarin-text { color: #d35400; font-weight: bold; background-color: #fff5eb; padding: 2px 6px; border-radius: 4px; font-size: 0.85em; }
    .kode-badge { background-color: #34495e; color: white; padding: 1px 8px; border-radius: 4px; font-family: monospace; font-size: 0.8em; }
    </style>""", unsafe_allow_html=True)

# 5. LOGIKA LOGIN
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.write("#")
        st.title("🔒 Akses Gudang")
        nik_input = st.text_input("NIK Karyawan:", type="password")
        if st.button("Masuk Ke Sistem", use_container_width=True):
            if nik_input in DATA_KARYAWAN:
                st.session_state.logged_in = True
                st.session_state.nama_user = DATA_KARYAWAN[nik_input]
                st.session_state.nik_user = nik_input
                st.rerun()
            else: st.error("⚠️ NIK Tidak Terdaftar")
else:
    # --- HEADER ---
    c_nama, c_logout = st.columns([4, 1])
    with c_nama: st.markdown(f"### 📦 Digital Warehouse - {st.session_state.nama_user}")
    with c_logout: 
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    st.divider()

    # --- LAYOUT UTAMA ---
    col_kiri, col_kanan = st.columns([1.3, 2.7], gap="medium")

    with col_kiri:
        st.markdown('**💬 Obrolan Grup**')
        is_admin = st.session_state.nik_user == "84200082"
        nama_fix = f"ADMIN-{st.session_state.nama_user}" if is_admin else st.session_state.nama_user
        nama_enc = urllib.parse.quote(nama_fix)
        link_cbox = f"https://www3.cbox.ws/box/?boxid=3554511&boxtag=eFn5Pq&nme={nama_enc}&nmefixed=1&nmelock=1"
        st.components.v1.iframe(link_cbox, height=500, scrolling=True)

    with col_kanan:
        st.markdown('**🔍 Cari Material**')
        NAMA_FILE = "Data_barang.csv" if os.path.exists("Data_barang.csv") else "data_barang.csv"
        
        # FUNGSI LOAD DATA DENGAN PEMBERSIH CACHE
        def load_data(file):
            for enc in ['utf-8-sig', 'gb18030', 'cp1252']:
                try:
                    df = pd.read_csv(file, encoding=enc).fillna('')
                    df.columns = df.columns.str.strip()
                    return df
                except: continue
            return pd.DataFrame()

        if os.path.exists(NAMA_FILE):
            # Kita panggil langsung tanpa @st.cache_data agar data baru selalu terbaca
            df = load_data(NAMA_FILE)
            
            # Tombol Refresh untuk Admin
            if is_admin:
                if st.button("🔄 Refresh Data Baru"):
                    st.cache_data.clear()
                    st.rerun()
            
            st.caption(f"✅ Menampilkan {len(df)} material.")
            search = st.text_input("", placeholder="Ketik nama atau kode...")

            if search:
                hasil = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
                if not hasil.empty:
                    for i, row in hasil.iterrows():
                        st.markdown('<div class="product-card">', unsafe_allow_html=True)
                        c_foto, c_teks, c_zoom = st.columns([1, 3.2, 0.8])
                        
                        foto_csv = str(row.get('Foto', '')).strip()
                        
                        if not foto_csv or foto_csv.lower() == 'nan':
                            url_img = "https://via.placeholder.com/150?text=No+Image"
                        else:
                            # Jika di CSV sudah ada ekstensi (.jpg/.png), biarkan saja. 
                            # Jika tidak ada, Cloudinary dengan f_auto akan mencoba mencarinya.
                            url_img = f"{BASE_URL}{foto_csv}"
                        
                        with c_foto: 
                            st.markdown(f'<div class="img-container"><img src="{url_img}"></div>', unsafe_allow_html=True)
                        with c_teks:
                            st.markdown(f"**{row.get('Nama_Indo', '-')}**")
                            if row.get('Nama_Mandarin'): st.markdown(f"<span class='mandarin-text'>{row.get('Nama_Mandarin')}</span>", unsafe_allow_html=True)
                            st.write(f"Kode: <span class='kode-badge'>{row.get('Kode', '-')}</span>", unsafe_allow_html=True)
                        with c_zoom:
                            with st.expander("🔍 Zoom"): st.image(url_img, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                else: st.warning("Barang tidak ditemukan.")