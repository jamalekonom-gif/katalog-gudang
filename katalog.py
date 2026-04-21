import streamlit as st
import pandas as pd

# 1. KONFIGURASI
st.set_page_config(page_title="Warehouse Digital Catalog", page_icon="📦", layout="wide")

# 2. DATA KARYAWAN
DATA_KARYAWAN = {"84200082": "JAMALUDDIN", "84200061": "ENNI ROSDAENI", "85400228": "PUTRI", "84300997": "MUH. TAWAKKAL", "84102172": "WAHYU DWI SETYAN", "80519113": "UMI KHOLIFA"}

# 3. CSS (PASTI RAPI & GAMBAR KECIL)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}
    .stDeployButton {display:none;} [data-testid="stSidebar"] {display: none;}
    .img-box img { width: 140px !important; height: 140px !important; object-fit: contain; border-radius: 10px; border: 1px solid #eee; }
    .product-card { background-color: white; padding: 15px; border-radius: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 10px; border-left: 5px solid #007bff; }
    .mandarin-text { color: #e67e22; font-weight: bold; font-size: 0.9em; background: #fff5eb; padding: 3px 8px; border-radius: 5px; display: inline-block; }
    .kode-badge { background-color: #34495e; color: white; padding: 2px 8px; border-radius: 5px; font-size: 0.8em; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

# 4. LOGIN
if "logged_in" not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.title("🔒 Login Gudang")
        nik = st.text_input("NIK:", type="password")
        if st.button("Masuk"):
            if nik in DATA_KARYAWAN:
                st.session_state.logged_in, st.session_state.nama_user, st.session_state.nik_user = True, DATA_KARYAWAN[nik], nik
                st.rerun()
            else: st.error("NIK Salah")
else:
    # --- HALAMAN UTAMA ---
    c1, c2 = st.columns([4, 1])
    with c1: st.subheader(f"📦 Catalog & Chat - {st.session_state.nama_user}")
    with c2: 
        if st.button("Keluar"): 
            st.session_state.logged_in = False
            st.rerun()

    st.divider()

    # --- LAYOUT DUA KOLOM ---
    col_kiri, col_kanan = st.columns([1.1, 2.9], gap="medium")

    with col_kiri:
        st.write("**💬 Obrolan & Saran**")
        # PAKAI CBOX BAPAK (PASTI NYAMBUNG ANTAR HP)
        st.components.v1.iframe("https://www3.cbox.ws/box/?boxid=3554511&boxtag=eFn5Pq", height=550, scrolling=True)
        st.caption("Info: Untuk kirim saran barang, langsung ketik di atas ya Pak!")

    with col_kanan:
        st.write("**🔍 Cari Material**")
        search = st.text_input("", placeholder="Ketik nama/kode barang...")
        
        # Load Data
        for enc in ['utf-8-sig', 'gb18030', 'cp1252']:
            try:
                df = pd.read_csv("data_barang.csv", encoding=enc).fillna('')
                break
            except: df = pd.DataFrame()

        if search and not df.empty:
            hasil = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
            for i, row in hasil.iterrows():
                with st.container():
                    st.markdown('<div class="product-card">', unsafe_allow_html=True)
                    f1, f2 = st.columns([1, 3])
                    with f1:
                        foto = str(row.get('Foto', '')).strip()
                        url = f"https://res.cloudinary.com/dj4xyen1s/image/upload/f_auto,q_auto/{foto}.jpg" if foto else "https://via.placeholder.com/150"
                        st.markdown(f'<div class="img-box"><img src="{url}"></div>', unsafe_allow_html=True)
                    with f2:
                        st.markdown(f"#### {row.get('Nama_Indo')}")
                        if row.get('Nama_Mandarin'): st.markdown(f"<span class='mandarin-text'>{row.get('Nama_Mandarin')}</span>", unsafe_allow_html=True)
                        st.write(f"Kode: <span class='kode-badge'>{row.get('Kode')}</span>", unsafe_allow_html=True)
                        st.caption("Copy kode ini dan tempel di obrolan kiri jika ada saran.")
                    st.markdown('</div>', unsafe_allow_html=True)