# app.py
import os
import streamlit as st
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, auth
from googleapiclient.discovery import build
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs, urlencode
import httpx
from pydantic import BaseModel
from typing import Optional

# --- Environment Configuration ---
class AppConfig(BaseModel):
    firebase_web_api_key: str = "AIzaSyCadZIoYzIc_QhEkGjv86G4rjFwMASd5ig"
    gemini_api_key: str = "AIzaSyDpaOZq0jE6d4SdTpf1GyNk_lLkB75Kn_8"
    google_client_id: str = "7155955115-49hktiu4afnqe61k87fhk1cfrop9j46l.apps.googleusercontent.com"
    google_client_secret: str = "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"
    google_project_id: str = "nothing-d3af4"
    service_account_info: dict = {
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

def load_config() -> AppConfig:
    return AppConfig()

# --- Constants ---
SCOPES = [
    'https://www.googleapis.com/auth/forms.body',
    'https://www.googleapis.com/auth/spreadsheets',
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]
REDIRECT_URI = "https://formda.streamlit.app/"

# --- Security Initialization ---
@st.cache_resource
def initialize_firebase(config: AppConfig):
    if not firebase_admin._apps:
        cred = credentials.Certificate(config.service_account_info)
        firebase_admin.initialize_app(cred)

@st.cache_resource
def initialize_gemini(config: AppConfig):
    genai.configure(api_key=config.gemini_api_key)
    return genai.GenerativeModel('gemini-pro')

# --- Authentication Services ---
class AuthService:
    def __init__(self, config: AppConfig):
        self.config = config
        self.oauth_client = self._create_oauth_client()
        
    def _create_oauth_client(self):
        return {
            "web": {
                "client_id": self.config.google_client_id,
                "project_id": self.config.google_project_id,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "client_secret": self.config.google_client_secret,
                "redirect_uris": [REDIRECT_URI],
                "scopes": SCOPES
            }
        }

    def get_authorization_url(self):
        auth_url = (
            "https://accounts.google.com/o/oauth2/v2/auth?"
            + urlencode({
                "client_id": self.config.google_client_id,
                "redirect_uri": REDIRECT_URI,
                "scope": " ".join(SCOPES),
                "response_type": "code",
                "access_type": "offline",
                "prompt": "consent",
                "state": st.experimental_user["session_id"]
            })
        )
        return auth_url

    async def exchange_code(self, code: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "code": code,
                    "client_id": self.config.google_client_id,
                    "client_secret": self.config.google_client_secret,
                    "redirect_uri": REDIRECT_URI,
                    "grant_type": "authorization_code"
                }
            )
            response.raise_for_status()
            return response.json()

# --- Google Services Integration ---
class GoogleServices:
    def __init__(self, credentials):
        self.credentials = credentials
        
    @property
    def forms_service(self):
        return build('forms', 'v1', credentials=self.credentials)

    @property
    def sheets_service(self):
        return build('sheets', 'v4', credentials=self.credentials)

    @property
    def drive_service(self):
        return build('drive', 'v3', credentials=self.credentials)

# --- Main Application Logic ---
class WorkspaceCreator:
    def __init__(self):
        self.config = load_config()
        initialize_firebase(self.config)
        self.auth_service = AuthService(self.config)
        self.gemini_model = initialize_gemini(self.config)
        
    def _get_google_credentials(self):
        if 'google_credentials' in st.session_state:
            creds = service_account.Credentials.from_service_account_info(
                self.config.service_account_info,
                scopes=SCOPES
            )
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
            return creds
        return None

    async def handle_authentication(self):
        query_params = st.experimental_get_query_params()
        if 'code' in query_params and 'state' in query_params:
            if query_params["state"][0] != st.experimental_user["session_id"]:
                st.error("Invalid session state")
                return
            
            try:
                token_data = await self.auth_service.exchange_code(query_params["code"][0])
                id_token = token_data['id_token']
                
                decoded_token = auth.verify_id_token(id_token)
                user = auth.get_user(decoded_token['uid'])
                
                st.session_state.user = {
                    'uid': user.uid,
                    'email': user.email,
                    'name': user.display_name,
                    'id_token': id_token,
                    'expires_at': datetime.now() + timedelta(seconds=token_data['expires_in'])
                }
                st.experimental_set_query_params()
                st.rerun()
                
            except Exception as e:
                st.error(f"Authentication failed: {str(e)}")
                st.session_state.user = None

    def create_google_form(self, title: str, questions: list):
        try:
            creds = self._get_google_credentials()
            services = GoogleServices(creds)
            
            form = {"info": {"title": title}}
            result = services.forms_service.forms().create(body=form).execute()
            
            requests = [{
                "createItem": {
                    "item": {
                        "title": q["text"],
                        "questionItem": {
                            "question": {
                                "required": q.get("required", False),
                                "textQuestion": {}
                            }
                        }
                    },
                    "location": {"index": i}
                }
            } for i, q in enumerate(questions) if q["text"]]
            
            if requests:
                services.forms_service.forms().batchUpdate(
                    formId=result["formId"],
                    body={"requests": requests}
                ).execute()
                
            services.drive_service.permissions().create(
                fileId=result["formId"],
                body={"role": "writer", "type": "user", "emailAddress": st.session_state.user['email']}
            ).execute()
            
            return f"https://docs.google.com/forms/d/{result['formId']}/edit"
            
        except Exception as e:
            st.error(f"Form creation failed: {str(e)}")
            return None

    def create_google_sheet(self, title: str, headers: list):
        try:
            creds = self._get_google_credentials()
            services = GoogleServices(creds)
            
            spreadsheet = {
                'properties': {'title': title},
                'sheets': [{
                    'properties': {
                        'title': 'Responses',
                        'gridProperties': {
                            'rowCount': 100,
                            'columnCount': len(headers)
                        }
                    }
                }]
            }
            
            spreadsheet = services.sheets_service.spreadsheets().create(body=spreadsheet).execute()
            
            services.sheets_service.spreadsheets().values().update(
                spreadsheetId=spreadsheet['spreadsheetId'],
                range="A1",
                valueInputOption="USER_ENTERED",
                body={"values": [headers]}
            ).execute()
            
            services.drive_service.permissions().create(
                fileId=spreadsheet['spreadsheetId'],
                body={"role": "writer", "type": "user", "emailAddress": st.session_state.user['email']}
            ).execute()
            
            return f"https://docs.google.com/spreadsheets/d/{spreadsheet['spreadsheetId']}/edit"
            
        except Exception as e:
            st.error(f"Sheet creation failed: {str(e)}")
            return None

    def show_auth_sidebar(self):
        with st.sidebar:
            st.header("Authentication")
            if st.session_state.user:
                st.markdown(f"""
                    **Logged in as:**  
                    👤 {st.session_state.user.get('name', 'User')}  
                    📧 {st.session_state.user['email']}  
                    ⏳ Session expires: {st.session_state.user['expires_at'].strftime('%Y-%m-%d %H:%M:%S')}
                """)
                if st.button("🚪 Logout", use_container_width=True):
                    st.session_state.clear()
                    st.rerun()
            else:
                st.subheader("Sign In")
                auth_url = self.auth_service.get_authorization_url()
                st.markdown(f"""
                    <a href="{auth_url}" style="
                        display: inline-block;
                        padding: 0.5rem 1rem;
                        background: #4285F4;
                        color: white;
                        border-radius: 4px;
                        text-decoration: none;
                        font-weight: bold;
                    ">Sign in with Google</a>
                """, unsafe_allow_html=True)

    def show_main_interface(self):
        st.header("📝 Create New Resources")
        with st.form("resource_creator"):
            col1, col2 = st.columns(2)
            with col1:
                form_title = st.text_input("Form Title", "Customer Feedback Form")
            with col2:
                sheet_title = st.text_input("Sheet Title", "Feedback Responses")
            
            st.subheader("❓ Form Questions")
            num_questions = st.slider("Number of Questions", 1, 10, 3)
            
            questions = []
            for i in range(num_questions):
                cols = st.columns([4, 1])
                with cols[0]:
                    text = st.text_input(f"Question {i+1}", key=f"q{i}")
                with cols[1]:
                    required = st.checkbox("Required", key=f"req{i}")
                if text:
                    questions.append({"text": text, "required": required})
            
            if st.form_submit_button("🚀 Create Resources", use_container_width=True):
                if not any(q["text"] for q in questions):
                    st.error("Please add at least one valid question!")
                else:
                    with st.spinner("Creating resources..."):
                        form_url = self.create_google_form(form_title, questions)
                        sheet_url = self.create_google_sheet(sheet_title, 
                                                           ["Timestamp"] + [q["text"] for q in questions])
                        if form_url and sheet_url:
                            st.success("✅ Resources created successfully!")
                            st.markdown(f"""
                                **Form URL**: [Open Form]({form_url})  
                                **Sheet URL**: [Open Sheet]({sheet_url})
                            """)

    def show_chat_interface(self):
        st.header("🤖 AI Assistant")
        
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
            
        for msg in st.session_state.chat_history:
            with st.chat_message(msg['role']):
                st.markdown(msg['content'])
        
        if prompt := st.chat_input("Ask about form/sheet creation..."):
            st.session_state.chat_history.append({'role': 'user', 'content': prompt})
            
            with st.spinner("Generating response..."):
                try:
                    response = self.gemini_model.generate_content(
                        f"You're a Google Workspace expert. Context: {st.session_state.get('form_context', '')} "
                        f"User question: {prompt}"
                    )
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': response.text
                    })
                    st.rerun()
                except Exception as e:
                    st.error(f"AI Error: {str(e)}")

# --- Application Entry Point ---
def main():
    st.set_page_config(
        page_title="Secure Workspace Creator",
        page_icon="🔒",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    app = WorkspaceCreator()
    
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    app.handle_authentication()
    app.show_auth_sidebar()
    
    if st.session_state.user:
        app.show_main_interface()
        app.show_chat_interface()
    else:
        st.info("Please sign in to access the workspace creation tools")

if __name__ == "__main__":
    main()
