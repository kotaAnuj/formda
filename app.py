import streamlit as st
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import webbrowser
import os

# Firebase configuration
firebase_config = {
    "apiKey": "AIzaSyC6YllFBzRnUjFfIJhGjIkwMlGELuKs9YQ",
    "authDomain": "nothing-d3af4.firebaseapp.com",
    "projectId": "nothing-d3af4",
    "storageBucket": "nothing-d3af4.firebasestorage.app",
    "messagingSenderId": "7155955115",
    "appId": "1:7155955115:web:62e7e9a543ba2f77dc8eee"
}

# Create HTML file content
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Firebase Auth</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f5f5f5;
        }}
        .container {{
            text-align: center;
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        button {{
            background-color: #4285f4;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            margin: 10px;
        }}
        button:hover {{
            background-color: #357abd;
        }}
        #status {{
            margin: 20px 0;
            padding: 10px;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h2>Firebase Authentication</h2>
        <div id="status"></div>
        <button id="loginBtn">Login with Google</button>
        <button id="logoutBtn" style="display: none;">Logout</button>
    </div>

    <script src="https://www.gstatic.com/firebasejs/9.22.1/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.22.1/firebase-auth-compat.js"></script>

    <script>
        const firebaseConfig = {json.dumps(firebase_config)};
        firebase.initializeApp(firebaseConfig);

        const auth = firebase.auth();
        const loginBtn = document.getElementById('loginBtn');
        const logoutBtn = document.getElementById('logoutBtn');
        const status = document.getElementById('status');

        loginBtn.addEventListener('click', () => {{
            const provider = new firebase.auth.GoogleAuthProvider();
            auth.signInWithPopup(provider)
                .then((result) => {{
                    console.log('Login successful');
                    status.style.backgroundColor = '#e8f5e9';
                    status.style.color = '#2e7d32';
                    status.textContent = `Logged in as: ${{result.user.email}}`;
                }})
                .catch((error) => {{
                    console.error('Login error:', error);
                    status.style.backgroundColor = '#ffebee';
                    status.style.color = '#c62828';
                    status.textContent = `Error: ${{error.message}}`;
                }});
        }});

        logoutBtn.addEventListener('click', () => {{
            auth.signOut().then(() => {{
                console.log('Logged out');
                status.style.backgroundColor = '#e3f2fd';
                status.style.color = '#1976d2';
                status.textContent = 'Please log in';
            }}).catch((error) => {{
                console.error('Logout error:', error);
                status.textContent = `Error: ${{error.message}}`;
            }});
        }});

        auth.onAuthStateChanged((user) => {{
            if (user) {{
                status.style.backgroundColor = '#e8f5e9';
                status.style.color = '#2e7d32';
                status.textContent = `Logged in as: ${{user.email}}`;
                loginBtn.style.display = 'none';
                logoutBtn.style.display = 'inline-block';
            }} else {{
                status.style.backgroundColor = '#e3f2fd';
                status.style.color = '#1976d2';
                status.textContent = 'Please log in';
                loginBtn.style.display = 'inline-block';
                logoutBtn.style.display = 'none';
            }}
        }});
    </script>
</body>
</html>
"""

# Write the HTML file
with open("login.html", "w") as f:
    f.write(html_content)

class CustomHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)

    def do_GET(self):
        if self.path == '/':
            self.path = '/login.html'
        return SimpleHTTPRequestHandler.do_GET(self)

def run_server():
    server = HTTPServer(('127.0.0.1', 8000), CustomHandler)
    print("Server started at http://127.0.0.1:8000")
    server.serve_forever()

# Start the server in a separate thread
server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

# Streamlit UI
st.title("Firebase Authentication")
st.write("Please use the authentication page that opened in a new tab.")
st.info("If the page didn't open automatically, [click here](http://127.0.0.1:8000)")

# Open the browser automatically
webbrowser.open('http://127.0.0.1:8000')

# Keep the Streamlit app running
st.write("You can close this window after you're done.")
