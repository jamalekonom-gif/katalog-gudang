import streamlit as st
import pandas as pd
from datetime import datetime
import os
import urllib.parse
import time

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

# 3. SETTING CLOUDINARY
CLOUD_NAME = "dj4xyen1s"
BASE_URL_SMALL = f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/f_auto,q_auto,w_200,h_200,c_pad,b_white/"
BASE_URL_LARGE = f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/f_auto,q_auto/"

# 4. CSS (Tampilan Bersih & Modern)
st.markdown("""<style>
    #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}
    .stDeployButton {display:none;} [data-testid="stSidebar"] {display: none;}
    .product-card { background-color: white; padding: 12px; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.05); margin-bottom: 10px; border-left: 5px solid #007bff; }
    .img-container { width: 85px; height: 85px; overflow: hidden; border-radius: 8px; border: 1px solid #eee; display: flex; align-items: center; justify-content: center; background-color: white; flex-shrink: 0; }
    .img-container img { max-width: 100%; max-height: 100%; object-fit: contain; }
    .mandarin-text { color: #d35400; font-weight: bold; background-color: #fff5eb; padding: 2px 6px; border-radius: 4px; font-size: 0.85em; }
    .kode-badge { background-color: #34495e; color: white; padding: 1px 8px; border-radius: 4px; font-family: monospace; font-size: 0.8em; }
    .section-title { color: #2c3e50; font-weight: bold; font-size: 1.1rem; margin-bottom: 10px; }
    </style>""", unsafe_allow_html=True)

# 5. FUNGSI SAPAAN WAKTU
def dapatkan_sapaan():
    jam = datetime.now().hour
    if 5 <= jam < 11: return "🌅 Selamat Pagi"
    elif 11 <= jam < 15: return "☀️ Selamat Siang"
    elif 15 <= jam < 18: return "🌇 Selamat Sore"
    else: return "🌙 Selamat Malam"

# 6. LOGIKA LOGIN
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.write("#")
        st.title("🔒 Akses Gudang")
        nik_input = st.text_input("Masukkan NIK Anda:", type="password")
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
    with c_nama: 
        sapaan = dapatkan_sapaan()
        st.markdown(f"### {sapaan}, **{st.session_state.nama_user}**!")
    with c_logout: 
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    st.divider()

    # --- LAYOUT UTAMA ---
    col_kiri, col_kanan = st.columns([1.3, 2.7], gap="medium")

    # KOLOM KIRI: CBOX
    with col_kiri:
        st.markdown('<p class="section-title">💬 Obrolan Grup</p>', unsafe_allow_html=True)
        is_admin = st.session_state.nik_user == "84200082"
        nama_fix = f"ADMIN-{st.session_state.nama_user}" if is_admin else st.session_state.nama_user
        nama_enc = urllib.parse.quote(nama_fix)
        link_cbox = f"https://www3.cbox.ws/box/?boxid=3554511&boxtag=eFn5Pq&nme={nama_enc}&nmefixed=1&nmelock=1"
        st.components.v1.iframe(link_cbox, height=500, scrolling=True)
        if is_admin:
            st.link_button("🗑️ MODERASI CHAT (HAPUS)", "https://www3.cbox.ws/box/?boxid=3554511&boxtag=eFn5Pq&sec=mod", use_container_width=True)

    # KOLOM KANAN: KATALOG
    with col_kanan:
        st.markdown('<p class="section-title">🔍 Cari Material</p>', unsafe_allow_html=True)
        NAMA_FILE = "Data_barang.csv" if os.path.exists("Data_barang.csv") else "data_barang.csv"
        
        @st.cache_data
        def load_data(file):
            for enc in ['utf-8-sig', 'gb18030', 'cp1252']:
                try:
                    df = pd.read_csv(file, encoding=enc).fillna('')
                    df.columns = df.columns.str.strip()
                    return df
                except: continue
            return pd.DataFrame()

        if os.path.exists(NAMA_FILE):
            df = load_data(NAMA_FILE)
            st.caption(f"✅ Sistem Aktif. Terbaca {len(df)} material.")
            search = st.text_input("", placeholder="Ketik nama atau kode material...")

            if search:
                with st.spinner('Mencari di gudang...'):
                    hasil = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
                
                if not hasil.empty:
                    st.write(f"Menampilkan {len(hasil)} hasil:")
                    for i, row in hasil.iterrows():
                        st.markdown('<div class="product-card">', unsafe_allow_html=True)
                        c_foto, c_teks, c_zoom = st.columns([1, 3.2, 0.8])
                        
                        # --- LOGIKA FOTO FLEKSIBEL ---
                        foto_raw = str(row.get('Foto', '')).strip()
                        
                        # Cek apakah sudah ada ekstensinya di CSV
                        has_extension = any(foto_raw.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp'])
                        
                        if foto_raw == "" or foto_raw.lower() == "nan":
                            url_small = "https://via.placeholder.com/150?text=No+Image"
                            url_large = "https://via.placeholder.com/600?text=No+Image"
                        else:
                            # Jika tidak ada ekstensi, default kita tambahkan .jpg (Cloudinary akan handle otomatis)
                            # Tapi jika sudah ada ekstensi (.png/.jpeg), biarkan saja apa adanya
                            foto_final = foto_raw if has_extension else f"{foto_raw}.jpg"
                            url_small = f"{BASE_URL_SMALL}{foto_final}"
                            url_large = f"{BASE_URL_LARGE}{foto_final}"
                        
                        with c_foto: 
                            st.markdown(f'<div class="img-container"><img src="{url_small}"></div>', unsafe_allow_html=True)
                        
                        with c_teks:
                            st.markdown(f"**{row.get('Nama_Indo', '-')}**")
                            if row.get('Nama_Mandarin'): 
                                st.markdown(f"<span class='mandarin-text'>{row.get('Nama_Mandarin')}</span>", unsafe_allow_html=True)
                            st.write(f"Kode: <span class='kode-badge'>{row.get('Kode', '-')}</span>", unsafe_allow_html=True)
                        
                        with c_zoom:
                            with st.expander("🔍 Zoom"): 
                                st.image(url_large, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.warning("Data tidak ditemukan.")