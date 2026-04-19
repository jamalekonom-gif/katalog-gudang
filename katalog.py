import streamlit as st
import pandas as pd

# Identitas Cloudinary Bapak
CLOUD_NAME = "dj4xyen1s"
BASE_URL = f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/"

st.set_page_config(page_title="Katalog Gudang Online", layout="wide")
st.title("📦 Katalog Barang Gudang")

@st.cache_data
def load_data():
    try:
        try:
            df = pd.read_csv("data_barang.csv", encoding='utf-8')
        except:
            df = pd.read_csv("data_barang.csv", encoding='latin1')
        
        # Membersihkan nama kolom dari spasi agar pas dengan Nama_Indo, dll
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Gagal membaca file CSV: {e}")
        return pd.DataFrame()

df = load_data()

search = st.text_input("Cari Nama Barang atau Kode Material:")

if search and not df.empty:
    hasil = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
    
    if not hasil.empty:
        for index, row in hasil.iterrows():
            with st.container():
                col1, col2 = st.columns([1, 3])
                
                # MENGAMBIL DATA DARI EXCEL BAPAK
                nama_indo = str(row.get('Nama_Indo', 'Tidak Ada Nama'))
                nama_mandarin = str(row.get('Nama_Mandarin', '-'))
                kode_barang = str(row.get('Kode', '-'))
                # Kita ambil kolom Foto untuk gambar
                foto_id = str(row.get('Foto', '')).strip()
                
                with col1:
                    if foto_id and foto_id != 'nan':
                        # Memanggil foto dari Cloudinary
                        url_foto = f"{BASE_URL}{foto_id}.jpg"
                        st.image(url_foto, use_container_width=True)
                    else:
                        st.info("Foto tidak tersedia")
                
                with col2:
                    st.subheader(nama_indo)
                    st.write(f"**Nama Mandarin:** {nama_mandarin}")
                    st.write(f"**Kode Material:** {kode_barang}")
                st.divider()
    else:
        st.warning("Barang tidak ditemukan.")