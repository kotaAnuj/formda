import os
import streamlit as st
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, auth
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
import requests
import json
from datetime import datetime

# Firebase Configuration
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

# Firebase Web Config
FIREBASE_WEB_CONFIG = {
    "apiKey": "AIzaSyC6YllFBzRnUjFfIJhGjIkwMlGELuKs9YQ",
    "authDomain": "nothing-d3af4.firebaseapp.com",
    "databaseURL": "https://nothing-d3af4-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "nothing-d3af4",
    "storageBucket": "nothing-d3af4.firebasestorage.app",
    "messagingSenderId": "7155955115",
    "appId": "1:7155955115:web:62e7e9a543ba2f77dc8eee",
    "measurementId": "G-JNLGNYK8DM"
}

# Google API configuration
SCOPES = [
    'https://www.googleapis.com/auth/forms.body',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Initialize Firebase Admin
@st.cache_resource
def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(FIREBASE_CONFIG)
        return firebase_admin.initialize_app(cred)
    return firebase_admin.get_app()

# Initialize Gemini
@st.cache_resource
def initialize_gemini():
    genai.configure(api_key="AIzaSyDpaOZq0jE6d4SdTpf1GyNk_lLkB75Kn_8")
    return genai.GenerativeModel('gemini-pro')

def get_google_services():
    """Initialize Google services using service account"""
    credentials = service_account.Credentials.from_service_account_info(
        FIREBASE_CONFIG,
        scopes=SCOPES
    )
    
    forms_service = build('forms', 'v1', credentials=credentials)
    sheets_service = build('sheets', 'v4', credentials=credentials)
    return forms_service, sheets_service

def firebase_sign_in(email, password):
    """Firebase email/password authentication"""
    try:
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_CONFIG['apiKey']}"
        data = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Authentication failed: {str(e)}")
        return None

def create_google_form(service, title, questions):
    """Create a Google Form with error handling"""
    try:
        form = {
            "info": {
                "title": title,
                "documentTitle": title
            }
        }
        result = service.forms().create(body=form).execute()
        
        requests = []
        for i, question in enumerate(questions):
            request = {
                "createItem": {
                    "item": {
                        "title": question["text"],
                        "questionItem": {
                            "question": {
                                "required": question.get("required", False),
                                "textQuestion": {}
                            }
                        }
                    },
                    "location": {"index": i}
                }
            }
            requests.append(request)
        
        if requests:
            service.forms().batchUpdate(
                formId=result["formId"],
                body={"requests": requests}
            ).execute()
        
        return f"https://docs.google.com/forms/d/{result['formId']}/edit"
    except Exception as e:
        st.error(f"Error creating form: {str(e)}")
        return None

def create_google_sheet(service, title, headers):
    """Create a Google Sheet with error handling"""
    try:
        spreadsheet = {
            'properties': {'title': title},
            'sheets': [{
                'properties': {
                    'title': 'Sheet1',
                    'gridProperties': {
                        'rowCount': 100,
                        'columnCount': len(headers)
                    }
                }
            }]
        }
        
        spreadsheet = service.spreadsheets().create(body=spreadsheet).execute()
        
        if headers:
            body = {"values": [headers]}
            service.spreadsheets().values().update(
                spreadsheetId=spreadsheet['spreadsheetId'],
                range="A1",
                valueInputOption="USER_ENTERED",
                body=body
            ).execute()
        
        return f"https://docs.google.com/spreadsheets/d/{spreadsheet['spreadsheetId']}/edit"
    except Exception as e:
        st.error(f"Error creating sheet: {str(e)}")
        return None

def main():
    st.set_page_config(
        page_title="Complete Workspace Creator",
        page_icon="🔥",
        layout="wide"
    )
    
    # Initialize services
    firebase_app = initialize_firebase()
    model = initialize_gemini()
    
    # Initialize session state
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    st.title("🔥 Complete Workspace Creator")
    
    # Authentication sidebar
    with st.sidebar:
        st.header("Authentication")
        if st.session_state.user:
            st.markdown(f"""
                **Logged in as:**
                - Email: {st.session_state.user['email']}
            """)
            if st.button("Logout", type="primary"):
                st.session_state.user = None
                st.session_state.chat_history = []
                st.experimental_rerun()
        else:
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login", type="primary")
                
                if submit:
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
                                st.experimental_rerun()
    
    # Main interface
    if st.session_state.user:
        try:
            # Get Google services
            forms_service, sheets_service = get_google_services()
            
            # Creation interface
            st.header("Create New Resource")
            
            with st.form("resource_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    form_title = st.text_input(
                        "Form Title",
                        "Customer Feedback Form"
                    )
                
                with col2:
                    sheet_title = st.text_input(
                        "Sheet Title",
                        "Feedback Responses"
                    )
                
                # Dynamic question addition
                st.subheader("Form Questions")
                num_questions = st.number_input(
                    "Number of questions",
                    1, 10, 3
                )
                
                questions = []
                for i in range(num_questions):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        question_text = st.text_input(f"Question {i+1}", key=f"q_{i}")
                    with col2:
                        required = st.checkbox("Required", key=f"req_{i}")
                    if question_text:  # Only add non-empty questions
                        questions.append({"text": question_text, "required": required})
                
                submit_button = st.form_submit_button("Create Resources", type="primary")
                
                if submit_button:
                    if not questions:
                        st.error("Please add at least one question")
                    else:
                        with st.spinner("Creating resources..."):
                            form_url = create_google_form(
                                forms_service,
                                form_title,
                                questions
                            )
                            sheet_url = create_google_sheet(
                                sheets_service,
                                sheet_title,
                                ["Timestamp"] + [q["text"] for q in questions]
                            )
                            
                            if form_url and sheet_url:
                                st.success("Resources created successfully!")
                                st.markdown(f"""
                                    **Form URL**: [Open Form]({form_url})  
                                    **Sheet URL**: [Open Sheet]({sheet_url})
                                """)
            
            # Chat interface
            st.header("AI Assistant")
            st.markdown("""
            Ask me anything about:
            - Creating forms and sheets
            - Best practices for survey design
            - Form question types and formatting
            - Data collection strategies
            """)
            
            # Display chat history
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
            
            # Chat input
            if prompt := st.chat_input("Ask about form/sheet creation...", key="chat_input"):
                with st.spinner("Thinking..."):
                    # Add user message to chat history
                    st.session_state.chat_history.append({
                        "role": "user",
                        "content": prompt
                    })
                    
                    # Generate AI response with context
                    context = """You are an AI assistant helping users create Google Forms and Sheets.
                    You can help with form design, question formatting, and best practices.
                    Keep responses clear, concise, and focused on forms and sheets."""
                    
                    full_prompt = f"{context}\n\nUser: {prompt}"
                    response = model.generate_content(full_prompt)
                    
                    # Add AI response to chat history
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response.text
                    })
                    
                    # Rerun to update the chat interface
                    st.experimental_rerun()
                    
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            with st.expander("Error Details"):
                st.code(str(e))
            st.info("Please try logging out and back in again.")

if __name__ == "__main__":
    main()
