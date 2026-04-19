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
        # Mencoba baca file dengan encoding berbeda agar tidak error merah
        try:
            df = pd.read_csv("data_barang.csv", encoding='utf-8')
        except:
            df = pd.read_csv("data_barang.csv", encoding='latin1')
        
        # Membersihkan nama kolom dari spasi yang tidak sengaja terketik
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Gagal membaca file CSV: {e}")
        return pd.DataFrame()

df = load_data()

search = st.text_input("Cari Nama Barang atau Kode Material:")

if search and not df.empty:
    # Mencari data di semua kolom (A, B, C, atau D)
    hasil = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
    
    if not hasil.empty:
        for index, row in hasil.iterrows():
            with st.container():
                col1, col2 = st.columns([1, 3])
                
                # SESUAIKAN DENGAN NAMA KOLOM EXCEL BAPAK
                # Nama_Indo untuk judul, Foto untuk gambar
                nama_tampil = row.get('Nama_Indo', 'Nama Tidak Ditemukan')
                nama_mandarin = row.get('Nama_Mandarin', '')
                kode_foto = str(row.get('Foto', '')).strip()
                
                with col1:
                    if kode_foto and kode_foto != 'nan':
                        # Otomatis tambah .jpg
                        url_foto = f"{BASE_URL}{kode_foto}.jpg"
                        st.image(url_foto, use_container_width=True)
                    else:
                        st.info("Tidak ada foto")
                
                with col2:
                    st.subheader(nama_tampil)
                    if nama_mandarin:
                        st.write(f"**Nama Mandarin:** {nama_mandarin}")
                    st.write(f"**Kode Material:** {kode_material}")
                st.divider()
    else:
        st.warning("Barang tidak ditemukan.")