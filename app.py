import os
import streamlit as st
import google.generativeai as genai
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

# OAuth configuration
CLIENT_CONFIG = {
    "web": {
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token",
        "redirect_uris": [os.getenv("REDIRECT_URI")]
    }
}
SCOPES = [
    'https://www.googleapis.com/auth/forms.body',
    'https://www.googleapis.com/auth/spreadsheets'
]

def get_google_auth():
    flow = Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=SCOPES,
        redirect_uri=CLIENT_CONFIG['web']['redirect_uris'][0]
    )
    return flow

# (Keep the existing create_google_form and create_google_sheet functions from previous answer)

def generate_structure(user_input):
    prompt = f"""Convert this user request into JSON structure for Google Form/Sheet creation:
    {user_input}
    
    Return JSON format:
    {{
        "form": {{
            "title": "Form Title",
            "questions": [
                {{
                    "question": "Question text",
                    "type": "textQuestion|choiceQuestion",
                    "required": boolean,
                    "options": ["Option1", "Option2"] (for choiceQuestion)
                }}
            ]
        }},
        "sheet": {{
            "title": "Sheet Title",
            "headers": ["Header1", "Header2"]
        }}
    }}"""
    
    response = model.generate_content(prompt)
    return json.loads(response.text)

def chat_with_ai(prompt):
    response = model.generate_content(prompt)
    return response.text

def main():
    st.title("AI Workspace Creator with Chat")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Authentication
    if 'credentials' not in st.session_state:
        flow = get_google_auth()
        auth_url, _ = flow.authorization_url(prompt='consent')
        st.sidebar.link_button("Login with Google", auth_url)
    else:
        st.sidebar.success("✅ Logged in with Google")
    
    # Chat interface
    with st.container():
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        if prompt := st.chat_input("Ask about form/sheet creation or workspace automation"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                response = chat_with_ai(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Creation interface
    with st.sidebar:
        st.header("Create Resources")
        user_input = st.text_area("Describe what you want to create")
        
        if st.button("Create Now"):
            with st.spinner("Generating..."):
                try:
                    structure = generate_structure(user_input)
                    creds = Credentials(**st.session_state.credentials)
                    results = {}
                    
                    if 'form' in structure:
                        forms_service = build('forms', 'v1', credentials=creds)
                        form_url = create_google_form(forms_service, structure['form'])
                        results['form'] = form_url
                    
                    if 'sheet' in structure:
                        sheets_service = build('sheets', 'v4', credentials=creds)
                        sheet_url = create_google_sheet(sheets_service, structure['sheet'])
                        results['sheet'] = sheet_url
                    
                    st.success("Resources created successfully!")
                    if 'form' in results:
                        st.markdown(f"**Form URL**: [Open Form]({results['form']})")
                    if 'sheet' in results:
                        st.markdown(f"**Sheet URL**: [Open Sheet]({results['sheet']})")
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
