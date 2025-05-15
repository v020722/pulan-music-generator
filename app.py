import streamlit as st
import openai
from pydub import AudioSegment
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os
import json

# 🔐 Load API Key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# 🌐 Google Drive Authentication
@st.cache_resource
def authenticate_drive():
    """Authenticate Google Drive using client secrets from Streamlit secrets."""
    try:
        # Load the secret from Streamlit Secrets
        client_secret = {
            "web": {
                "client_id": st.secrets["GOOGLE_DRIVE_CLIENT_SECRET"]["client_id"],
                "project_id": st.secrets["GOOGLE_DRIVE_CLIENT_SECRET"]["project_id"],
                "auth_uri": st.secrets["GOOGLE_DRIVE_CLIENT_SECRET"]["auth_uri"],
                "token_uri": st.secrets["GOOGLE_DRIVE_CLIENT_SECRET"]["token_uri"],
                "auth_provider_x509_cert_url": st.secrets["GOOGLE_DRIVE_CLIENT_SECRET"]["auth_provider_x509_cert_url"],
                "client_secret": st.secrets["GOOGLE_DRIVE_CLIENT_SECRET"]["client_secret"],
                "redirect_uris": st.secrets["GOOGLE_DRIVE_CLIENT_SECRET"]["redirect_uris"]
            }
        }

        # Save it to JSON format for GoogleAuth
        with open('client_secrets.json', 'w') as f:
            json.dump(client_secret, f)

        # Authenticate and initialize the drive
        gauth = GoogleAuth()
        gauth.LoadClientConfigFile('client_secrets.json')
        gauth.CommandLineAuth()
        drive = GoogleDrive(gauth)
        st.success("✅ Google Drive authenticated successfully!")
        return drive
    
    except KeyError as e:
        st.error(f"❌ Missing key in Streamlit Secrets: {e}")
    except Exception as e:
        st.error(f"❌ Error in Google Drive Authentication: {e}")

    return None

drive = authenticate_drive()
