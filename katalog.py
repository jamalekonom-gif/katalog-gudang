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

# 3. DATABASE MEMORI (Sesi Aktif)
if "log_kunjungan" not in st.session_state:
    st.session_state.log_kunjungan = []
if "kotak_saran" not in st.session_state:
    st.session_state.kotak_saran = []

# 4. SETTING CLOUDINARY
CLOUD_NAME = "dj4xyen1s"
BASE_URL = f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/f_auto,q_auto/"

# CSS - TAMPILAN RAPI & COMPACT
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    [data-testid="stSidebar"] {display: none;}
    
    /* Kartu Produk Ringkas */
    .product-card { 
        background-color: white; padding: 15px; border-radius: 12px; 
        box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 15px; 
        border-left: 5px solid #007bff; 
    }
    
    /* Pengaturan Gambar 75px agar tidak kebesaran */
    .img-container {
        width: 85px; height: 85px; overflow: hidden; border-radius: 8px;
        border: 1px solid #eee; display: flex; align-items: center;
        justify-content: center; background-color: white;
    }
    .img-container img { max-width: 100%; max-height: 100%; object-fit: contain; }

    .mandarin-text { color: #d35400; font-weight: bold; background-color: #fff5eb; padding: 2px 8px; border-radius: 5px; font-size: 0.9em; }
    .kode-badge { background-color: #34495e; color: white; padding: 2px 10px; border-radius: 4px; font-family: monospace; font-size: 0.8em; }
    .section-title { color: #2c3e50; font-weight: bold; font-size: 1.1rem; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 5. LOGIKA LOGIN
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
                waktu = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                st.session_state.log_kunjungan.append({"Waktu": waktu, "Nama": st.session_state.nama_user, "NIK": nik_input})
                st.rerun()
            else:
                st.error("NIK Tidak Terdaftar")
else:
    # --- HEADER ---
    c_nama, c_logout = st.columns([4, 1])
    with c_nama:
        st.markdown(f"### 📦 Digital Warehouse - {st.session_state.nama_user}")
    with c_logout:
        if st.button("Keluar", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    # --- MENU ADMIN PAK JAMALUDDIN ---
    if st.session_state.nik_user == "84200082":
        with st.expander("📊 PANEL ADMIN (LAPORAN & SARAN)"):
            tab1, tab2 = st.tabs(["👥 Riwayat Login", "📩 Saran Masuk"])
            with tab1: st.table(pd.DataFrame(st.session_state.log_kunjungan))
            with tab2: st.table(pd.DataFrame(st.session_state.kotak_saran))

    st.divider()

    # --- LAYOUT DUA KOLOM (CBOX & KATALOG) ---
    col_kiri, col_kanan = st.columns([1.2, 2.8], gap="medium")

    # KOLOM KIRI: CBOX & SARAN UMUM
    with col_kiri:
        st.markdown('<p class="section-title">💬 Obrolan Grup</p>', unsafe_allow_html=True)
        # Link Cbox Bapak
        st.components.v1.iframe("https://www3.cbox.ws/box/?boxid=3554511&boxtag=eFn5Pq", height=500, scrolling=True)
        
        if st.session_state.nik_user != "84200082":
            with st.expander("📢 Kirim Saran Umum"):
                su = st.text_area("Masukan Anda...", key="su_input")
                if st.button("Kirim Saran Umum"):
                    if su:
                        st.session_state.kotak_saran.append({
                            "Waktu": datetime.now().strftime("%d/%m/%Y %H:%M"),
                            "Oleh": st.session_state.nama_user,
                            "Jenis": "Umum",
                            "Detail": su
                        })
                        st.success("Terkirim!")

    # KOLOM KANAN: KATALOG BARANG
    with col_kanan:
        st.markdown('<p class="section-title">🔍 Cari Material</p>', unsafe_allow_html=True)
        
        def load_data():
            for enc in ['utf-8-sig', 'gb18030', 'cp1252']:
                try:
                    df = pd.read_csv("data_barang.csv", encoding=enc).fillna('')
                    df.columns = df.columns.str.strip()
                    return df
                except: continue
            return pd.DataFrame()

        df = load_data()
        search = st.text_input("", placeholder="Ketik nama barang atau kode...")

        if search and not df.empty:
            hasil = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
            if not hasil.empty:
                for i, row in hasil.iterrows():
                    st.markdown('<div class="product-card">', unsafe_allow_html=True)
                    c_foto, c_teks = st.columns([1, 3])
                    
                    with c_foto:
                        foto = str(row.get('Foto', '')).strip()
                        url = f"{BASE_URL}{foto}.jpg" if foto else "https://via.placeholder.com/150"
                        st.markdown(f'''
                            <div class="img-container">
                                <img src="{url}">
                            </div>
                        ''', unsafe_allow_html=True)
                    
                    with c_teks:
                        st.markdown(f"**{row.get('Nama_Indo', '-')}**")
                        if row.get('Nama_Mandarin'):
                            st.markdown(f"<span class='mandarin-text'>{row.get('Nama_Mandarin')}</span>", unsafe_allow_html=True)
                        st.write(f"Kode: <span class='kode-badge'>{row.get('Kode', '-')}</span>", unsafe_allow_html=True)
                        
                        if st.session_state.nik_user != "84200082":
                            with st.expander("📝 Laporkan Barang Ini"):
                                sk = st.text_area("Catatan...", key=f"sk_{i}")
                                if st.button("Kirim Laporan", key=f"btn_{i}"):
                                    st.session_state.kotak_saran.append({
                                        "Waktu": datetime.now().strftime("%d/%m/%Y %H:%M"),
                                        "Oleh": st.session_state.nama_user,
                                        "Jenis": "Spesifik",
                                        "Detail": f"{row.get('Nama_Indo')} - {sk}"
                                    })
                                    st.success("Terkirim!")
                    st.markdown('</div>', unsafe_allow_html=True)