import streamlit as st
import pandas as pd
from datetime import datetime

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Warehouse Digital Catalog", page_icon="📦", layout="wide")

# 2. DATA UTAMA
NOMOR_WA_BAPAK = "6285222452777" # <-- Ganti dengan nomor WA Bapak (awali 62)
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
BASE_URL = f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/f_auto,q_auto/"

# 4. CSS UNTUK PERBAIKAN GAMBAR & LAYOUT
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}
    .stDeployButton {display:none;} [data-testid="stSidebar"] {display: none;}
    
    /* Memaksa Gambar Tetap Kecil */
    .img-box img {
        width: 150px !important; /* Ukuran lebar tetap */
        height: 150px !important; /* Ukuran tinggi tetap */
        object-fit: cover; /* Gambar dipotong rapi agar kotak */
        border-radius: 10px;
        border: 1px solid #ddd;
    }
    
    .product-card { 
        background-color: white; padding: 15px; border-radius: 12px; 
        box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 10px; 
        border-left: 5px solid #28a745;
    }
    
    .mandarin-text { color: #e67e22; font-weight: bold; font-size: 0.9em; }
    .kode-badge { background-color: #34495e; color: white; padding: 2px 6px; border-radius: 4px; font-size: 0.8em; }
    </style>
    """, unsafe_allow_html=True)

# 5. LOGIN
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.write("#")
        st.title("🔒 Login Gudang")
        nik_input = st.text_input("Masukkan NIK:", type="password")
        if st.button("Masuk", use_container_width=True):
            if nik_input in DATA_KARYAWAN:
                st.session_state.logged_in = True
                st.session_state.nama_user = DATA_KARYAWAN[nik_input]
                st.session_state.nik_user = nik_input
                st.rerun()
            else: st.error("NIK Salah")
else:
    # --- HEADER ---
    c1, c2 = st.columns([4, 1])
    with c1:
        st.markdown(f"### 📦 Catalog & Chat")
        st.write(f"Halo, **{st.session_state.nama_user}**")
    with c2:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    st.divider()

    # --- LAYOUT DASHBOARD ---
    col_kiri, col_kanan = st.columns([1.2, 2.8], gap="medium")

    with col_kiri:
        st.markdown("**💬 Obrolan Grup**")
        link_cbox = "https://www3.cbox.ws/box/?boxid=3554511&boxtag=eFn5Pq"
        st.components.v1.iframe(link_cbox, height=500, scrolling=True)
        
        # Saran Umum via WhatsApp
        if st.session_state.nik_user != "84200082":
            st.write("#")
            su = st.text_area("Kirim Kritik/Saran Umum ke Pak Jamal:")
            if st.button("Kirim via WhatsApp"):
                if su:
                    msg = f"Halo Pak Jamal, saya {st.session_state.nama_user} ingin memberi saran umum: {su}"
                    st.markdown(f'<a href="https://wa.me/{NOMOR_WA_BAPAK}?text={msg}" target="_blank">Klik di sini untuk kirim ke WA</a>', unsafe_allow_html=True)

    with col_kanan:
        st.markdown("**🔍 Cari Material**")
        search = st.text_input("", placeholder="Ketik nama/kode...")
        
        df = pd.read_csv("data_barang.csv").fillna('')
        
        if search:
            hasil = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
            for i, row in hasil.iterrows():
                with st.container():
                    st.markdown('<div class="product-card">', unsafe_allow_html=True)
                    f1, f2 = st.columns([1, 3])
                    with f1:
                        foto = str(row.get('Foto', '')).strip()
                        url = f"{BASE_URL}{foto}.jpg" if foto else "https://via.placeholder.com/150"
                        st.markdown(f'<div class="img-box"><img src="{url}"></div>', unsafe_allow_html=True)
                    with f2:
                        st.markdown(f"**{row.get('Nama_Indo')}**")
                        st.markdown(f"<span class='mandarin-text'>{row.get('Nama_Mandarin')}</span>", unsafe_allow_html=True)
                        st.markdown(f"Kode: <span class='kode-badge'>{row.get('Kode')}</span>", unsafe_allow_html=True)
                        
                        # TOMBOL LAPOR VIA WA (PASTI MASUK)
                        if st.session_state.nik_user != "84200082":
                            nama_m = row.get('Nama_Indo')
                            kode_m = row.get('Kode')
                            teks_wa = f"Halo Pak Jamal, saya {st.session_state.nama_user}. Ada saran untuk barang {nama_m} ({kode_m}): "
                            link_wa = f"https://wa.me/{NOMOR_WA_BAPAK}?text={teks_wa.replace(' ', '%20')}"
                            st.markdown(f'<a href="{link_wa}" target="_blank" style="color: #28a745; font-size: 0.8em; font-weight: bold;">📝 Kirim Saran Barang via WA</a>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)