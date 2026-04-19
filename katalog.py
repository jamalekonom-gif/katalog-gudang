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
        # KODE SAKTI: Mencoba baca dengan format berbeda agar tidak error merah
        try:
            df = pd.read_csv("data_barang.csv", encoding='utf-8')
        except:
            df = pd.read_csv("data_barang.csv", encoding='latin1')
            
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Gagal membaca file CSV: {e}")
        return pd.DataFrame()

df = load_data()

search = st.text_input("Cari Kode Material atau Nama Barang:")

if search and not df.empty:
    hasil = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
    
    if not hasil.empty:
        for index, row in hasil.iterrows():
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    if 'Foto' in df.columns:
                        kode_foto = str(row['Foto']).strip()
                        # Kita langsung panggil tanpa folder karena sudah dipindah ke Home
                        url_foto = f"{BASE_URL}{kode_foto}.jpg"
                        st.image(url_foto, use_container_width=True)
                
                with col2:
                    st.subheader(row.get('Nama Barang', 'Tanpa Nama'))
                    st.write(f"**Kode Material:** {row.get('Foto', '-')}")
                st.divider()
    else:
        st.warning("Barang tidak ditemukan.")