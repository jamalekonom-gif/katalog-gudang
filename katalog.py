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

# 3. DATABASE MEMORI (Sesi Aktif)
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
    
    /* Memaksa Gambar Tetap Kecil & Rapi */
    .img-box img {
        width: 130px !important;
        height: 130px !important;
        object-fit: contain;
        border-radius: 8px;
        background-color: #f8f9fa;
        border: 1px solid #eee;
    }
    
    .product-card { 
        background-color: white; padding: 12px; border-radius: 10px; 
        box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 8px; 
        border-left: 5px solid #007bff;
    }
    
    .mandarin-text { color: #e67e22; font-weight: bold; font-size: 0.85em; background: #fff5eb; padding: 2px 5px; border-radius: 4px; display: inline-block; }
    .kode-badge { background-color: #34495e; color: white; padding: 2px 6px; border-radius: 4px; font-size: 0.75em; font-family: monospace; }
    .section-label { color: #2c3e50; font-weight: bold; font-size: 1rem; margin-bottom: -10px; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 6. LOGIKA LOGIN
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
                st.session_state.log_kunjungan.append({"Waktu": datetime.now().strftime("%d/%m/%Y %H:%M"), "Nama": st.session_state.nama_user})
                st.rerun()
            else: st.error("NIK Salah")
else:
    # --- HEADER ---
    c1, c2 = st.columns([4, 1])
    with c1:
        st.markdown(f"### 📦 Catalog & Chat")
        st.caption(f"User: {st.session_state.nama_user}")
    with c2:
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    # MENU ADMIN (KHUSUS PAK JAMALUDDIN)
    if st.session_state.nik_user == "84200082":
        with st.expander("📊 PANEL ADMIN (RIWAYAT & SARAN)"):
            t1, t2 = st.tabs(["👥 Pengunjung", "📩 Rekap Saran"])
            with t1: st.table(pd.DataFrame(st.session_state.log_kunjungan))
            with t2: 
                if st.session_state.kotak_saran:
                    st.table(pd.DataFrame(st.session_state.kotak_saran))
                else:
                    st.write("Belum ada saran.")

    st.divider()

    # --- LAYOUT DASHBOARD ---
    col_kiri, col_kanan = st.columns([1.1, 2.9], gap="medium")

    # SISI KIRI: CHAT & SARAN UMUM
    with col_kiri:
        st.markdown('<p class="section-label">💬 Obrolan Grup</p>', unsafe_allow_html=True)
        link_cbox = "https://www3.cbox.ws/box/?boxid=3554511&boxtag=eFn5Pq"
        st.components.v1.iframe(link_cbox, height=500, scrolling=True)
        
        # SARAN UMUM (MASUK KE TAB ADMIN BAPAK)
        if st.session_state.nik_user != "84200082":
            st.write("#")
            with st.expander("📢 Kirim Saran Umum"):
                su = st.text_area("Tulis saran untuk gudang...", key="su_area")
                if st.button("Kirim Saran"):
                    if su:
                        st.session_state.kotak_saran.append({
                            "Waktu": datetime.now().strftime("%H:%M"),
                            "Oleh": st.session_state.nama_user,
                            "Konteks": "UMUM",
                            "Pesan": su
                        })
                        st.success("Terkirim ke Admin!")

    # SISI KANAN: PENCARIAN BARANG
    with col_kanan:
        st.markdown('<p class="section-label">🔍 Cari Material</p>', unsafe_allow_html=True)
        search = st.text_input("", placeholder="Ketik nama atau kode barang...")
        
        def load_data():
            # Mengatasi UnicodeDecodeError
            for enc in ['utf-8-sig', 'gb18030', 'cp1252', 'latin1']:
                try:
                    df_temp = pd.read_csv("data_barang.csv", encoding=enc).fillna('')
                    df_temp.columns = df_temp.columns.str.strip()
                    return df_temp
                except: continue
            return pd.DataFrame()

        df = load_data()
        
        if search and not df.empty:
            hasil = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
            if not hasil.empty:
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
                            if row.get('Nama_Mandarin'):
                                st.markdown(f"<span class='mandarin-text'>{row.get('Nama_Mandarin')}</span>", unsafe_allow_html=True)
                            st.write(f"Kode: <span class='kode-badge'>{row.get('Kode')}</span>", unsafe_allow_html=True)
                            
                            # SARAN PER BARANG (MASUK KE TAB ADMIN BAPAK)
                            if st.session_state.nik_user != "84200082":
                                with st.expander("📝 Saran Barang"):
                                    sk = st.text_area("Masukan...", key=f"s_{i}")
                                    if st.button("Kirim", key=f"b_{i}"):
                                        st.session_state.kotak_saran.append({
                                            "Waktu": datetime.now().strftime("%H:%M"),
                                            "Oleh": st.session_state.nama_user,
                                            "Konteks": f"{row.get('Nama_Indo')} ({row.get('Kode')})",
                                            "Pesan": sk
                                        })
                                        st.success("Saran tersimpan!")
                        st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("Barang tidak ditemukan.")