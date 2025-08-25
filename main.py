import streamlit as st
import cv2
import tempfile
import ExerciseAiTrainer as exercise
from chatbot import run_chatbot
import time
import json 
import os 
import hashlib

st.set_page_config(page_title='FitX AI Trainer', layout='centered')

# Utility functions for user authentication
def get_user_data():
    if os.path.exists("users.json"):
        try:
            with open("users.json", "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_user_data(data):
    with open("users.json", "w") as f:
        json.dump(data, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    users = get_user_data()
    if username in users and users[username]["password"] == hash_password(password):
        return True
    return False

def create_user(username, password):
    users = get_user_data()
    if username in users:
        return False
    users[username] = {
        "password": hash_password(password),
        "created_at": time.time()
    }
    save_user_data(users)
    return True

# Login/signup UI
def login_signup():
    st.title("Welcome to FitX AI Trainer 👋")
    
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.image("logo.png", width=350)
    st.markdown("</div>", unsafe_allow_html=True)
    
    option = st.radio("Choose Option", ["Login", "Sign Up"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if option == "Login":
        if st.button("Login"):
            if authenticate_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
            else:
                st.error("Invalid username or password.")
    else:
        if st.button("Sign Up"):
            if create_user(username, password):
                st.success("Account created. Please login.")
            else:
                st.error("Username already exists.")
    
    st.markdown("<hr><center><small>© 2025 FitX AI - Douaa Fajr 💎 </small></center>", unsafe_allow_html=True)

# Main app
def main_app():
    st.title(f"FitX AI Trainer - Hello {st.session_state.username}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()

    options = st.sidebar.selectbox('Select Option', ('Video', 'WebCam', 'Auto Classify', 'chatbot'))

    if options == 'chatbot':
        st.markdown("-------")
        st.markdown("The chatbot is here to assist you")
        run_chatbot()

    elif options == 'Video':
        st.markdown("-------")
        st.write('## Upload your video and select the correct type of Exercise to count repetitions')
        st.write("Ensure you are clearly visible and facing the camera directly.")

        exercise_options = st.sidebar.selectbox('Select Exercise', ('Bicept Curl', 'Push Up', 'Squat', 'Shoulder Press'))
        video_file = st.sidebar.file_uploader("Upload a video", type=["mp4", "mov", 'avi', 'asf', 'm4v'])

        if video_file:
            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(video_file.read())
            cap = cv2.VideoCapture(tfile.name)

            st.sidebar.video(tfile.name)
            st.markdown('-------')
            st.video(tfile.name)

            st.markdown('## Output Video')

            exer = exercise.Exercise()
            if exercise_options == 'Bicept Curl':
                exer.bicept_curl(cap, is_video=True, counter=0, stage_right=None, stage_left=None)
            elif exercise_options == 'Push Up':
                st.write("Film showing your left side or facing frontally")
                exer.push_up(cap, is_video=True, counter=0, stage=None)
            elif exercise_options == 'Squat':
                exer.squat(cap, is_video=True, counter=0, stage=None)
            elif exercise_options == 'Shoulder Press':
                exer.shoulder_press(cap, is_video=True, counter=0, stage=None)

    elif options == 'Auto Classify':
        st.markdown("-------")
        st.write('Click to start automatic classification and repetition counting')
        if st.button('Start Auto Classification'):
            time.sleep(2)
            exer = exercise.Exercise()
            exer.auto_classify_and_count()

    elif options == 'WebCam':
        st.markdown("-------")
        exercise_general = st.sidebar.selectbox('Select Exercise', ('Bicept Curl', 'Push Up', 'Squat', 'Shoulder Press'))

        if st.button('Start Exercise'):
            cap = cv2.VideoCapture(0)
            exer = exercise.Exercise()

            if exercise_general == 'Bicept Curl':
                exer.bicept_curl(cap, counter=0, stage_right=None, stage_left=None)
            elif exercise_general == 'Push Up':
                exer.push_up(cap, counter=0, stage=None)
            elif exercise_general == 'Squat':
                exer.squat(cap, counter=0, stage=None)
            elif exercise_general == 'Shoulder Press':
                exer.shoulder_press(cap, counter=0, stage=None)

if __name__ == '__main__':
    # Load custom CSS if exists
    if os.path.exists("static/styles.css"):
        with open("static/styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        main_app()
    else:
        login_signup()
