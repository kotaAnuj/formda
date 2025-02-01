import os
import streamlit as st
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, auth
from googleapiclient.discovery import build
from google.oauth2 import service_account
from google_auth_oauthlib.flow import Flow
import requests
import json
from datetime import datetime
from urllib.parse import urlencode


FIREBASE_CONFIG = {
    "type": "service_account",
    "project_id": "nothing-d3af4",
    "private_key_id": "12b049fdbd855a5565d36af20d474f1deea00441",
    "private_key": """-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCPt3slddDnofon
9mC6MRXP4lpxtfy/caRfGpVnHM+SExYhxSIkLMvsbDH3A2bOENrHL7PIphh7xQ0O
MtWjBUoONnPIl+Jq8XyZaB847jfK101Kuc8TKaAMwucYBAgbYgc/8t0/84y6pbtN
KlJJ2UudDhA6AiLB4I/BM6swUo7bjDlklWpuDpm5Wjjb1e/gtmR/3O8Ean/anpHG
mydeg3iNZnZ6CQfjjWmk9PULVepBofYzCIsgB5R4oibp8jCyZr6Fvz7X4DPEIL1Y
KgddPe6CpX82SF4ikhuW8F5Eq9hl1ufNvPe8/OdPA58wsBzp7+L386aefmAMssdi
rTVKGixNAgMBAAECggEAQ1s3pK1srPst7qfa2rjho65PPGcSX7mH06j2Z77JjAlV
AJvPbgvuwU5ONpqKBr9AgkVZqgsqg2utvD9YAFEczb94kYWZ8QxgHNf/diOz02YI
DCM8qZsDL6fzPj65e/f8NN0DFBN2HA5L1BUnPwRQG3o5Ya6ZkqtIRMEOFRZEbSG9
/RtzVXWl6L6sHJN65QLphBrDnBpQKeW9XEPbGvFVb/s0IDcl8oeTburts1Bu5Hqm
wtN/minQ+edtEx8tniLzL7cZL9dNpa1nWKKiYlneScI08f+kKh/K4kdyZ6qAGfB7
LuFZ60IYNJuWCyqjL5eawvfCk7FHlCIpNKdYJygMYwKBgQDCxDEwbGeDgKserMmi
BUvRAa1gkOOloaARVl186W/nsCxz6mqvuirKodHoZliI3+1iVutUXHyT0nLYWS9M
ZFsFgpiG4aReamGSRZ/t53ly4ctMnU/l6U705zD/zYWB1b/cypkdUQC4UUq9OWBd
2bVNMEebq/2OlQzdNH5gdTN/jwKBgQC85oxSCSVF5m8LSbFf19enhl4y8XIji0tk
57tJC3QAeDTarCl/KnfyBkN2JClUuOJrd3J8P2dJrclmhdMCQ9TLmNRB4N5AzMAs
IFzK62MFixYxNljabGDklaY3y9vZmWYmQDC8Zlvxl8nFefiGxilSPpXKBG+p2Hsr
Dc+k3+aoYwKBgFfi+iNUt30ioZUM+UuQQj8FF7xchS0nerh4FWWZXPLaj6Sa4ht7
0XVwgezxyf+xtEfM2xJNTbXSoBo6XFqHan9ZCATNa0Njk7XSjzFmY2pQs1FWJ0ii
+AsRDA5SKm2FC7fRADi3ZbDGlgg/DNostGApaha4DIm7fnuPBXv3Rw7HAoGABcMG
fq4Wu/YWZwK9bU35HvwDPYyNzbW++/nxhX3a8PS5r/3WWjGibPhx8FWUCSiGh36i
OFX6wY2SehUU5ZnKENe9ibDhNprINdBa5Dmf0Jh4edHNjgQGRJKn+kW2lAGQ0xPc
KLL6lPjrR6G7yeibdA3CpeHSwhx/TUXjkoTd1T8CgYBlr5TLHAH0QrYlXQVN7LaG
yIlOfvTdbMO4dbu/ziy6WmOfgk9mcpGc7BxoApD1+biZXPHEM1+xoDKS4chzpRQm
KRqCwM9I4pxCs+knGhP7TL/4v4LIT+qhTbd9POCzCZt05EsDdd+lGtW+CHkG8noV
aLbRpRTr3I34yE6mleATLA==
-----END PRIVATE KEY-----""",
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
    "databaseURL": "https://nothing-d3af4-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "nothing-d3af4",
    "storageBucket": "nothing-d3af4.firebasestorage.app",
    "messagingSenderId": "7155955115",
    "appId": "1:7155955115:web:3bd80618f9aff1a4dc8eee",
    "measurementId": "G-XSVGL2M8LL"
}

GOOGLE_OAUTH_CONFIG = {
    "web": {
        "client_id": "YOUR_GOOGLE_OAUTH_CLIENT_ID",
        "project_id": "nothing-d3af4",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "YOUR_GOOGLE_OAUTH_CLIENT_SECRET",
        "redirect_uris": ["https://formda.streamlit.app/"],
        "javascript_origins": ["https://formda.streamlit.app"]
    }
}

GEMINI_API_KEY = "AIzaSyDpaOZq0jE6d4SdTpf1GyNk_lLkB75Kn_8"

SCOPES = [
    'https://www.googleapis.com/auth/forms.body',
    'https://www.googleapis.com/auth/spreadsheets',
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]


@st.cache_resource
def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(FIREBASE_CONFIG)
        return firebase_admin.initialize_app(cred)
    return firebase_admin.get_app()

@st.cache_resource
def initialize_gemini():
    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel('gemini-pro')


def get_google_flow():
    return Flow.from_client_config(
        client_config=GOOGLE_OAUTH_CONFIG,
        scopes=SCOPES,
        redirect_uri=GOOGLE_OAUTH_CONFIG['web']['redirect_uris'][0]
    )

def google_sign_in():
    flow = get_google_flow()
    auth_url, _ = flow.authorization_url(prompt='consent')
    st.markdown(f"""
        <a href="{auth_url}" target="_self" style="
            display: inline-block;
            padding: 0.5rem 1rem;
            background: #4285F4;
            color: white;
            border-radius: 4px;
            text-decoration: none;
            font-weight: bold;
        ">Sign in with Google</a>
    """, unsafe_allow_html=True)

def handle_oauth_callback():
    flow = get_google_flow()
    code = st.experimental_get_query_params().get('code')
    if code:
        try:
            flow.fetch_token(code=code[0])
            id_token = flow.credentials.id_token
            decoded_token = auth.verify_id_token(id_token)
            user = auth.get_user(decoded_token['uid'])
            st.session_state.user = {
                'uid': user.uid,
                'email': user.email,
                'name': user.display_name,
                'idToken': id_token,
                'expires': flow.credentials.expiry.timestamp()
            }
            # Clear query params after successful login
            st.experimental_set_query_params()
        except Exception as e:
            st.error(f"Google authentication failed: {str(e)}")
            st.session_state.user = None


def firebase_sign_in(email, password):
    try:
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_CONFIG['apiKey']}"
        response = requests.post(url, json={
            "email": email,
            "password": password,
            "returnSecureToken": True
        })
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Login failed: {str(e)}")
        return None


def get_google_services():
    creds = service_account.Credentials.from_service_account_info(
        FIREBASE_CONFIG,
        scopes=SCOPES
    )
    return (
        build('forms', 'v1', credentials=creds),
        build('sheets', 'v4', credentials=creds)
    )

def create_google_form(service, title, questions):
    form = {"info": {"title": title}}
    result = service.forms().create(body=form).execute()
    
    requests_list = [{
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
    
    if requests_list:
        service.forms().batchUpdate(
            formId=result["formId"],
            body={"requests": requests_list}
        ).execute()
    
    drive = build('drive', 'v3', credentials=service._credentials)
    drive.permissions().create(
        fileId=result["formId"],
        body={"role": "reader", "type": "anyone"}
    ).execute()
    
    return f"https://docs.google.com/forms/d/{result['formId']}/edit"

def create_google_sheet(service, title, headers):
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
    
    spreadsheet = service.spreadsheets().create(body=spreadsheet).execute()
    
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet['spreadsheetId'],
        range="A1",
        valueInputOption="USER_ENTERED",
        body={"values": [headers]}
    ).execute()
    
    drive = build('drive', 'v3', credentials=service._credentials)
    drive.permissions().create(
        fileId=spreadsheet['spreadsheetId'],
        body={"role": "writer", "type": "anyone"}
    ).execute()
    
    return f"https://docs.google.com/spreadsheets/d/{spreadsheet['spreadsheetId']}/edit"


def main():
    st.set_page_config(
        page_title="Complete Workspace Creator",
        page_icon="🔥",
        layout="wide"
    )
    
    initialize_firebase()
    model = initialize_gemini()
    
    # Handle OAuth callback if present
    handle_oauth_callback()
    
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    st.title("🔥 Complete Workspace Creator")
    
    # Authentication Sidebar
    with st.sidebar:
        st.header("Authentication")
        if st.session_state.user:
            st.markdown(f"""
                **Logged in as:**
                - Email: {st.session_state.user['email']}
                - Session expires: {datetime.fromtimestamp(int(st.session_state.user.get('expires', 0)))}
            """)
            if st.button("Logout", type="primary"):
                st.session_state.user = None
                st.session_state.chat_history = []
                st.rerun()
        else:
            # Option for Google Sign-In
            google_sign_in()
            st.info("Or, login with Email/Password below:")
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                if st.form_submit_button("Login", type="primary"):
                    if not email or not password:
                        st.error("Please enter both email and password")
                    else:
                        with st.spinner("Logging in..."):
                            result = firebase_sign_in(email, password)
                            if result and 'idToken' in result:
                                st.session_state.user = {
                                    'email': result['email'],
                                    'idToken': result['idToken'],
                                    'expiresIn': result['expiresIn']
                                }
                                st.rerun()
    
    # Main Interface
    if st.session_state.user:
        try:
            forms_service, sheets_service = get_google_services()
            
            # Resource Creation Section
            st.header("Create New Resource")
            with st.form("resource_form"):
                col1, col2 = st.columns(2)
                with col1:
                    form_title = st.text_input("Form Title", "Customer Feedback Form")
                with col2:
                    sheet_title = st.text_input("Sheet Title", "Feedback Responses")
                
                st.subheader("Form Questions")
                num_questions = st.number_input("Number of questions", 1, 10, 3)
                
                questions = []
                for i in range(num_questions):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        question_text = st.text_input(f"Question {i+1}", key=f"q_{i}")
                    with col2:
                        required = st.checkbox("Required", key=f"req_{i}")
                    if question_text:
                        questions.append({"text": question_text, "required": required})
                
                if st.form_submit_button("Create Resources", type="primary"):
                    if not questions:
                        st.error("Please add at least one question")
                    else:
                        with st.spinner("Creating resources..."):
                            form_url = create_google_form(forms_service, form_title, questions)
                            sheet_url = create_google_sheet(sheets_service, sheet_title, 
                                                          ["Timestamp"] + [q["text"] for q in questions])
                            if form_url and sheet_url:
                                st.success("Resources created successfully!")
                                st.markdown(f"""
                                    **Form URL**: [Open Form]({form_url})  
                                    **Sheet URL**: [Open Sheet]({sheet_url})
                                """)
            
            # AI Chat Interface
            st.header("AI Assistant")
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
            
            if prompt := st.chat_input("Ask about form/sheet creation..."):
                with st.spinner("Generating response..."):
                    st.session_state.chat_history.append({"role": "user", "content": prompt})
                    context = (
                        "You are an AI assistant helping users create Google Forms and Sheets.\n"
                        "You can help with form design, question formatting, and best practices."
                    )
                    response = model.generate_content(f"{context}\n\nUser: {prompt}")
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response.text
                    })
                    st.rerun()
                    
        except Exception as e:
            st.error(f"System error: {str(e)}")
            st.info("Please try logging out and back in again.")

if __name__ == "__main__":
    main()
