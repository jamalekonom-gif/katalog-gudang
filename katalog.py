import streamlit as st
import pandas as pd

CLOUD_NAME = "dj4xyen1s"
BASE_URL = f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/"

st.set_page_config(page_title="Katalog Gudang Online", layout="wide")
st.title("📦 Katalog Barang Gudang")

@st.cache_data
def load_data():
    # Mencoba membaca dengan berbagai format agar Mandarin muncul
    for enc in ['utf-8-sig', 'utf-8', 'gb18030', 'cp1252']:
        try:
            df = pd.read_csv("data_barang.csv", encoding=enc)
            df.columns = df.columns.str.strip()
            return df
        except:
            continue
    return pd.DataFrame()

df = load_data()

search = st.text_input("Cari Nama Barang atau Kode Material:")

if search and not df.empty:
    hasil = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
    
    if not hasil.empty:
        for index, row in hasil.iterrows():
            with st.container():
                col1, col2 = st.columns([1, 2])
                
                nama_indo = str(row.get('Nama_Indo', '-'))
                nama_mand = str(row.get('Nama_Mandarin', '-'))
                foto_id = str(row.get('Foto', '')).strip()
                kode_mat = str(row.get('Kode', '-'))
                
                with col1:
                    if foto_id and foto_id != 'nan' and foto_id != '0':
                        # Kode ini mencoba menampilkan foto
                        url = f"{BASE_URL}{foto_id}.jpg"
                        st.image(url, use_container_width=True)
                    else:
                        st.warning("Foto tidak ditemukan")
                
                with col2:
                    st.header(nama_indo)
                    st.subheader(f"Mandarin: {nama_mand}")
                    st.write(f"**Kode:** {kode_mat}")
                    # Link rahasia untuk tes (Klik ini kalau gambar pecah)
                    if foto_id:
                        st.caption(f"[Klik untuk tes link foto](https://res.cloudinary.com/{CLOUD_NAME}/image/upload/{foto_id}.jpg)")
                st.divider()
    else:
        st.warning("Barang tidak ditemukan.")