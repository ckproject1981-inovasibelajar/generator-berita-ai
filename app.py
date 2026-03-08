import streamlit as st
import google.generativeai as genai
from docx import Document
import io

# Konfigurasi Halaman
st.set_page_config(page_title="AI News Generator", layout="centered")

# Sidebar untuk API Key
st.sidebar.title("Pengaturan")
api_key = st.sidebar.text_input("Masukkan Kode Password yang Telah Diberikan", type="password")

st.title("📰 i-Humas")

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
        st.error("API Key belum diisi!")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # Detektif Model: Mencari model yang mendukung generateContent
            available_models = [m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            
            if not available_models:
                st.error("Tidak ditemukan model yang mendukung generateContent!")
            else:
                model_name = available_models[0].name
                st.write(f"Menggunakan model: {model_name}")
                model = genai.GenerativeModel(model_name)
                
                prompt = f"Tuliskan berita dengan judul {judul}, detail: {rincian}."
                
                with st.spinner("Sedang menyusun berita..."):
                    response = model.generate_content(prompt)
                    berita_teks = response.text
                    st.write(berita_teks)
                    
                    doc_buffer = create_docx(berita_teks)
                    st.download_button("📥 Download Berita (.docx)", doc_buffer, "berita.docx")
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")