import streamlit as st
import google.generativeai as genai
from docx import Document
import io

# Konfigurasi Halaman
st.set_page_config(page_title="AI News Generator", layout="centered")

st.title("📰 Selamat Datang di i-Humas PUI-PT Disruptive Learning Innovation (DLI) Universitas Negeri Malang Ver 1.0 ")

# --- LOGIKA API KEY OTOMATIS ---
# Mencoba mengambil dari Streamlit Secrets, jika kosong baru minta input manual
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    # Sidebar hanya muncul jika tidak ada secret (untuk pengembangan lokal)
    api_key = st.sidebar.text_input("Masukkan Kode Password (API Key)", type="password")

# --- KONFIGURASI GENAI ---
# Kita harus memastikan api_key terisi sebelum memanggil genai.configure
if api_key:
    genai.configure(api_key=api_key)
else:
    st.warning("Silakan masukkan API Key di sidebar untuk memulai.")

# Form Input
with st.form("news_form"):
    judul = st.text_input("Judul Berita")
    tempat = st.text_input("Tempat Kejadian")
    waktu = st.text_input("Waktu Kejadian")
    narasumber = st.text_input("Narasumber")
    gaya = st.selectbox("Gaya Bahasa", ["Formal", "Santai", "Investigatif", "Sensasional"])
    rincian = st.text_area("Rincian Kejadian")
    kata_kunci = st.text_input("Kata Kunci (pisahkan dengan koma)")
    submit = st.form_submit_button("Generate Berita")

# Fungsi untuk membuat file Word
def create_docx(text):
    doc = Document()
    doc.add_heading('Hasil Berita AI', 0)
    doc.add_paragraph(text)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# Proses Generate
if submit:
    if not api_key:
        st.error("API Key belum tersedia!")
    else:
        try:
            # Detektif Model: Mencari model yang mendukung generateContent
            available_models = [m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            
            if not available_models:
                st.error("Tidak ditemukan model yang mendukung generateContent!")
            else:
                model_name = available_models[0].name
                model = genai.GenerativeModel(model_name)
                
                prompt = f"Anda adalah jurnalis. Tulis berita dengan judul: {judul}, Lokasi: {tempat}, Waktu: {waktu}, Narasumber: {narasumber}, Gaya: {gaya}. Detail: {rincian}. Kata Kunci: {kata_kunci}."
                
                with st.spinner("Sedang menyusun berita..."):
                    response = model.generate_content(prompt)
                    berita_teks = response.text
                    st.write(berita_teks)
                    
                    doc_buffer = create_docx(berita_teks)
                    st.download_button("📥 Download Berita (.docx)", doc_buffer, "berita.docx")
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")