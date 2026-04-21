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

# 3. DATABASE MEMORI (Hanya untuk Log Login)
if "log_kunjungan" not in st.session_state:
    st.session_state.log_kunjungan = []

# 4. SETTING CLOUDINARY
CLOUD_NAME = "dj4xyen1s"
BASE_URL = f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/f_auto,q_auto,w_200,h_200,c_pad,b_white/"

# 5. CSS - BERSIH & PROFESIONAL
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}
    .stDeployButton {display:none;} [data-testid="stSidebar"] {display: none;}
    
    /* Kartu Produk */
    .product-card { 
        background-color: white; padding: 12px; border-radius: 10px; 
        box-shadow: 0 2px 6px rgba(0,0,0,0.05); margin-bottom: 10px; 
        border-left: 5px solid #007bff;
    }
    
    /* Ukuran Gambar 85px */
    .img-container {
        width: 85px; height: 85px; overflow: hidden; border-radius: 8px;
        border: 1px solid #eee; display: flex; align-items: center;
        justify-content: center; background-color: white; flex-shrink: 0;
    }
    .img-container img { max-width: 100%; max-height: 100%; object-fit: contain; }

    .mandarin-text { color: #d35400; font-weight: bold; background-color: #fff5eb; padding: 2px 6px; border-radius: 4px; font-size: 0.85em; }
    .kode-badge { background-color: #34495e; color: white; padding: 1px 8px; border-radius: 4px; font-family: monospace; font-size: 0.8em; }
    .section-title { color: #2c3e50; font-weight: bold; font-size: 1.1rem; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 6. LOGIKA LOGIN
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.write("#")
        st.image("https://cdn-icons-png.flaticon.com/512/408/408710.png", width=80)
        st.title("🔒 Akses Gudang")
        nik_input = st.text_input("NIK Karyawan:", type="password")
        if st.button("Masuk Ke Sistem", use_container_width=True):
            if nik_input in DATA_KARYAWAN:
                st.session_state.logged_in = True
                st.session_state.nama_user = DATA_KARYAWAN[nik_input]
                st.session_state.nik_user = nik_input
                st.session_state.log_kunjungan.append({
                    "Waktu": datetime.now().strftime("%d/%m/%Y %H:%M"), 
                    "Nama": st.session_state.nama_user
                })
                st.rerun()
            else:
                st.error("⚠️ NIK Tidak Terdaftar")
else:
    # --- HEADER ---
    c_nama, c_logout = st.columns([4, 1])
    with c_nama:
        st.markdown(f"### 📦 Digital Warehouse - {st.session_state.nama_user}")
    with c_logout:
        if st.button("Keluar", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    # --- MENU ADMIN (Hanya Riwayat Login) ---
    if st.session_state.nik_user == "84200082":
        with st.expander("📊 PANEL ADMIN (RIWAYAT LOGIN)"):
            if st.session_state.log_kunjungan:
                st.table(pd.DataFrame(st.session_state.log_kunjungan))
            else:
                st.write("Belum ada data.")

    st.divider()

    # --- LAYOUT UTAMA ---
    col_kiri, col_kanan = st.columns([1.2, 2.8], gap="medium")

    # KOLOM KIRI: CBOX
    with col_kiri:
        st.markdown('<p class="section-title">💬 Obrolan Grup</p>', unsafe_allow_html=True)
        st.components.v1.iframe("https://www3.cbox.ws/box/?boxid=3554511&boxtag=eFn5Pq", height=550, scrolling=True)

    # KOLOM KANAN: KATALOG
    with col_kanan:
        st.markdown('<p class="section-title">🔍 Cari Material</p>', unsafe_allow_html=True)
        
        @st.cache_data
        def load_data():
            # Mencoba membaca file dengan berbagai encoding agar karakter mandarin aman
            for enc in ['utf-8-sig', 'gb18030', 'cp1252']:
                try:
                    df = pd.read_csv("Data_barang.csv", encoding=enc).fillna('')
                    return df
                except: continue
            return pd.DataFrame()

        df = load_data()
        
        # Pesan status data
        if not df.empty:
            st.caption(f"✅ Sistem Aktif. Total {len(df)} material siap dicari.")
        
        search = st.text_input("", placeholder="Ketik nama barang atau kode...")

        if search and not df.empty:
            # Pencarian di semua kolom
            hasil = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
            
            if not hasil.empty:
                for i, row in hasil.iterrows():
                    st.markdown('<div class="product-card">', unsafe_allow_html=True)
                    c_foto, c_teks = st.columns([1, 4])
                    
                    with c_foto:
                        foto = str(row.get('Foto', '')).strip()
                        # Jika di CSV belum ada .jpg, kita tambahkan otomatis
                        if foto and not foto.lower().endswith(('.jpg', '.png')):
                            foto = f"{foto}.jpg"
                        
                        url = f"{BASE_URL}{foto}" if foto else "https://via.placeholder.com/150"
                        st.markdown(f'''
                            <div class="img-container">
                                <img src="{url}">
                            </div>
                        ''', unsafe_allow_html=True)
                    
                    with c_teks:
                        # Mengambil data berdasarkan nama kolom di CSV Bapak
                        nama_indo = row.get('Nama_Indo', '-')
                        nama_mand = row.get('Nama_Mandarin', '')
                        kode_mat = row.get('Kode', '-')
                        
                        st.markdown(f"**{nama_indo}**")
                        if nama_mand:
                            st.markdown(f"<span class='mandarin-text'>{nama_mand}</span>", unsafe_allow_html=True)
                        st.write(f"Kode: <span class='kode-badge'>{kode_mat}</span>", unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning(f"Material '{search}' tidak ditemukan.")