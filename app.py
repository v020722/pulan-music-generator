import streamlit as st
import openai
from pydub import AudioSegment
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os

# 🔐 Set your OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# 🌐 Google Drive Authentication (No JSON File Required)
@st.cache_resource
def authenticate_drive():
    """Authenticate Google Drive using OAuth 2.0."""
    try:
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()  # Open a browser for Google login
        drive = GoogleDrive(gauth)
        st.success("✅ Google Drive authenticated successfully!")
        return drive
    except Exception as e:
        st.error(f"❌ Google Drive Authentication Failed: {e}")
        return None

drive = authenticate_drive()

# 🎹 Generate Music Function
def generate_music(prompt, duration):
    """Generate a MIDI music file based on a prompt."""
    st.write(f"🎼 Generating music for: **{prompt}**")
    try:
        # ChatCompletion call for music generation
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a music composer."},
                {"role": "user", "content": f"Generate a musical composition for the theme: '{prompt}' in MIDI format."}
            ]
        )

        midi_data = response.choices[0].message['content']

        # Save to MIDI file
        with open("musenet_output.mid", "w") as f:
            f.write(midi_data)

        st.success("🎵 Music generated and saved as `musenet_output.mid`")
        st.audio("musenet_output.mid")
    except Exception as e:
        st.error(f"❌ Failed to generate music: {e}")

# 🔄 Load Music from Google Drive
def load_from_drive(file_id):
    """Download a MIDI file from Google Drive and play it."""
    if not drive:
        st.error("Google Drive is not authenticated.")
        return
    
    st.write(f"📥 Downloading from Google Drive ID: **{file_id}**")
    try:
        file = drive.CreateFile({'id': file_id})
        file.GetContentFile('drive_output.mid')
        st.success("✅ Music loaded from Drive!")
        st.audio('drive_output.mid')
    except Exception as e:
        st.error(f"❌ Error loading from Google Drive: {e}")

# 📌 Streamlit UI
st.title("🎵 Pulan")
st.write("Generate beautiful music with OpenAI MuseNet and Google Drive integration.")

# ✏️ Music Prompt
prompt = st.text_input("Enter a music prompt (e.g., Epic Orchestral, Jazz Piano)")
duration = st.slider("Select duration (seconds):", 10, 300, 30)

# 🎼 Generate Button
if st.button("Generate Music"):
    generate_music(prompt, duration)

# 📥 Google Drive ID Input
file_id = st.text_input("Google Drive File ID")
if st.button("Load from Google Drive"):
    load_from_drive(file_id)

# 📂 File Uploader
uploaded_file = st.file_uploader("Upload a MIDI file", type=["mid"])
if uploaded_file is not None:
    with open("uploaded_midi.mid", "wb") as f:
        f.write(uploaded_file.read())
    st.success("✅ File uploaded successfully!")
    st.audio("uploaded_midi.mid")
