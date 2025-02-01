import os
import streamlit as st
import google.generativeai as genai
import pyrebase
import json
from datetime import datetime
from googleapiclient.discovery import build
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials

# Load environment variables
load_dotenv()

# Configure Firebase
firebase_config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": "nothing-d3af4.firebaseapp.com",
    "databaseURL": "https://nothing-d3af4-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "nothing-d3af4",
    "storageBucket": "nothing-d3af4.firebasestorage.app",
    "messagingSenderId": "7155955115",
    "appId": "1:7155955115:web:3bd80618f9aff1a4dc8eee",
    "measurementId": "G-XSVGL2M8LL"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# Service scopes
SCOPES = [
    'https://www.googleapis.com/auth/forms.body',
    'https://www.googleapis.com/auth/spreadsheets'
]

def get_google_credentials(id_token):
    return Credentials(
        token=id_token,
        scopes=SCOPES,
        token_uri='https://oauth2.googleapis.com/token'
    )

def create_google_form(creds, form_details):
    try:
        service = build('forms', 'v1', credentials=creds)
        form = {
            'info': {
                'title': form_details['title'],
                'documentTitle': form_details['title']
            }
        }
        result = service.forms().create(body=form).execute()
        
        requests = []
        for i, item in enumerate(form_details['items']):
            request = {
                "createItem": {
                    "item": {
                        "title": item['question'],
                        "questionItem": {
                            "question": {
                                "required": item.get('required', False),
                                item['type']: {}
                            }
                        }
                    },
                    "location": {"index": i}
                }
            }
            if item['type'] == 'choiceQuestion' and 'options' in item:
                request["createItem"]["item"]["questionItem"]["question"]["choiceQuestion"]["options"] = [
                    {"value": opt} for opt in item['options']
                ]
            requests.append(request)
        
        if requests:
            service.forms().batchUpdate(
                formId=result['formId'], body={'requests': requests}
            ).execute()
        
        return f"https://docs.google.com/forms/d/{result['formId']}/edit"
    except Exception as e:
        st.error(f"Form creation failed: {str(e)}")
        return None

def create_google_sheet(creds, sheet_details):
    try:
        service = build('sheets', 'v4', credentials=creds)
        spreadsheet = {
            'properties': {
                'title': sheet_details['title'],
                'locale': 'en_US',
                'timeZone': 'UTC'
            }
        }
        spreadsheet = service.spreadsheets().create(body=spreadsheet).execute()
        
        if 'headers' in sheet_details:
            body = {
                'values': [sheet_details['headers']]
            }
            service.spreadsheets().values().update(
                spreadsheetId=spreadsheet['spreadsheetId'],
                range="A1",
                valueInputOption="USER_ENTERED",
                body=body
            ).execute()
        
        return f"https://docs.google.com/spreadsheets/d/{spreadsheet['spreadsheetId']}/edit"
    except Exception as e:
        st.error(f"Sheet creation failed: {str(e)}")
        return None

def ai_chat(prompt, user_email):
    response = model.generate_content(f"User {user_email} asks: {prompt}")
    return response.text

def main():
    st.title("🔥 Smart Workspace Creator")
    
    # Initialize session state
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Authentication sidebar
    with st.sidebar:
        st.header("Authentication")
        if st.session_state.user:
            user = st.session_state.user
            st.markdown(f"""
                **Logged in as:**
                - Name: {user['displayName']}
                - Email: {user['email']}
            """)
            if st.button("Logout"):
                st.session_state.user = None
                st.experimental_rerun()
        else:
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                try:
                    user = auth.sign_in_with_email_and_password(email, password)
                    st.session_state.user = auth.get_account_info(user['idToken'])['users'][0]
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Login failed: {str(e)}")
            
            if st.button("Google Sign-In"):
                try:
                    redirect_url = "http://localhost:8501/"
                    provider = auth.GoogleAuthProvider()
                    st.session_state.provider = provider
                    st.session_state.redirect_url = redirect_url
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Google Sign-In failed: {str(e)}")

    # Main interface
    if st.session_state.user:
        user_email = st.session_state.user['email']
        
        # Chat interface
        st.header("AI Assistant Chat")
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        
        if prompt := st.chat_input("Ask about form/sheet creation..."):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                response = ai_chat(prompt, user_email)
                st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        # Creation interface
        st.header("Create New Resource")
        col1, col2 = st.columns(2)
        
        with col1:
            with st.form("form_creator"):
                st.subheader("Create Google Form")
                form_title = st.text_input("Form Title", value=f"{user_email.split('@')[0]} Survey")
                questions = st.text_area("Enter questions (one per line)")
                if st.form_submit_button("Create Form"):
                    try:
                        creds = get_google_credentials(st.session_state.user['idToken'])
                        form_details = {
                            "title": form_title,
                            "items": [{"question": q, "type": "textQuestion"} for q in questions.split('\n') if q]
                        }
                        form_url = create_google_form(creds, form_details)
                        if form_url:
                            st.success(f"Form created: [Open Form]({form_url})")
                    except Exception as e:
                        st.error(f"Error creating form: {str(e)}")
        
        with col2:
            with st.form("sheet_creator"):
                st.subheader("Create Google Sheet")
                sheet_title = st.text_input("Sheet Title", value=f"{user_email.split('@')[0]} Data")
                headers = st.text_input("Headers (comma separated)")
                if st.form_submit_button("Create Sheet"):
                    try:
                        creds = get_google_credentials(st.session_state.user['idToken'])
                        sheet_details = {
                            "title": sheet_title,
                            "headers": [h.strip() for h in headers.split(',') if h]
                        }
                        sheet_url = create_google_sheet(creds, sheet_details)
                        if sheet_url:
                            st.success(f"Sheet created: [Open Sheet]({sheet_url})")
                    except Exception as e:
                        st.error(f"Error creating sheet: {str(e)}")

    else:
        st.markdown("""
            ## Welcome to Smart Workspace Creator!
            Please login using your Google account or email/password in the sidebar to:
            - Create custom Google Forms
            - Generate organized Google Sheets
            - Get AI assistance for workspace automation
        """)

if __name__ == "__main__":
    main()
