import streamlit as st
import openai
import PyPDF2
import io

# Fungsi untuk membaca teks dari PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

# Fungsi untuk menganalisis teks menggunakan OpenAI API
def analyze_contract_with_openai(text, openai_api_key):
    openai.api_key = openai_api_key
    try:
        response = openai.chat.completions.create(
            model="gpt-4",  # Anda bisa mengganti dengan model lain seperti "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "Anda adalah asisten yang ahli dalam menganalisis dokumen kontrak. Berikan ringkasan, poin-poin penting, dan potensi risiko."},
                {"role": "user", "content": f"Analisis dokumen kontrak berikut ini:\n\n{text}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Terjadi kesalahan saat memanggil OpenAI API: {e}"

st.set_page_config(layout="wide")
st.title("Aplikasi Analisis Dokumen Kontrak PDF")

# Sidebar untuk input API Key
st.sidebar.header("Konfigurasi OpenAI")
openai_api_key = st.sidebar.text_input("Masukkan OpenAI API Key Anda", type="password")
st.sidebar.markdown("Dapatkan API Key Anda dari [OpenAI Dashboard](https://platform.openai.com/account/api-keys)")

# Main content
st.header("Unggah Dokumen Kontrak PDF")
uploaded_file = st.file_uploader("Pilih file PDF", type="pdf")

if uploaded_file is not None:
    st.success("File PDF berhasil diunggah!")

    if openai_api_key:
        with st.spinner("Mengekstrak teks dari PDF..."):
            pdf_text = extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
            st.subheader("Pratinjau Teks yang Diekstrak:")
            st.text_area("Teks dari PDF", pdf_text[:1000] + "...", height=200) # Menampilkan 1000 karakter pertama

        if st.button("Mulai Analisis Kontrak"):
            with st.spinner("Menganalisis kontrak menggunakan OpenAI... Ini mungkin memakan waktu beberapa saat."):
                analysis_result = analyze_contract_with_openai(pdf_text, openai_api_key)
                st.subheader("Hasil Analisis Kontrak:")
                st.write(analysis_result)
    else:
        st.warning("Mohon masukkan OpenAI API Key Anda di sidebar untuk memulai analisis.")

st.markdown("---")
st.markdown("Dibuat dengan ❤️ oleh Asisten AI")
