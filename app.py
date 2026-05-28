import os
import math
import time
import requests
import streamlit as st
from pypdf import PdfReader
from docx import Document
from gtts import gTTS

# Core System Parameters
API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyDTsz4s3lKWy79WfDjs6TxuPj_0EyDza1M")

def extract_text_and_check_pages(uploaded_file, file_name):
    text = ""
    if file_name.endswith(".pdf"):
        pdf_reader = PdfReader(uploaded_file)
        if len(pdf_reader.pages) > 10:
            return None, f"Error: Document exceeds maximum limit of 10 pages (Found {len(pdf_reader.pages)} pages)."
        
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
                
    elif file_name.endswith(".docx"):
        doc = Document(uploaded_file)
        for paragraph in doc.paragraphs:
            if paragraph.text:
                text += paragraph.text + "\n"
                
    return text, None

def chunk_text(text, words_per_chunk=3000):
    words = text.split()
    total_chunks = math.ceil(len(words) / words_per_chunk)
    chunks = []
    for i in range(total_chunks):
        start = i * words_per_chunk
        end = start + words_per_chunk
        chunks.append(" ".join(words[start:end]))
    return chunks

def call_gemini_api(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    if response.status_code == 200:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    elif response.status_code == 429:
        st.error("API Rate Limit hit (429). Please try again in 1 minute.")
        st.stop()
    else:
        st.error(f"Gemini API Error ({response.status_code}): {response.text}")
        st.stop()

def summarize_chunks(chunks):
    partial_summaries = []
    progress_bar = st.progress(0)
    for idx, chunk in enumerate(chunks):
        percent_complete = int(((idx + 1) / len(chunks)) * 50)
        progress_bar.progress(percent_complete)
        prompt = f"Write a clean summary of this section. Use plain sentences without any markdown bullet points or formatting:\n\n{chunk}"
        partial_summaries.append(call_gemini_api(prompt))
        
    combined_text = "\n".join(partial_summaries)
    progress_bar.progress(75)
    
    final_prompt = (
        "You are an expert audiobook scriptwriter. Combine the following summaries into a single, continuous narrative script. "
        "It must flow smoothly like a story or essay from one topic to the next. CRITICAL: Do not include any headers, titles, "
        "bullet points, asterisks, or markdown formatting whatsoever. Provide only the raw, fluid text narrative:\n\n" + combined_text
    )
    final_result = call_gemini_api(final_prompt)
    progress_bar.progress(100)
    return final_result

# Word-by-word streaming generator function
def text_streamer(text_content):
    for word in text_content.split(" "):
        yield word + " "
        time.sleep(0.04) # Speed controller for typewriter effect

# Streamlit User Interface
st.set_page_config(page_title="DocuVoice AI", page_icon="🎧", layout="centered")

st.markdown("<h1 style='text-align: center; font-size: 3rem;'>🎧 DocuVoice AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.3rem; font-weight: 500;'>Convert large structural documents into smooth, fluid audiobook summaries instantly.</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.1rem; color: #a3a8b4;'>Upload a PDF or DOCX file (Max 10 pages for PDFs)</p>", unsafe_allow_html=True)
st.write("") 

uploaded_file = st.file_uploader("", type=["pdf", "docx"])

if uploaded_file is not None:
    st.info(f"Target File Acknowledged: {uploaded_file.name}")
    
    if st.button("Compile Audiobook System", use_container_width=True):
        raw_text, error_message = extract_text_and_check_pages(uploaded_file, uploaded_file.name)
        
        if error_message:
            st.error(error_message)
        elif not raw_text or not raw_text.strip():
            st.warning("Target document contains no extractable alphanumeric characters.")
        else:
            with st.spinner("Executing live multi-stage AI compilation..."):
                text_chunks = chunk_text(raw_text)
                final_summary = summarize_chunks(text_chunks)
                
                output_audio_path = "summary_audio.mp3"
                tts = gTTS(text=final_summary, lang='en')
                tts.save(output_audio_path)
                
                st.success("Analysis Complete!")
                
                # Dynamic typewriter streaming animation
                st.subheader("📝 Continuous Text Narrative Summary")
                st.write_stream(text_streamer(final_summary))
                
                # Live Audio Player presentation element
                st.subheader("🔊 Playable Audio Transcript")
                with open(output_audio_path, "rb") as audio_file:
                    st.audio(audio_file.read(), format="audio/mp3")
                    
                st.balloons()