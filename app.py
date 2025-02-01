import os
import streamlit as st
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, auth
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import requests
import json

# Firebase Configuration (Embedded in the code)
FIREBASE_CONFIG = {
    "apiKey": "AIzaSyCadZIoYzIc_QhEkGjv86G4rjFwMASd5ig",
    "authDomain": "nothing-d3af4.firebaseapp.com",
    "databaseURL": "https://nothing-d3af4-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "nothing-d3af4",
    "storageBucket": "nothing-d3af4.firebasestorage.app",
    "messagingSenderId": "7155955115",
    "appId": "1:7155955115:web:3bd80618f9aff1a4dc8eee",
    "measurementId": "G-XSVGL2M8LL"
}

# Initialize Firebase Admin
if not firebase_admin._apps:
    cred = credentials.Certificate({
        "project_id": FIREBASE_CONFIG["projectId"],
        "private_key": os.environ.get("FIREBASE_PRIVATE_KEY", "").replace('\\n', '\n'),
        "client_email": f'firebase-adminsdk-{FIREBASE_CONFIG["projectId"]}@appspot.gserviceaccount.com',
        "token_uri": "https://oauth2.googleapis.com/token",
    })
    firebase_admin.initialize_app(cred)

# Configure Gemini
genai.configure(api_key="AIzaSyDpaOZq0jE6d4SdTpf1GyNk_lLkB75Kn_8")
model = genai.GenerativeModel('gemini-pro')

# Firebase Sign-In Function
def firebase_sign_in(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_CONFIG['apiKey']}"
    data = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    response = requests.post(url, json=data)
    return response.json()

# Google API Scopes
SCOPES = [
    'https://www.googleapis.com/auth/forms.body',
    'https://www.googleapis.com/auth/spreadsheets'
]

# Create Google Form
def create_google_form(service, title, questions):
    form = {"info": {"title": title, "documentTitle": title}}
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
            formId=result["formId"], body={"requests": requests}
        ).execute()
    
    return f"https://docs.google.com/forms/d/{result['formId']}/edit"

# Create Google Sheet
def create_google_sheet(service, title, headers):
    spreadsheet = {
        'properties': {'title': title},
        'sheets': [{
            'properties': {
                'title': 'Sheet1',
                'gridProperties": {'rowCount': 100, 'columnCount': len(headers)}
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

# Main Application
def main():
    st.title("🔥 Complete Workspace Creator")
    
    # Initialize session state
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'google_creds' not in st.session_state:
        st.session_state.google_creds = None
    
    # Authentication sidebar
    with st.sidebar:
        st.header("Authentication")
        if st.session_state.user:
            st.markdown(f"""
                **Logged in as:**
                - Email: {st.session_state.user['email']}
            """)
            if st.button("Logout"):
                st.session_state.user = None
                st.session_state.google_creds = None
                st.experimental_rerun()
        else:
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                result = firebase_sign_in(email, password)
                if 'error' in result:
                    st.error("Login failed: " + result['error']['message'])
                else:
                    st.session_state.user = {
                        'email': result['email'],
                        'idToken': result['idToken']
                    }
                    st.experimental_rerun()
    
    # Main interface
    if st.session_state.user:
        # Create Google services using Firebase token
        google_creds = Credentials(st.session_state.user['idToken'])
        forms_service = build('forms', 'v1', credentials=google_creds)
        sheets_service = build('sheets', 'v4', credentials=google_creds)
        
        # Creation interface
        st.header("Create New Resource")
        form_title = st.text_input("Form Title", "Customer Feedback Form")
        sheet_title = st.text_input("Sheet Title", "Feedback Responses")
        
        if st.button("Create Resources"):
            form_url = create_google_form(
                forms_service,
                form_title,
                [{"text": "What is your name?", "required": True}]
            )
            sheet_url = create_google_sheet(
                sheets_service,
                sheet_title,
                ["Timestamp", "Name", "Feedback"]
            )
            
            st.success("Resources created successfully!")
            st.markdown(f"**Form URL**: [Open Form]({form_url})")
            st.markdown(f"**Sheet URL**: [Open Sheet]({sheet_url})")
    
    # Chat interface
    if st.session_state.user:
        st.header("AI Assistant")
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        
        if prompt := st.chat_input("Ask about form/sheet creation..."):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            response = model.generate_content(prompt).text
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.experimental_rerun()

if __name__ == "__main__":
    main()
