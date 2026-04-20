import streamlit as st
import pandas as pd
from datetime import datetime

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

# 3. DATABASE MEMORI
if "log_kunjungan" not in st.session_state:
    st.session_state.log_kunjungan = []
if "kotak_saran" not in st.session_state:
    st.session_state.kotak_saran = []

# 4. SETTING CLOUDINARY
CLOUD_NAME = "dj4xyen1s"
BASE_URL = f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/f_auto,q_auto/"

# 5. CSS UNTUK TAMPILAN DASHBOARD RAPI
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}
    .stDeployButton {display:none;} [data-testid="stSidebar"] {display: none;}
    
    /* Background Halaman */
    .main { background-color: #f8f9fa; }
    
    /* Atur Jarak Antar Elemen agar Rapat */
    [data-testid="stVerticalBlock"] { gap: 0.5rem; }
    
    /* Kotak Produk */
    .product-card { 
        background-color: white; padding: 15px; border-radius: 12px; 
        box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 15px; 
        border-left: 5px solid #007bff;
    }
    
    /* Nama Mandarin */
    .mandarin-text { 
        color: #e67e22; font-weight: bold; background-color: #fff5eb; 
        padding: 2px 8px; border-radius: 4px; display: inline-block; font-size: 0.9em;
    }
    
    /* Badge Kode Material */
    .kode-badge { 
        background-color: #34495e; color: white; padding: 2px 8px; 
        border-radius: 4px; font-family: monospace; font-size: 0.85em; display: inline-block;
    }

    /* Judul Kolom */
    .section-title {
        color: #2c3e50; font-weight: bold; font-size: 1.1rem; margin-bottom: -10px; margin-top: 10px;
    }

    /* Bingkai Foto agar tidak meluber */
    .img-container img {
        max-height: 180px; width: auto; border-radius: 8px; object-fit: contain;
    }
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
        if st.button("Masuk", use_container_width=True):
            if nik_input in DATA_KARYAWAN:
                st.session_state.logged_in = True
                st.session_state.nama_user = DATA_KARYAWAN[nik_input]
                st.session_state.nik_user = nik_input
                st.session_state.log_kunjungan.append({"Waktu": datetime.now().strftime("%d/%m/%Y %H:%M"), "Nama": st.session_state.nama_user})
                st.rerun()
            else: st.error("⚠️ NIK Salah")
else:
    # --- HEADER ---
    c1, c2 = st.columns([4, 1])
    with c1:
        st.markdown(f"### 📦 Digital Warehouse Catalog")
        st.caption(f"User: {st.session_state.nama_user}")
    with c2:
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    # MENU ADMIN
    if st.session_state.nik_user == "84200082":
        with st.expander("📊 PANEL ADMIN"):
            t1, t2 = st.tabs(["👥 Login", "📩 Saran"])
            with t1: st.table(pd.DataFrame(st.session_state.log_kunjungan))
            with t2: st.table(pd.DataFrame(st.session_state.kotak_saran))

    st.divider()

    # --- LAYOUT DUA KOLOM ---
    col_kiri, col_kanan = st.columns([1.1, 2.9], gap="medium")

    # KOLOM KIRI (CHAT & SARAN UMUM)
    with col_kiri:
        st.markdown('<p class="section-title">💬 Obrolan Grup</p>', unsafe_allow_html=True)
        link_cbox = "https://www3.cbox.ws/box/?boxid=3554511&boxtag=eFn5Pq"
        st.components.v1.iframe(link_cbox, height=500, scrolling=True)
        
        # SARAN UMUM (Muncul untuk karyawan)
        if st.session_state.nik_user != "84200082":
            st.write("#")
            with st.expander("📢 Kirim Saran Umum"):
                su = st.text_area("Tulis saran Anda...", key="su")
                if st.button("Kirim Saran"):
                    if su:
                        st.session_state.kotak_saran.append({"Waktu": datetime.now().strftime("%H:%M"), "Oleh": st.session_state.nama_user, "Konteks": "UMUM", "Pesan": su})
                        st.success("Terkirim!")

    # KOLOM KANAN (KATALOG)
    with col_kanan:
        st.markdown('<p class="section-title">🔍 Cari Material</p>', unsafe_allow_html=True)
        search = st.text_input("", placeholder="Ketik nama atau kode barang...")
        
        def load_data():
            for enc in ['utf-8-sig', 'gb18030', 'cp1252']:
                try:
                    df = pd.read_csv("data_barang.csv", encoding=enc).fillna('')
                    return df
                except: continue
            return pd.DataFrame()

        df = load_data()
        
        if search:
            hasil = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
            for i, row in hasil.iterrows():
                with st.container():
                    st.markdown('<div class="product-card">', unsafe_allow_html=True)
                    f1, f2 = st.columns([1, 2.5])
                    with f1:
                        # Foto dengan ukuran terkontrol
                        f = str(row.get('Foto', '')).strip()
                        url = f"{BASE_URL}{f}.jpg" if f else "https://via.placeholder.com/300"
                        st.markdown('<div class="img-container">', unsafe_allow_html=True)
                        st.image(url, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    with f2:
                        st.markdown(f"#### {row.get('Nama_Indo')}")
                        if row.get('Nama_Mandarin'):
                            st.markdown(f"<div class='mandarin-text'>{row.get('Nama_Mandarin')}</div>", unsafe_allow_html=True)
                        st.write(f"Kode: <span class='kode-badge'>{row.get('Kode')}</span>", unsafe_allow_html=True)
                        
                        if st.session_state.nik_user != "84200082":
                            with st.expander("📝 Saran Barang"):
                                sk = st.text_area("Masukan...", key=f"s_{i}")
                                if st.button("Kirim", key=f"b_{i}"):
                                    st.session_state.kotak_saran.append({"Waktu": datetime.now().strftime("%H:%M"), "Oleh": st.session_state.nama_user, "Konteks": f"{row.get('Nama_Indo')} ({row.get('Kode')})", "Pesan": sk})
                                    st.success("Terkirim!")
                    st.markdown('</div>', unsafe_allow_html=True)