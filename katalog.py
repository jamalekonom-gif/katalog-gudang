import streamlit as st
import pandas as pd

CLOUD_NAME = "dj4xyen1s"
BASE_URL = f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/"

st.set_page_config(page_title="Katalog Gudang Online", layout="wide")
st.title("📦 Katalog Barang Gudang")

@st.cache_data
def load_data():
    encodings = ['utf-8-sig', 'gb18030', 'utf-16', 'cp1252', 'latin1']
    for enc in encodings:
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
                        # KODE PINTAR: Cek apakah sudah ada .jpg di nama file
                        if not foto_id.lower().endswith('.jpg'):
                            final_foto_id = foto_id + ".jpg"
                        else:
                            final_foto_id = foto_id
                            
                        url_foto = f"{BASE_URL}{final_foto_id}"
                        st.image(url_foto, use_container_width=True)
                    else:
                        st.info("Foto belum ada")
                
                with col2:
                    st.header(nama_indo)
                    st.subheader(f"Mandarin: {nama_mand}")
                    st.write(f"**Kode Material:** {kode_mat}")
                st.divider()