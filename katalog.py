import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import json

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Warehouse Catalog JAMAL", page_icon="📦", layout="wide")

# 2. DATA KARYAWAN RESMI
DATA_KARYAWAN = {
    "84200082": "JAMALUDDIN",
    "84200061": "ENNI ROSDAENI",
    "85400228": "PUTRI",
    "84300997": "MUH. TAWAKKAL",
    "84102172": "WAHYU DWI SETYAN",
    "80519113": "UMI KHOLIFA"
}

# 3. KONEKSI KE FIREBASE (DATABASE)
if not firebase_admin._apps:
    # Mengambil rahasia dari info yang Bapak berikan
    key_dict = st.secrets["textkey"] if "textkey" in st.secrets else {
        "type": "service_account",
        "project_id": "jamal-f27cc",
        "private_key_id": "93c496d2c1cdbc6895a483eba775901636640557",
        "private_key": st.secrets["private_key"].replace('\\n', '\n'),
        "client_email": "firebase-adminsdk-fbsvc@jamal-f27cc.iam.gserviceaccount.com",
        "client_id": "110514718222395303109",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40jamal-f27cc.iam.gserviceaccount.com"
    }
    cred = credentials.Certificate(key_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Fungsi Simpan Saran ke Database
def kirim_saran_ke_firebase(nama, konteks, pesan):
    try:
        db.collection("saran_gudang").add({
            "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "oleh": nama,
            "barang": konteks,
            "isi_pesan": pesan
        })
        return True
    except:
        return False

# 4. CSS (GAMBAR KECIL & RAPI)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}
    .stDeployButton {display:none;} [data-testid="stSidebar"] {display: none;}
    .img-box img { width: 140px !important; height: 140px !important; object-fit: contain; border-radius: 10px; }
    .product-card { background-color: white; padding: 15px; border-radius: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 10px; border-left: 5px solid #007bff; }
    .mandarin-text { color: #e67e22; font-weight: bold; font-size: 0.9em; background: #fff5eb; padding: 3px 8px; border-radius: 5px; display: inline-block; }
    .kode-badge { background-color: #34495e; color: white; padding: 2px 8px; border-radius: 5px; font-size: 0.8em; }
    </style>
    """, unsafe_allow_html=True)

# 5. LOGIKA LOGIN
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

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
    # --- HEADER ---
    c1, c2 = st.columns([4, 1])
    with c1: st.subheader(f"📦 Catalog & Chat - {st.session_state.nama_user}")
    with c2: 
        if st.button("Keluar"): 
            st.session_state.logged_in = False
            st.rerun()

    # MENU ADMIN (PAK JAMALUDDIN MELIHAT SARAN)
    if st.session_state.nik_user == "84200082":
        with st.expander("📊 LIHAT SARAN MASUK (FIREBASE REAL-TIME)"):
            docs = db.collection("saran_gudang").order_by("waktu", direction=firestore.Query.DESCENDING).stream()
            list_saran = []
            for doc in docs:
                list_saran.append(doc.to_dict())
            
            if list_saran:
                st.table(pd.DataFrame(list_saran))
            else:
                st.write("Belum ada saran masuk.")

    st.divider()

    # --- LAYOUT DUA KOLOM ---
    col_kiri, col_kanan = st.columns([1.1, 2.9], gap="medium")

    with col_kiri:
        st.write("**💬 Obrolan Grup**")
        st.components.v1.iframe("https://www3.cbox.ws/box/?boxid=3554511&boxtag=eFn5Pq", height=450, scrolling=True)
        
        # SARAN UMUM (FIREBASE)
        if st.session_state.nik_user != "84200082":
            with st.expander("📢 Kirim Saran Umum"):
                su = st.text_area("Masukan...", key="su_area")
                if st.button("Kirim Saran"):
                    if su:
                        if kirim_saran_ke_firebase(st.session_state.nama_user, "UMUM", su):
                            st.success("Terkirim!")

    with col_kanan:
        st.write("**🔍 Cari Material**")
        search = st.text_input("", placeholder="Ketik nama/kode barang...")
        
        # Load Data
        df = pd.read_csv("data_barang.csv", encoding='utf-8-sig').fillna('')

        if search:
            hasil = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
            for i, row in hasil.iterrows():
                with st.container():
                    st.markdown('<div class="product-card">', unsafe_allow_html=True)
                    f1, f2 = st.columns([1, 3])
                    with f1:
                        foto = str(row.get('Foto', '')).strip()
                        url = f"https://res.cloudinary.com/dj4xyen1s/image/upload/f_auto,q_auto/{foto}.jpg"
                        st.markdown(f'<div class="img-box"><img src="{url}"></div>', unsafe_allow_html=True)
                    with f2:
                        st.markdown(f"**{row.get('Nama_Indo')}**")
                        if row.get('Nama_Mandarin'): st.markdown(f"<span class='mandarin-text'>{row.get('Nama_Mandarin')}</span>", unsafe_allow_html=True)
                        st.write(f"Kode: <span class='kode-badge'>{row.get('Kode')}</span>", unsafe_allow_html=True)
                        
                        # SARAN BARANG (FIREBASE)
                        if st.session_state.nik_user != "84200082":
                            with st.expander("📝 Berikan Saran"):
                                sk = st.text_area("Pesan...", key=f"s_{i}")
                                if st.button("Kirim", key=f"b_{i}"):
                                    if kirim_saran_ke_firebase(st.session_state.nama_user, f"{row.get('Nama_Indo')} ({row.get('Kode')})", sk):
                                        st.success("Tersimpan!")
                    st.markdown('</div>', unsafe_allow_html=True)