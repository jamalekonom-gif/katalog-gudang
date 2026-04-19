import streamlit as st
import pandas as pd

# Masukkan Cloud Name Bapak yang tadi
CLOUD_NAME = "dj4xyen1s"
# Ini adalah alamat dasar foto Bapak di internet
BASE_URL = f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/"

st.set_page_config(page_title="Katalog Gudang Online", layout="wide")
st.title("📦 Katalog Barang Gudang")

# Fungsi untuk baca data
@st.cache_data
def load_data():
    return pd.read_csv("data_barang.csv")

df = load_data()

# Kolom Pencarian
search = st.text_input("Cari Kode Material atau Nama Barang:")

if search:
    # Cari di semua kolom
    hasil = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
    
    if not hasil.empty:
        for index, row in hasil.iterrows():
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    # RAKIT LINK FOTO OTOMATIS
                    # Menggabungkan Alamat Cloudinary + Nama File di Excel
                    url_foto = BASE_URL + str(row['Foto'])
                    
                    # Menampilkan Foto
                    st.image(url_foto, use_container_width=True)
                
                with col2:
                    st.subheader(row['Nama Barang'])
                    st.write(f"**Kode Material:** {row['Foto']}")
                    # Bapak bisa tambah kolom lain di sini, misal:
                    # st.write(f"**Lokasi Rak:** {row['Lokasi']}")
                st.divider()
    else:
        st.warning("Barang tidak ditemukan.")