import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Katalog Gudang Digital", layout="wide")

@st.cache_data
def load_data():
    file_path = "data_barang.csv"
    if os.path.exists(file_path):
        # Mencoba format paling umum untuk Mandarin (GB18030 atau UTF-8)
        for enc in ['gb18030', 'utf-8-sig', 'utf-8', 'latin-1']:
            try:
                # Coba baca dengan koma atau titik koma
                for sep in [',', ';']:
                    df = pd.read_csv(file_path, encoding=enc, sep=sep)
                    if not df.empty:
                        # Bersihkan nama kolom
                        df.columns = [str(c).strip().lower() for c in df.columns]
                        return df
            except:
                continue
    return pd.DataFrame()

st.title("📦 Katalog Barang Gudang")
df = load_data()

if not df.empty:
    st.success(f"✅ Berhasil memuat {len(df)} data barang.")
    cari = st.text_input("Ketik Nama Barang atau Kode di sini...")
    
    if cari:
        # Mencari di semua kolom dan pastikan semua jadi teks
        hasil = df[df.astype(str).apply(lambda x: x.str.contains(cari, case=False)).any(axis=1)]
        
        if not hasil.empty:
            for i, row in hasil.iterrows():
                col1, col2 = st.columns([1, 4])
                with col1:
                    # Cari kolom foto
                    c_foto = [c for c in df.columns if 'foto' in c]
                    nama_f = str(row[c_foto[0]]) if c_foto else ""
                    path = os.path.join("FOTO MATERIAL", nama_f)
                    if os.path.exists(path) and nama_f != "nan" and nama_f != "":
                        st.image(path, width=150)
                    else:
                        st.warning("No Photo")
                with col2:
                    # Cari kolom nama dan kode
                    c_indo = [c for c in df.columns if 'indo' in c]
                    c_mand = [c for c in df.columns if 'mandarin' in c]
                    c_kode = [c for c in df.columns if 'kode' in c]
                    
                    st.subheader(f"{row[c_indo[0]] if c_indo else 'N/A'} / {row[c_mand[0]] if c_mand else 'N/A'}")
                    st.write(f"**Kode:** {row[c_kode[0]] if c_kode else 'N/A'}")
                st.divider()
        else:
            st.info("Barang tidak ditemukan.")
else:
    st.error("Gagal membaca file 'data_barang.csv'.")