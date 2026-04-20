import streamlit as st
import pandas as pd
from datetime import datetime

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Warehouse Digital Catalog", page_icon="📦", layout="wide")

# 2. DATA KARYAWAN (DAFTAR NIK RESMI)
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

# 5. CSS - TAMPILAN BERSIH & PROFESIONAL
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}
    .stDeployButton {display:none;} [data-testid="stSidebar"] {display: none;}
    .stImage img { max-height: 250px; width: auto; border-radius: 10px; object-fit: contain; }
    .product-card { background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 25px; border-top: 4px solid #007bff; }
    .mandarin-text { color: #d35400; font-weight: bold; background-color: #fff5eb; padding: 5px 10px; border-radius: 8px; display: inline-block; }
    .kode-badge { background-color: #34495e; color: white; padding: 3px 12px; border-radius: 50px; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

# 6. LOGIKA LOGIN
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("#")
        st.image("https://cdn-icons-png.flaticon.com/512/408/408710.png", width=100)
        st.title("🔒 Akses Gudang")
        nik_input = st.text_input("NIK Karyawan:", type="password")
        if st.button("Masuk Ke Sistem", use_container_width=True):
            if nik_input in DATA_KARYAWAN:
                st.session_state.logged_in = True
                st.session_state.nama_user = DATA_KARYAWAN[nik_input]
                st.session_state.nik_user = nik_input
                # Catat login
                st.session_state.log_kunjungan.append({
                    "Waktu": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "Nama": st.session_state.nama_user
                })
                st.rerun()
            else:
                st.error("⚠️ NIK Tidak Terdaftar")
else:
    # --- HALAMAN UTAMA SETELAH LOGIN ---
    c_nama, c_logout = st.columns([4, 1])
    with c_nama:
        st.info(f"👤 Selamat bekerja, **{st.session_state.nama_user}**!")
    with c_logout:
        if st.button("Keluar (Logout)", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    # --- MENU ADMIN (KHUSUS PAK JAMALUDDIN) ---
    if st.session_state.nik_user == "84200082":
        with st.expander("📊 MENU ADMIN (RIWAYAT LOGIN & SARAN)"):
            t1, t2 = st.tabs(["👥 Pengunjung", "📩 Kritik & Saran"])
            with t1: st.table(pd.DataFrame(st.session_state.log_kunjungan))
            with t2: st.table(pd.DataFrame(st.session_state.kotak_saran))

    st.divider()

    # --- FITUR CHAT TERINTEGRASI (OBROLAN NYAMBUNG ANTAR HP) ---
    st.subheader("💬 Obrolan Grup Gudang")
    
    # LINK DI BAWAH INI ADALAH CONTOH. 
    # Nanti kalau Bapak sudah daftar Cbox, ganti tulisan 'CONTOH' dengan ID Bapak.
    link_chat_cbox = "https://www2.cbox.ws/box/?boxid=953258&boxtag=v8v7r8" 
    
    st.components.v1.iframe(link_chat_cbox, height=450, scrolling=True)
    
    st.divider()

    # --- PENCARIAN BARANG ---
    def load_data():
        encodings = ['utf-8-sig', 'gb18030', 'utf-16', 'cp1252']
        for enc in encodings:
            try:
                df = pd.read_csv("data_barang.csv", encoding=enc).fillna('')
                df.columns = df.columns.str.strip()
                return df
            except: continue
        return pd.DataFrame()

    df = load_data()
    search = st.text_input("", placeholder="🔍 Cari Nama Barang atau Kode Material...")
    
    if search and not df.empty:
        hasil = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
        if not hasil.empty:
            for i, row in hasil.iterrows():
                with st.container():
                    st.markdown('<div class="product-card">', unsafe_allow_html=True)
                    c_f, c_t = st.columns([1, 2.5])
                    with c_f:
                        f = str(row.get('Foto', '')).strip()
                        url = f"{BASE_URL}{f}.jpg" if f else "https://via.placeholder.com/300"
                        st.image(url, use_container_width=True)
                    with c_t:
                        st.markdown(f"### {row.get('Nama_Indo', '-')}")
                        st.markdown(f"<span class='mandarin-text'>{row.get('Nama_Mandarin', '-')}</span>", unsafe_allow_html=True)
                        st.write(f"**Kode:** <span class='kode-badge'>{row.get('Kode', '-')}</span>", unsafe_allow_html=True)
                        
                        # Saran Spesifik Barang (Hanya untuk karyawan)
                        if st.session_state.nik_user != "84200082":
                            with st.expander("📝 Catatan Barang"):
                                s_khusus = st.text_area("Tulis saran...", key=f"kh_{i}")
                                if st.button("Kirim", key=f"bt_{i}"):
                                    st.session_state.kotak_saran.append({
                                        "Waktu": datetime.now().strftime("%H:%M"),
                                        "Oleh": st.session_state.nama_user,
                                        "Pesan": f"{row.get('Nama_Indo')} - {s_khusus}"
                                    })
                                    st.success("Terkirim!")
                    st.markdown('</div>', unsafe_allow_html=True)
    
    # --- SARAN UMUM (HANYA KARYAWAN) ---
    if st.session_state.nik_user != "84200082":
        st.divider()
        st.subheader("📢 Kritik & Saran Umum")
        s_umum = st.text_area("Masukan untuk gudang secara keseluruhan...", key="umum")
        if st.button("Kirim Saran Umum", use_container_width=True):
            if s_umum:
                st.session_state.kotak_saran.append({
                    "Waktu": datetime.now().strftime("%H:%M"),
                    "Oleh": st.session_state.nama_user,
                    "Pesan": f"UMUM: {s_umum}"
                })
                st.success("✅ Terima kasih, saran sudah diterima Pak Jamaluddin!")