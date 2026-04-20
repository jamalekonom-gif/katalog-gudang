import streamlit as st
import pandas as pd

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Warehouse Digital Catalog", 
    page_icon="📦", 
    layout="wide"
)

# 2. DAFTAR NIK (Silakan tambah NIK karyawan di sini)
NIK_TERDAFTAR = ["84200061", "84200082", "85400228", "84300997", "84102172", "80519113"]

# 3. SETTING CLOUDINARY
CLOUD_NAME = "dj4xyen1s"
BASE_URL = f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/f_auto,q_auto/"

# CSS UNTUK TAMPILAN PROFESIONAL & LOGIN DI TENGAH
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    .main { background-color: #f8f9fa; }
    
    /* Box Login di Tengah */
    .login-box {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        max-width: 400px;
        margin: auto;
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

# 4. LOGIKA LOGIN (HALAMAN UTAMA)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # TAMPILAN LOGIN DI TENGAH
    st.write("#") # Kasih jarak atas
    col1, col2, col3 = st.columns([1, 2, 1]) # Buat kolom agar box ada di tengah
    
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/408/408710.png", width=100)
        st.title("🔒 Akses Gudang")
        st.write("Silakan masukkan NIK Anda untuk melihat katalog.")
        
        nik_input = st.text_input("NIK Karyawan:", type="password", placeholder="Ketik NIK di sini...")
        
        if st.button("Masuk Ke Sistem", use_container_width=True):
            if nik_input in NIK_TERDAFTAR:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("⚠️ NIK Tidak Terdaftar!")
else:
    # --- HALAMAN KATALOG (Jika sudah login) ---
    st.title("📦 Digital Warehouse Catalog")
    
    # Tombol Logout ditaruh di Sidebar agar tidak mengganggu pencarian
    with st.sidebar:
        st.success("✅ Anda Terverifikasi")
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
                        st.markdown("---")
                        st.markdown("✅ **Status:** Barang Aktif")
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("Data tidak ditemukan.")
    elif not search:
        st.info("Silakan ketik nama barang untuk mencari.")