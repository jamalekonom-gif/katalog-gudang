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

# 5. CSS - TAMPILAN BERSIH
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}
    .stDeployButton {display:none;} [data-testid="stSidebar"] {display: none;}
    .stImage img { max-height: 250px; width: auto; border-radius: 10px; object-fit: contain; }
    .product-card { background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 25px; border-top: 4px solid #007bff; }
    .mandarin-text { color: #d35400; font-weight: bold; background-color: #fff5eb; padding: 5px 10px; border-radius: 8px; display: inline-block; font-size: 1.1em; }
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
                st.session_state.log_kunjungan.append({"Waktu": datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Nama": st.session_state.nama_user})
                st.rerun()
            else: st.error("⚠️ NIK Tidak Terdaftar")
else:
    # --- HALAMAN UTAMA ---
    c_nama, c_logout = st.columns([4, 1])
    with c_nama:
        st.info(f"👤 Selamat bekerja, **{st.session_state.nama_user}**!")
    with c_logout:
        if st.button("Keluar", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    # MENU ADMIN (PAK JAMALUDDIN)
    if st.session_state.nik_user == "84200082":
        with st.expander("📊 MENU ADMIN (RIWAYAT LOGIN & SARAN)"):
            t1, t2 = st.tabs(["👥 Pengunjung", "📩 Rekap Kritik & Saran"])
            with t1: 
                st.table(pd.DataFrame(st.session_state.log_kunjungan))
            with t2: 
                if st.session_state.kotak_saran:
                    st.table(pd.DataFrame(st.session_state.kotak_saran))
                else:
                    st.write("Belum ada saran masuk.")

    st.divider()

    # --- FITUR OBROLAN GRUP ---
    st.subheader("💬 Obrolan Grup Gudang")
    link_cbox = "https://www3.cbox.ws/box/?boxid=3554511&boxtag=eFn5Pq"
    st.components.v1.iframe(link_cbox, height=450, scrolling=True)
    
    # --- KRITIK & SARAN UMUM ---
    if st.session_state.nik_user != "84200082":
        with st.expander("📢 Kirim Kritik & Saran Umum"):
            su = st.text_area("Tulis masukan Anda di sini...", key="su_input")
            if st.button("Kirim Saran Umum"):
                if su:
                    st.session_state.kotak_saran.append({
                        "Waktu": datetime.now().strftime("%d/%m/%Y %H:%M"), 
                        "Oleh": st.session_state.nama_user, 
                        "Konteks/Barang": "UMUM",
                        "Pesan Saran": su
                    })
                    st.success("✅ Terkirim ke Pak Jamaluddin!")
                else:
                    st.warning("Mohon isi pesan terlebih dahulu.")

    st.divider()

    # --- PENCARIAN BARANG ---
    def load_data():
        for enc in ['utf-8-sig', 'gb18030', 'cp1252', 'latin1']:
            try:
                df = pd.read_csv("data_barang.csv", encoding=enc).fillna('')
                df.columns = df.columns.str.strip()
                return df
            except: continue
        return pd.DataFrame()

    df = load_data()
    search = st.text_input("", placeholder="🔍 Cari Nama Barang atau Kode Material...")
    
    if search:
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
                        nama_brg = row.get('Nama_Indo')
                        nama_mand = row.get('Nama_Mandarin')
                        kode_brg = row.get('Kode')
                        
                        st.markdown(f"### {nama_brg}")
                        # MEMUNCULKAN KEMBALI NAMA MANDARIN
                        if nama_mand:
                            st.markdown(f"<span class='mandarin-text'>{nama_mand}</span>", unsafe_allow_html=True)
                        
                        st.write(f"**Kode:** <span class='kode-badge'>{kode_brg}</span>", unsafe_allow_html=True)
                        
                        # Saran Spesifik Barang
                        if st.session_state.nik_user != "84200082":
                            with st.expander(f"📝 Berikan Saran untuk {nama_brg}"):
                                s_khusus = st.text_area("Apa yang perlu diperbaiki/ditambahkan?", key=f"s_{i}")
                                if st.button("Kirim Saran", key=f"b_{i}"):
                                    if s_khusus:
                                        st.session_state.kotak_saran.append({
                                            "Waktu": datetime.now().strftime("%d/%m/%Y %H:%M"), 
                                            "Oleh": st.session_state.nama_user, 
                                            "Konteks/Barang": f"{nama_brg} ({kode_brg})",
                                            "Pesan Saran": s_khusus
                                        })
                                        st.success(f"✅ Saran untuk {kode_brg} telah dikirim!")
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("Data tidak ditemukan.")