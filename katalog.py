import streamlit as st
import pandas as pd
from datetime import datetime
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

# 3. DATABASE MEMORI (Data akan hilang jika aplikasi restart)
if "log_kunjungan" not in st.session_state:
    st.session_state.log_kunjungan = []
if "kotak_saran" not in st.session_state:
    st.session_state.kotak_saran = []

# 4. SETTING CLOUDINARY
CLOUD_NAME = "dj4xyen1s"
BASE_URL = f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/f_auto,q_auto,w_150,h_150,c_pad,b_white/"

# 5. CSS UNTUK UKURAN GAMBAR RAPI
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}
    .stDeployButton {display:none;} [data-testid="stSidebar"] {display: none;}
    
    /* Background */
    .main { background-color: #f8f9fa; }
    
    /* Kartu Produk */
    .product-card { 
        background-color: white; padding: 12px; border-radius: 10px; 
        box-shadow: 0 2px 6px rgba(0,0,0,0.05); margin-bottom: 10px; 
        border-left: 5px solid #007bff;
    }
    
    /* PENGATURAN GAMBAR (PENTING) */
    .img-box {
        width: 100%;
        max-width: 150px; /* Ukuran gambar dibatasi */
        height: 150px;
        overflow: hidden;
        border-radius: 8px;
        border: 1px solid #eee;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: white;
    }
    .img-box img {
        max-width: 100%;
        max-height: 100%;
        object-fit: contain;
    }
    
    .mandarin-text { 
        color: #e67e22; font-weight: bold; background-color: #fff5eb; 
        padding: 1px 6px; border-radius: 4px; font-size: 0.85em;
    }
    
    .kode-badge { 
        background-color: #34495e; color: white; padding: 1px 6px; 
        border-radius: 4px; font-family: monospace; font-size: 0.8em;
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
        st.markdown(f"### 📦 Digital Catalog - {st.session_state.nama_user}")
    with c2:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    # PANEL ADMIN
    if st.session_state.nik_user == "84200082":
        with st.expander("📊 PANEL ADMIN"):
            t1, t2 = st.tabs(["👥 Login", "📩 Saran"])
            with t1: st.table(pd.DataFrame(st.session_state.log_kunjungan))
            with t2: st.table(pd.DataFrame(st.session_state.kotak_saran))

    st.divider()

    # --- LAYOUT DUA KOLOM ---
    col_kiri, col_kanan = st.columns([1.1, 2.9], gap="medium")

    with col_kiri:
        st.write("**💬 Obrolan Grup**")
        st.components.v1.iframe("https://www3.cbox.ws/box/?boxid=3554511&boxtag=eFn5Pq", height=450, scrolling=True)
        
        if st.session_state.nik_user != "84200082":
            with st.expander("📢 Saran Umum"):
                su = st.text_area("Tulis saran...", key="su")
                if st.button("Kirim Saran"):
                    if su:
                        st.session_state.kotak_saran.append({"Waktu": datetime.now().strftime("%H:%M"), "Oleh": st.session_state.nama_user, "Konteks": "UMUM", "Pesan": su})
                        st.success("Terkirim!")

    with col_kanan:
        st.write("**🔍 Cari Material**")
        search = st.text_input("", placeholder="Ketik nama atau kode barang...")
        
        @st.cache_data
        def get_data():
            try:
                return pd.read_csv("data_barang.csv", encoding='utf-8-sig').fillna('')
            except:
                return pd.DataFrame()

        df = get_data()
        
        if search:
            hasil = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
            for i, row in hasil.iterrows():
                st.markdown(f'''
                <div class="product-card">
                    <div style="display: flex; gap: 15px; align-items: flex-start;">
                        <div class="img-box">
                            <img src="{BASE_URL}{str(row.get('Foto', '')).strip()}.jpg">
                        </div>
                        <div style="flex: 1;">
                            <h4 style="margin: 0; color: #2c3e50;">{row.get('Nama_Indo')}</h4>
                            <div style="margin-top: 5px;">
                                <span class="mandarin-text">{row.get('Nama_Mandarin')}</span>
                            </div>
                            <div style="margin-top: 5px;">
                                <span class="kode-badge">Kode: {row.get('Kode')}</span>
                            </div>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                
                # Tombol Saran (Streamlit Button harus di luar f-string HTML)
                if st.session_state.nik_user != "84200082":
                    with st.expander(f"📝 Beri Saran untuk {row.get('Nama_Indo')}"):
                        pesan_saran = st.text_area("Pesan...", key=f"txt_{i}")
                        if st.button("Kirim Laporan", key=f"btn_{i}"):
                            st.session_state.kotak_saran.append({
                                "Waktu": datetime.now().strftime("%H:%M"), 
                                "Oleh": st.session_state.nama_user, 
                                "Konteks": row.get('Nama_Indo'), 
                                "Pesan": pesan_saran
                            })
                            st.success("Laporan terkirim ke Admin!")