import streamlit as st
import pandas as pd

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Warehouse Digital Catalog", 
    page_icon="📦", 
    layout="wide"
)

# 2. DAFTAR NIK DAN NAMA KARYAWAN (Silakan tambah di sini)
# Formatnya: "NIK": "Nama Karyawan"
DATA_KARYAWAN = {
    "84200061": "ENNI ROSDAENI",
    "84200082": "JAMALUDDIN",
    "85400228": "PUTRI",
    "84300997": "MUH. TAWAKKAL",
    "84102172": "WAHYU DWI SETYAN",
    "80519113": "UMI KHOLIFA"
}

# 3. SETTING CLOUDINARY
CLOUD_NAME = "dj4xyen1s"
BASE_URL = f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/f_auto,q_auto/"

# CSS UNTUK TAMPILAN PROFESIONAL
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    .main { background-color: #f8f9fa; }
    
    /* Box Login */
    .login-box {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
    }

    /* Ukuran Gambar Katalog */
    .stImage img {
        max-height: 250px;
        width: auto;
        border-radius: 10px;
        object-fit: contain;
    }
    
    .product-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 25px;
        border-top: 4px solid #007bff;
    }
    
    .mandarin-text {
        color: #d35400;
        font-weight: bold;
        font-size: 1.1em;
        background-color: #fff5eb;
        padding: 5px 10px;
        border-radius: 8px;
        display: inline-block;
    }
    
    .kode-badge {
        background-color: #34495e;
        color: white;
        padding: 3px 12px;
        border-radius: 50px;
        font-family: monospace;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. LOGIKA LOGIN
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.nama_user = ""

if not st.session_state.logged_in:
    st.write("#")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/408/408710.png", width=100)
        st.title("🔒 Akses Gudang")
        st.write("Silakan masukkan NIK Anda.")
        
        nik_input = st.text_input("NIK Karyawan:", type="password", placeholder="Ketik NIK...")
        
        if st.button("Masuk Ke Sistem", use_container_width=True):
            if nik_input in DATA_KARYAWAN:
                st.session_state.logged_in = True
                st.session_state.nama_user = DATA_KARYAWAN[nik_input] # Ambil nama berdasarkan NIK
                st.rerun()
            else:
                st.error("⚠️ NIK Tidak Terdaftar!")
else:
    # --- HALAMAN KATALOG ---
    st.title("📦 Digital Warehouse Catalog")
    # Menampilkan Nama Karyawan yang sedang login
    st.info(f"👤 Selamat Bekerja, **{st.session_state.nama_user}**!")
    
    with st.sidebar:
        st.write(f"Logged in as: **{st.session_state.nama_user}**")
        if st.button("Keluar (Logout)", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    def load_data():
        encodings = ['utf-8-sig', 'gb18030', 'utf-16', 'cp1252', 'latin1']
        for enc in encodings:
            try:
                df = pd.read_csv("data_barang.csv", encoding=enc, low_memory=False)
                df.columns = df.columns.str.strip()
                return df
            except:
                continue
        return pd.DataFrame()

    df = load_data()
    search = st.text_input("", placeholder="🔍 Cari Nama Barang atau Kode Material...")

    if search and not df.empty:
        hasil = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
        
        if not hasil.empty:
            st.write(f"Ditemukan **{len(hasil)}** item")
            for index, row in hasil.iterrows():
                with st.container():
                    st.markdown('<div class="product-card">', unsafe_allow_html=True)
                    c1, c2 = st.columns([1, 2.5])
                    
                    with c1:
                        foto_id = str(row.get('Foto', '')).strip()
                        if foto_id and foto_id not in ['nan', '0', '']:
                            final_foto_id = foto_id if foto_id.lower().endswith('.jpg') else foto_id + ".jpg"
                            st.image(f"{BASE_URL}{final_foto_id}", use_container_width=True)
                        else:
                            st.image("https://via.placeholder.com/300x300?text=Foto+Kosong", use_container_width=True)

                    with c2:
                        st.markdown(f"### {row.get('Nama_Indo', '-')}")
                        st.markdown(f'<span class="mandarin-text">{row.get("Nama_Mandarin", "-")}</span>', unsafe_allow_html=True)
                        st.write("")
                        st.markdown(f"**Kode Material:** <span class='kode-badge'>{row.get('Kode', '-')}</span>", unsafe_allow_html=True)
                        # TULISAN STATUS SUDAH DIHAPUS DI SINI
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("Data tidak ditemukan.")
    elif not search:
        st.write("Silakan ketik pada kolom pencarian di atas.")