import streamlit as st
import pandas as pd
from datetime import datetime

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Warehouse Digital Catalog", page_icon="📦", layout="wide")

# 2. DATA KARYAWAN
DATA_KARYAWAN = {
    "84200082": "JAMALUDDIN",
    "84200061": "ENNI ROSDAENI",
    "85400228": "PUTRI",
    "84300997": "MUH. TAWAKKAL",
    "84102172": "WAHYU DWI SETYAN",
    "80519113": "UMI KHOLIFA"
}

# 3. DATABASE MEMORI (Sesi Aktif)
if "log_kunjungan" not in st.session_state:
    st.session_state.log_kunjungan = []
if "kotak_saran" not in st.session_state:
    st.session_state.kotak_saran = []
if "chat_gudang" not in st.session_state:
    st.session_state.chat_gudang = [] # Tempat simpan obrolan

# 4. SETTING CLOUDINARY
CLOUD_NAME = "dj4xyen1s"
BASE_URL = f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/f_auto,q_auto/"

# CSS - TAMPILAN BERSIH & BOX CHAT
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    [data-testid="stSidebar"] {display: none;}
    .stImage img { max-height: 250px; width: auto; border-radius: 10px; object-fit: contain; }
    .product-card { background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 25px; border-top: 4px solid #007bff; }
    .mandarin-text { color: #d35400; font-weight: bold; background-color: #fff5eb; padding: 5px 10px; border-radius: 8px; display: inline-block; }
    .kode-badge { background-color: #34495e; color: white; padding: 3px 12px; border-radius: 50px; font-family: monospace; }
    
    /* Gaya Chat */
    .chat-box {
        background-color: #e9ecef;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 5px;
    }
    .chat-user { font-weight: bold; color: #007bff; font-size: 0.9em; }
    .chat-time { color: #6c757d; font-size: 0.7em; }
    </style>
    """, unsafe_allow_html=True)

# 5. LOGIKA LOGIN
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("#")
        st.image("https://cdn-icons-png.flaticon.com/512/408/408710.png", width=100)
        st.title("🔒 Akses Gudang")
        nik_input = st.text_input("NIK Karyawan:", type="password")
        if st.button("Masuk Ke Sistem", use_container_width=True):
            if nik_input in DATA_KARYAWAN:
                st.session_state.logged_in = True
                st.session_state.nama_user = DATA_KARYAWAN[nik_input]
                st.session_state.nik_user = nik_input
                waktu = datetime.now().strftime("%H:%M")
                st.session_state.log_kunjungan.append({"Waktu": waktu, "Nama": st.session_state.nama_user, "NIK": nik_input})
                st.rerun()
            else:
                st.error("NIK Tidak Terdaftar")
else:
    # --- HALAMAN UTAMA ---
    st.title("📦 Digital Warehouse Catalog")
    
    c_nama, c_logout = st.columns([4, 1])
    with c_nama:
        st.info(f"👤 **{st.session_state.nama_user}** (Online)")
    with c_logout:
        if st.button("Keluar (Logout)", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    # --- MENU ADMIN PAK JAMALUDDIN ---
    if st.session_state.nik_user == "84200082":
        with st.expander("📊 MENU ADMIN (RAHASIA)"):
            tab1, tab2 = st.tabs(["👥 Riwayat Login", "📩 Kritik & Saran"])
            with tab1: st.table(pd.DataFrame(st.session_state.log_kunjungan))
            with tab2: st.table(pd.DataFrame(st.session_state.kotak_saran))

    st.divider()

    # --- FITUR OBROLAN (CHAT) GUDANG ---
    with st.expander("💬 OBROLAN GRUP GUDANG (KOORDINASI)"):
        # Tampilkan Pesan
        chat_container = st.container(height=300)
        for pesan in st.session_state.chat_gudang:
            chat_container.markdown(f"""
            <div class="chat-box">
                <span class="chat-user">{pesan['User']}</span> <span class="chat-time">{pesan['Waktu']}</span><br>
                {pesan['Pesan']}
            </div>
            """, unsafe_allow_html=True)
        
        # Input Pesan
        with st.form("chat_form", clear_on_submit=True):
            teks_chat = st.text_input("Ketik pesan di sini...", placeholder="Contoh: Tolong cek stok baut di Rak A")
            submit_chat = st.form_submit_button("Kirim")
            if submit_chat and teks_chat:
                st.session_state.chat_gudang.append({
                    "User": st.session_state.nama_user,
                    "Waktu": datetime.now().strftime("%H:%M"),
                    "Pesan": teks_chat
                })
                st.rerun()

    st.divider()
    
    # --- PENCARIAN BARANG ---
    def load_data():
        for enc in ['utf-8-sig', 'gb18030', 'cp1252']:
            try: return pd.read_csv("data_barang.csv", encoding=enc).fillna('')
            except: continue
        return pd.DataFrame()

    df = load_data()
    search = st.text_input("", placeholder="🔍 Cari Barang...")
    
    if search:
        hasil = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
        for i, row in hasil.iterrows():
            with st.container():
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                c_f, c_t = st.columns([1, 2.5])
                with c_f:
                    f = str(row.get('Foto', '')).strip()
                    st.image(f"{BASE_URL}{f}.jpg" if f else "https://via.placeholder.com/300", use_container_width=True)
                with c_t:
                    st.markdown(f"### {row.get('Nama_Indo')}")
                    st.markdown(f"<span class='mandarin-text'>{row.get('Nama_Mandarin')}</span>", unsafe_allow_html=True)
                    st.write(f"**Kode:** {row.get('Kode')}")
                    
                    # Kotak Saran (Hanya Karyawan)
                    if st.session_state.nik_user != "84200082":
                        with st.expander("📝 Saran Barang"):
                            s = st.text_area("Catatan...", key=f"s_{i}")
                            if st.button("Kirim", key=f"b_{i}"):
                                st.session_state.kotak_saran.append({"Waktu": datetime.now().strftime("%H:%M"), "Oleh": st.session_state.nama_user, "Detail": f"{row.get('Nama_Indo')} - {s}"})
                                st.success("Terkirim!")
                st.markdown('</div>', unsafe_allow_html=True)
                # Tambahkan ini di bagian load data agar chat bisa terbaca antar sesi
def load_chat():
    if os.path.exists("chat_history.csv"):
        return pd.read_csv("chat_history.csv").to_dict('records')
    return []

def save_chat(user, pesan):
    waktu = datetime.now().strftime("%H:%M")
    new_chat = pd.DataFrame([{"Waktu": waktu, "User": user, "Pesan": pesan}])
    new_chat.to_csv("chat_history.csv", mode='a', header=not os.path.exists("chat_history.csv"), index=False)

    # --- KRITIK SARAN UMUM (Hanya Karyawan) ---
    if st.session_state.nik_user != "84200082":
        st.divider()
        st.subheader("📢 Kritik & Saran Umum")
        su = st.text_area("Masukan umum...", key="su")
        if st.button("Kirim Saran Umum"):
            st.session_state.kotak_saran.append({"Waktu": datetime.now().strftime("%H:%M"), "Oleh": st.session_state.nama_user, "Detail": su})
            st.success("Terkirim!")