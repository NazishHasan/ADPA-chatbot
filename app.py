import streamlit as st
import requests
import tempfile
import os
from gtts import gTTS
from PIL import Image
import streamlit as st

st.set_page_config(page_title="AL Dhafra Private Academy ChatBot", layout="centered")

# Hide Hugging Face branding menu and footer
hide_hf_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
"""
st.markdown(hide_hf_style, unsafe_allow_html=True)

# API Key and Model Setup
GROQ_API_KEY = st.secrets["KidsAPI"]
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-70b-8192"

# Title
st.title("🎓**عالِم أونلاين** - Al Dhafra Private Academy's Educational ChatBot-Student friendly")
st.markdown("Hello! I’m **Aalim Online**, your smart helper chatbot 🤖. Type a question below in **ENGLISH** or **ARABIC** and I’ll answer — and read it aloud, too! 🎧")

# Load Avatar
avatar = Image.open("Robochatbot.png")
st.image(avatar, width=200)

# Ask for the student's name
student_name = st.text_input("What is your name?")

if student_name:
    st.write(f"Hello, **{student_name}**! 👋 How can I assist you today?")
else:
    st.write("Hello, young learner! 👋 How can I assist you today?")
    
# Subject Filter
subject = st.selectbox("📚 Choose a subject", ["General", "Math", "Science", "English", "Social Studies", "Technology"])

# Language detection (basic Arabic check)
def is_arabic(text):
    return any('\u0600' <= char <= '\u06FF' for char in text)

# EduBot Response Function
def get_groq_response(user_input, subject):
    if is_arabic(user_input):
        system_prompt = "أنت مساعد ذكي يساعد الطلاب من الصف الأول إلى الصف الثامن. اجعل إجاباتك بسيطة ولطيفة."
    else:
        system_prompt = f"You are a helpful, friendly assistant for students in Grades 1 to 8. Answer in a clear and child-friendly way with clear and short or medium size description. Subject: {subject}"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    }

    response = requests.post(GROQ_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        st.error(f"API error: {response.status_code} - {response.text}")
        return "Sorry, I couldn't get a response. Please try again."

# Text-to-Speech
def speak_text(text, lang="en"):
    tts = gTTS(text, lang=lang)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        audio_file = open(fp.name, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')
        audio_file.close()
        os.unlink(fp.name)


# Input box for the user question
user_input = st.text_input("✏️ Type your question here:")

# Single button with unique key
if st.button("Ask EduBot", key="ask_button"):
    if user_input:
        with st.spinner("Thinking..."):
            answer = get_groq_response(user_input, subject)
            st.success("🌟 EduBot: " + answer)
            speak_text(answer, lang="ar" if is_arabic(user_input) else "en")
    else:
        st.warning("Please type a question.")


st.markdown("---")
st.markdown("💡 *Try questions like:*")
st.markdown("- What is a fraction?\n- Explain the water cycle.\n- Tell me a grammar rule.\n- من هو مخترع الكهرباء؟")
