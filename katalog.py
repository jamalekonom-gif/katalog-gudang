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

# 5. CSS UNTUK TAMPILAN DASHBOARD MODERN
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}
    .stDeployButton {display:none;} [data-testid="stSidebar"] {display: none;}
    
    /* Background Halaman */
    .main { background-color: #f0f2f6; }
    
    /* Kotak Produk */
    .product-card { 
        background-color: white; 
        padding: 15px; 
        border-radius: 15px; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); 
        margin-bottom: 20px; 
        border-left: 5px solid #007bff;
        transition: transform 0.2s;
    }
    .product-card:hover { transform: scale(1.01); }
    
    /* Nama Mandarin */
    .mandarin-text { 
        color: #e67e22; 
        font-weight: bold; 
        background-color: #fdf2e9; 
        padding: 4px 10px; 
        border-radius: 6px; 
        display: inline-block;
        margin-top: 5px;
    }
    
    /* Badge Kode Material */
    .kode-badge { 
        background-color: #2c3e50; 
        color: white; 
        padding: 2px 10px; 
        border-radius: 4px; 
        font-family: 'Courier New', monospace;
        font-size: 0.9em;
    }

    /* Container Chat */
    .chat-container {
        background-color: white;
        border-radius: 15px;
        padding: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
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
        nik_input = st.text_input("Masukkan NIK Anda:", type="password")
        if st.button("Masuk Ke Sistem", use_container_width=True):
            if nik_input in DATA_KARYAWAN:
                st.session_state.logged_in = True
                st.session_state.nama_user = DATA_KARYAWAN[nik_input]
                st.session_state.nik_user = nik_input
                st.session_state.log_kunjungan.append({"Waktu": datetime.now().strftime("%H:%M:%S"), "Nama": st.session_state.nama_user})
                st.rerun()
            else: st.error("⚠️ NIK Tidak Terdaftar")
else:
    # --- HEADER UTAMA ---
    c_head1, c_head2 = st.columns([4, 1])
    with c_head1:
        st.title("📦 Digital Warehouse Catalog")
        st.write(f"Selamat bekerja, **{st.session_state.nama_user}**!")
    with c_head2:
        st.write("#")
        if st.button("Keluar (Logout)", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    # MENU ADMIN (KHUSUS PAK JAMALUDDIN)
    if st.session_state.nik_user == "84200082":
        with st.expander("📊 PANEL KONTROL ADMIN (RAHASIA)"):
            t1, t2 = st.tabs(["👥 Pengunjung Hari Ini", "📩 Rekap Saran"])
            with t1: st.table(pd.DataFrame(st.session_state.log_kunjungan))
            with t2: 
                if st.session_state.kotak_saran: st.table(pd.DataFrame(st.session_state.kotak_saran))
                else: st.write("Belum ada saran masuk.")

    st.divider()

    # --- TATA LETAK KOLOM (LAYOUT) ---
    # Kolom 1 (Kiri) untuk Chat, Kolom 2 (Kanan) untuk Katalog
    col_kiri, col_kanan = st.columns([1.2, 2.8], gap="large")

    # --- BAGIAN KIRI: OBROLAN ---
    with col_kiri:
        st.subheader("💬 Obrolan Grup")
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        link_cbox = "https://www3.cbox.ws/box/?boxid=3554511&boxtag=eFn5Pq"
        st.components.v1.iframe(link_cbox, height=600, scrolling=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Saran Umum diletakkan di bawah chat agar rapi
        if st.session_state.nik_user != "84200082":
            st.write("#")
            with st.expander("📢 Kirim Kritik/Saran Umum"):
                su = st.text_area("Masukan Anda...", key="su_input")
                if st.button("Kirim Saran"):
                    st.session_state.kotak_saran.append({
                        "Waktu": datetime.now().strftime("%H:%M"), 
                        "Oleh": st.session_state.nama_user, 
                        "Konteks": "UMUM", "Pesan": su
                    })
                    st.success("Terkirim!")

    # --- BAGIAN KANAN: KATALOG BARANG ---
    with col_kanan:
        st.subheader("🔍 Cari Material")
        search = st.text_input("", placeholder="Ketik Nama Barang atau Kode di sini...")
        
        def load_data():
            for enc in ['utf-8-sig', 'gb18030', 'cp1252', 'latin1']:
                try:
                    df = pd.read_csv("data_barang.csv", encoding=enc).fillna('')
                    df.columns = df.columns.str.strip()
                    return df
                except: continue
            return pd.DataFrame()

        df = load_data()
        
        if search:
            hasil = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
            if not hasil.empty:
                st.write(f"Menampilkan {len(hasil)} hasil pencarian:")
                for i, row in hasil.iterrows():
                    with st.container():
                        st.markdown('<div class="product-card">', unsafe_allow_html=True)
                        c_foto, c_teks = st.columns([1, 2])
                        with c_foto:
                            f = str(row.get('Foto', '')).strip()
                            url = f"{BASE_URL}{f}.jpg" if f else "https://via.placeholder.com/300"
                            st.image(url, use_container_width=True)
                        with c_teks:
                            st.markdown(f"### {row.get('Nama_Indo')}")
                            # Memastikan Nama Mandarin Muncul
                            mandarin = row.get('Nama_Mandarin')
                            if mandarin:
                                st.markdown(f"<div class='mandarin-text'>{mandarin}</div>", unsafe_allow_html=True)
                            
                            st.write(f"**Kode Material:** <span class='kode-badge'>{row.get('Kode')}</span>", unsafe_allow_html=True)
                            
                            # Saran Per Barang (Hanya Karyawan)
                            if st.session_state.nik_user != "84200082":
                                with st.expander("📝 Berikan Saran"):
                                    s_khusus = st.text_area("Pesan...", key=f"s_{i}")
                                    if st.button("Kirim", key=f"b_{i}"):
                                        st.session_state.kotak_saran.append({
                                            "Waktu": datetime.now().strftime("%H:%M"), 
                                            "Oleh": st.session_state.nama_user, 
                                            "Konteks": f"{row.get('Nama_Indo')} ({row.get('Kode')})",
                                            "Pesan": s_khusus
                                        })
                                        st.success("Tersimpan!")
                        st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("Barang tidak ditemukan. Coba kata kunci lain.")
        else:
            st.info("Silakan ketik nama barang pada kolom pencarian di atas untuk melihat katalog.")