import streamlit as st
import pyrebase
import json
from datetime import datetime

# Initialize session state for user authentication
if 'user' not in st.session_state:
    st.session_state.user = None

# Firebase Configuration
firebaseConfig = {
    "apiKey": "AIzaSyC6YllFBzRnUjFfIJhGjIkwMlGELuKs9YQ",
    "authDomain": "nothing-d3af4.firebaseapp.com",
    "projectId": "nothing-d3af4",
    "storageBucket": "nothing-d3af4.firebasestorage.app",
    "messagingSenderId": "7155955115",
    "appId": "1:7155955115:web:62e7e9a543ba2f77dc8eee",
    "databaseURL": "https://nothing-d3af4-default-rtdb.asia-southeast1.firebasedatabase.app/"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

# Create the Streamlit app
def main():
    st.title("Firebase Authentication & Database Demo")
    
    # Sidebar menu
    menu = ["Login", "Sign Up", "Home", "Profile"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Login":
        st.subheader("Login")
        
        email = st.text_input("Email")
        password = st.text_input("Password", type='password')
        
        if st.button("Login"):
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                st.session_state.user = user
                
                # Get user profile data from database
                user_data = db.child("users").child(user['localId']).get()
                if user_data.val() is None:
                    # Create user profile if it doesn't exist
                    user_profile = {
                        "email": email,
                        "joined_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "last_login": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    db.child("users").child(user['localId']).set(user_profile)
                else:
                    # Update last login
                    db.child("users").child(user['localId']).update(
                        {"last_login": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                    )
                
                st.success("Logged in successfully!")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
                
    elif choice == "Sign Up":
        st.subheader("Create New Account")
        
        email = st.text_input("Email")
        password = st.text_input("Password", type='password')
        confirm_password = st.text_input("Confirm Password", type='password')
        
        if st.button("Sign Up"):
            if password == confirm_password:
                try:
                    user = auth.create_user_with_email_and_password(email, password)
                    
                    # Create user profile in database
                    user_profile = {
                        "email": email,
                        "joined_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "last_login": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    db.child("users").child(user['localId']).set(user_profile)
                    
                    st.success("Account created successfully!")
                    st.info("Please login with your new credentials")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.error("Passwords do not match")
                
    elif choice == "Home":
        if st.session_state.user is not None:
            st.subheader("Welcome to the Home Page")
            user_data = db.child("users").child(st.session_state.user['localId']).get().val()
            
            st.write(f"Logged in as: {user_data['email']}")
            st.write(f"Joined on: {user_data['joined_date']}")
            st.write(f"Last login: {user_data['last_login']}")
            
            # Add a note feature
            st.subheader("Add a Note")
            note_text = st.text_area("Write your note")
            if st.button("Save Note"):
                note = {
                    "text": note_text,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                db.child("users").child(st.session_state.user['localId']).child("notes").push(note)
                st.success("Note saved!")
            
            # Display all notes
            st.subheader("Your Notes")
            notes = db.child("users").child(st.session_state.user['localId']).child("notes").get()
            if notes.val():
                for note in notes.each():
                    with st.expander(f"Note from {note.val()['timestamp']}"):
                        st.write(note.val()['text'])
                        if st.button("Delete", key=note.key()):
                            db.child("users").child(st.session_state.user['localId']).child("notes").child(note.key()).remove()
                            st.success("Note deleted!")
                            st.experimental_rerun()
            
            if st.button("Logout"):
                st.session_state.user = None
                st.experimental_rerun()
        else:
            st.warning("Please login to access this page")
            st.info("Go to the Login page from the sidebar menu")
            
    elif choice == "Profile":
        if st.session_state.user is not None:
            st.subheader("Profile Settings")
            user_data = db.child("users").child(st.session_state.user['localId']).get().val()
            
            # Display and edit profile information
            new_name = st.text_input("Name", user_data.get('name', ''))
            new_bio = st.text_area("Bio", user_data.get('bio', ''))
            
            if st.button("Update Profile"):
                updates = {
                    "name": new_name,
                    "bio": new_bio
                }
                db.child("users").child(st.session_state.user['localId']).update(updates)
                st.success("Profile updated successfully!")
        else:
            st.warning("Please login to access this page")
            st.info("Go to the Login page from the sidebar menu")

if __name__ == '__main__':
    main()
