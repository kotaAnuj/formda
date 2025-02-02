import os
import streamlit as st
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, auth
from googleapiclient.discovery import build
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from datetime import datetime, timedelta
import json
import requests

# --- Firebase Configuration ---
FIREBASE_CONFIG = {
    "type": "service_account",
    "project_id": "nothing-d3af4",
    "private_key_id": "7e4fa4486188e7dc9732e2bf03ed36e7bbbd4acd",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCi+Iys/cP5NsBO\nQC+RId4jkJZU9NeXttW6n+k8ZqK7VYVDQ5Kl5fcnOR+52/WVQ6Mt9pOpwiFizFEu\n8VjiG2rLZZA03i3w8RAHt6Dn9xBDWzzOFmZB7RlAJojYJlluXvERFbWJiElV27ZJ\n33do0ABsXpYSKtaV+uz6ENOegS9/9e9gmGo6+ElEhS5PuXrRMrFA3K6DzTywT9HJ\nOpsy7Y7Jmt3XPQhWo6oevCiqv3vwPXu15lXeRkg8acuBNeweRx8Dm0sXqZXCoTdp\nYzH3m8AzP9ewNFThm7hQ6UV6jQj6mWAfYmFjTqlwIsQRvCXAtElbCyLRWmDuIErB\nhJLat/QbAgMBAAECggEAEAd+Xq1/Dw4RkCDEDPRV0w2vm5+RbPywvPBpkmVN8DsT\nJnCJBgQ+cP8vXaqC1zGV5TlxgKr1ebA68/ENGwAzWtoceva3chFj0D6Bdw9X7CgX\nLPYLDMTzTNn9b7Ul6rMv5sxJ1MMw417+6Pkv14FN6VrMS/Emtg2+LUJmbhqqv10b\nAUkA+6R9yKqmvPElwUAjblwZjPY5+buZYMAS4BGPn3TSbIccknElFJm0w1zGuFmA\n9jex63WJ5tDkXXDBbai8aTJuX30beOj2gvgpAzwr08nHDqdOpSXrauZyrn4vtPjk\nYW/8T1OWLiY/sq1aphU9Geb3bfJ6Vj5id1zu3emY8QKBgQDSn5CZk1T1y8zcjsRS\n63jqZQnvnHuDkk3tVynMESkvvxrUn4WzYE5Opmi7j+hZXn6X1ATlb+j+xqt/ajjA\nlkhFbKbSUNMiq6ppfIL0RTESwNrwSSNkzz1aIQWgADPeYLd5wc24lmkp34eRtVNV\nZJv2r/biGcJFaVqArjTQZgKOjQKBgQDGFNPv7Jpz6X32bSobfZkvDMUqueUG4ULS\nPg+2Q9MoRiI8KFNJdna8iuGM1YRd269tyEdDCAB1sBebqiBm7X/XDPQDJThY9PN9\nyLWCRK2YFQBQJwgmJRdqTqI2ow+bbIEuULLaO4uaqSH+dP2cg9BkfpibtOWyzWvt\nRcXcjfLXRwKBgDimWEMmQHS38wrjj2RqFyScNnbvFL2HrVQH3KMZfoVsFjBYE6Ly\nZT18PrEr/KeE5fG6QfLgDb/w+ZGUpV0PTrL1jU0GFjO+DmC+7435ykAsBPcaBN4J\na4wBU7z8MPc/9jlWahmawwBTMeh758URAW3xWCrqGLmIo6H2uRfQSCHFAoGAHiYX\naAI0NAZK9NICwbJpOV8RN4KZ2GU63XMywwQpxIyAM3XTz2+nfOUKlXv+LKb+WZBN\nQGecYk1OGpRXYDMv7RR8o2nr3KZT1UZSUiSP44D2zjxSojOtD7IuQHCrNHXcZ6dC\nwbKkegLaOLenzkXF1zXplnF/MKrRjYi8J+i3GIsCgYBb77hZ6SjcXWgU905/8q/I\nN56geykqo3NARG/UfhvGlWmxH3J0vVUp4UvVPalDP1h0o4oftwkTnnATsOgizK5c\ngMdVAWgkFopjG0Y6pCu10i75irHLpM9EL/BkuqevT4dssaB4JT71GyCCho50xoON\ntgDzB5j2R1AL0muvHQ34bw==\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-gu32b@nothing-d3af4.iam.gserviceaccount.com",
    "client_id": "116989293124035568174",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-gu32b%40nothing-d3af4.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

FIREBASE_WEB_CONFIG = {
    "apiKey": "AIzaSyCadZIoYzIc_QhEkGjv86G4rjFwMASd5ig",
    "authDomain": "nothing-d3af4.firebaseapp.com",
    "projectId": "nothing-d3af4",
    "storageBucket": "nothing-d3af4.appspot.com",
    "messagingSenderId": "7155955115",
    "appId": "1:7155955115:web:3bd80618f9aff1a4dc8eee",
    "measurementId": "G-XSVGL2M8LL"
}

# --- Initialization ---
@st.cache_resource
def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(FIREBASE_CONFIG)
        firebase_admin.initialize_app(cred)

@st.cache_resource
def initialize_gemini():
    genai.configure(api_key="AIzaSyDpaOZq0jE6d4SdTpf1GyNk_lLkB75Kn_8")
    return genai.GenerativeModel('gemini-pro')

# --- Authentication ---
def sign_in_with_google():
    auth_url = f"https://accounts.google.com/o/oauth2/auth?client_id={FIREBASE_WEB_CONFIG['apiKey']}&response_type=id_token&scope=openid%20profile%20email&redirect_uri={st.experimental_get_query_params().get('redirect_uri', [''])[0]}&state=STATE_STRING"
    st.markdown(f'<a href="{auth_url}">Sign in with Google</a>', unsafe_allow_html=True)

def verify_id_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        st.error(f"Authentication failed: {str(e)}")
        return None

def handle_authentication():
    query_params = st.experimental_get_query_params()
    if 'id_token' in query_params:
        decoded_token = verify_id_token(query_params['id_token'][0])
        if decoded_token:
            st.session_state.user = {
                'uid': decoded_token['uid'],
                'email': decoded_token['email'],
                'name': decoded_token.get('name', 'User'),
                'expires': datetime.now() + timedelta(hours=1)
            }
            st.experimental_set_query_params()

# --- Main Application ---
def show_auth_sidebar():
    with st.sidebar:
        st.header("Authentication")
        if st.session_state.user:
            st.markdown(f"""
                **Logged in as:**  
                👤 {st.session_state.user.get('name', 'User')}  
                📧 {st.session_state.user['email']}  
                ⏳ Session expires: {st.session_state.user['expires'].strftime('%Y-%m-%d %H:%M:%S')}
            """)
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.clear()
                st.rerun()
        else:
            st.subheader("Sign In")
            sign_in_with_google()

def main():
    st.set_page_config(
        page_title="Workspace Creator",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    initialize_firebase()
    gemini_model = initialize_gemini()
    handle_authentication()
    
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    show_auth_sidebar()
    
    if st.session_state.user:
        st.header("Welcome to Workspace Creator")
        # Add your main application content here
    else:
        st.info("Please sign in to access the workspace creation tools")

if __name__ == "__main__":
    main()
