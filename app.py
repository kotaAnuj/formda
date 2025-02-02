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
<!-- HTML head and style sections remain the same -->
<body>
    <div class="container">
        <h2>Firebase Authentication</h2>
        <div id="status"></div>
        <button id="loginBtn">Login with Google</button>
    </div>

    <script src="https://www.gstatic.com/firebasejs/9.22.1/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.22.1/firebase-auth-compat.js"></script>

    <script>
        const firebaseConfig = {json.dumps(firebase_config)};
        firebase.initializeApp(firebaseConfig);

        // Rest of the JavaScript code remains the same
    </script>
</body>
</html>
"""

# Write the HTML file
with open("login.html", "w") as f:
    f.write(html_content)

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/login.html'
        return SimpleHTTPRequestHandler.do_GET(self)

def run_server():
    # Changed from 'localhost' to '127.0.0.1'
    server = HTTPServer(('127.0.0.1', 8000), CustomHandler)
    server.serve_forever()

# Start the server in a separate thread
server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

# Streamlit UI
st.title("Firebase Authentication")
st.write("Please use the authentication page that opened in a new tab.")
# Updated URL to use 127.0.0.1
st.info("If the page didn't open automatically, [click here](http://127.0.0.1:8000)")

# Updated URL to use 127.0.0.1
webbrowser.open('http://127.0.0.1:8000')

# Keep the Streamlit app running
st.write("You can close this window after you're done.")
