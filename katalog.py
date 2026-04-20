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

# CSS UNTUK MENYEMBUNYIKAN MENU STREAMLIT DAN MEMPERCANTIK TAMPILAN
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    .main { background-color: #f8f9fa; }
    
    /* MODIFIKASI UKURAN GAMBAR AGAR TIDAK TERLALU BESAR */
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
        font-size: 0.8em;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. SISTEM LOGIN
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

with st.sidebar:
    st.markdown("### 🔒 Akses Gudang")
    st.image("https://cdn-icons-png.flaticon.com/512/408/408710.png", width=80)
    
    if not st.session_state.logged_in:
        nik_input = st.text_input("NIK Karyawan:", type="password", placeholder="Masukkan NIK...")
        if st.button("Masuk Ke Sistem", use_container_width=True):
            if nik_input in NIK_TERDAFTAR:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("NIK Tidak Terdaftar")
    else:
        st.success("✅ Terverifikasi")
        st.divider()
        if st.button("Keluar (Logout)", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

# 5. HALAMAN UTAMA (KATALOG)
if st.session_state.logged_in:
    st.title("📦 Digital Warehouse Catalog")
    st.caption("Manajemen Informasi Material & Inventaris")
    
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
                    col1, col2 = st.columns([1, 2.5])
                    
                    nama_indo = str(row.get('Nama_Indo', '-'))
                    nama_mand = str(row.get('Nama_Mandarin', '-'))
                    kode_mat = str(row.get('Kode', '-'))
                    foto_id = str(row.get('Foto', '')).strip()

                    with col1:
                        if foto_id and foto_id not in ['nan', '0', '']:
                            final_foto_id = foto_id if foto_id.lower().endswith('.jpg') else foto_id + ".jpg"
                            st.image(f"{BASE_URL}{final_foto_id}", use_container_width=True)
                        else:
                            st.image("https://via.placeholder.com/300x300?text=Foto+Kosong", use_container_width=True)

                    with col2:
                        st.markdown(f"### {nama_indo}")
                        st.markdown(f'<span class="mandarin-text">{nama_mand}</span>', unsafe_allow_html=True)
                        st.write("")
                        # BAGIAN YANG DIPERBAIKI (Tanda petik sudah benar sekarang)
                        st.markdown(f"**Kode Material:** <span class='kode-badge'>{kode_mat}</span>", unsafe_allow_html=True)
                        st.markdown("---")
                        st.markdown("✅ **Status:** Barang Aktif")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ Data tidak ditemukan.")
    elif not search:
        st.info("Silakan ketik nama barang atau kode material pada kolom pencarian di atas.")

else:
    st.markdown("---")
    st.warning("Mohon login terlebih dahulu melalui panel samping kiri.")