import streamlit as st
import pandas as pd

# Identitas Cloudinary Bapak
CLOUD_NAME = "dj4xyen1s"
BASE_URL = f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/"

st.set_page_config(page_title="Katalog Gudang Online", layout="wide")
st.title("📦 Katalog Barang Gudang")

# Fungsi baca data yang lebih aman
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data_barang.csv")
        # Membersihkan spasi di nama kolom agar tidak KeyError
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Gagal membaca file CSV: {e}")
        return pd.DataFrame()

df = load_data()

search = st.text_input("Cari Kode Material atau Nama Barang:")

if search and not df.empty:
    # Cari di semua kolom
    hasil = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
    
    if not hasil.empty:
        for index, row in hasil.iterrows():
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    # CEK KOLOM 'Foto'
                    if 'Foto' in df.columns:
                        # OTOMATIS TAMBAH .jpg DI SINI
                        kode_foto = str(row['Foto']).strip()
                        nama_file_lengkap = kode_foto + ".jpg" 
                        
                        url_foto = BASE_URL + nama_file_lengkap
                        st.image(url_foto, use_container_width=True)
                    else:
                        st.warning("Kolom 'Foto' tidak ditemukan.")
                
                with col2:
                    st.subheader(row.get('Nama Barang', 'Tanpa Nama'))
                    st.write(f"**Kode Material:** {row.get('Foto', '-')}")
                st.divider()
    else:
        st.warning("Barang tidak ditemukan.")