import streamlit as st
import base64
import speech_recognition as sr

def get_voice_text():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            st.info("🎙 Listening... Please speak clearly")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        text = recognizer.recognize_google(audio)
        return text

    except sr.UnknownValueError:
        return ""

    except sr.RequestError:
        return ""

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------
st.set_page_config(
    page_title="Legal AI Assistant",
    page_icon="⚖️",
    layout="wide"
)

# ---------------------------------------
# LOAD BACKGROUND IMAGE
# ---------------------------------------
def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg_image = get_base64_image(
    r"C:\Users\Anuradha kumari\OneDrive\Desktop\header.jpg"
)

# ---------------------------------------
# SESSION STATE
# ---------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

# ---------------------------------------
# THEME COLORS
# ---------------------------------------
if st.session_state.theme == "Dark":
    bg_color = "rgba(15,15,20,0.88)"
    text_color = "white"
else:
    bg_color = "rgba(255,255,255,0.8)"
    text_color = "#1f2a44"

# ---------------------------------------
# CSS
# ---------------------------------------
st.markdown(f"""
<style>

body {{
    background-image: url("data:image/jpg;base64,{bg_image}");
    background-size: cover;
    background-attachment: fixed;
}}

.main {{
    background-color: {bg_color};
    padding: 25px;
    border-radius: 14px;
}}

h1,h2,h3,p,label {{
    color: {text_color};
}}

section[data-testid="stSidebar"] {{
    background-color: #1f2a44;
}}

section[data-testid="stSidebar"] * {{
    color: white;
}}

.stButton>button {{
    background: linear-gradient(90deg,#6366f1,#8b5cf6);
    color: white;
    border-radius: 10px;
    height: 42px;
    font-size: 16px;
}}

.card {{
    background-color: rgba(255,255,255,0.95);
    padding: 22px;
    border-radius: 14px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.25);
    margin-bottom: 20px;
}}

.login-card {{
    max-width: 420px;
    margin: auto;
    margin-top: 90px;
    background: rgba(0,0,0,0.55);
    padding: 40px;
    border-radius: 18px;
    box-shadow: 0px 0px 40px rgba(99,102,241,0.5);
    backdrop-filter: blur(10px);
}}

.login-card h1 {{
    text-align: center;
}}

.login-card .stButton>button {{
    width: 100%;
}}

input {{
    background-color: rgba(255,255,255,0.1) !important;
    color: white !important;
}}

@media (max-width:768px) {{
    .main {{padding:10px;}}
    h1 {{font-size:26px;}}
    h2 {{font-size:20px;}}
}}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------
# SIMPLE LOCAL AUTH (DEMO)
# ---------------------------------------
import json
import hashlib

USER_FILE = "users.json"

def load_users():
    try:
        with open(USER_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def login(u, p):
    users = load_users()
    return users.get(u) == hash_password(p)

def register(u, p):
    users = load_users()
    if u in users:
        return False
    users[u] = hash_password(p)
    save_users(users)
    return True

def reset_password(u, p):
    users = load_users()
    if u not in users:
        return False
    users[u] = hash_password(p)
    save_users(users)
    return True

# ---------------------------------------
# LOGIN SCREEN
# ---------------------------------------
if not st.session_state.logged_in:

    st.markdown("<div class='login-card'>", unsafe_allow_html=True)

    st.title("🔐 Login to Legal AI Assistant")

    choice = st.radio("Select Option",["Login","Register","Forgot Password"])

    username = st.text_input("Username")
    password = st.text_input("Password",type="password")

    if choice=="Login":
        if st.button("Login"):
            if login(username,password):
                st.session_state.logged_in=True
                st.rerun()
            else:
                st.error("Invalid credentials")

    elif choice=="Register":
        if st.button("Register"):
            if register(username,password):
                st.success("Registration successful")
            else:
                st.error("User already exists")

    elif choice=="Forgot Password":
        new_pass = st.text_input("New Password",type="password")
        if st.button("Reset Password"):
            if reset_password(username,new_pass):
                st.success("Password updated")
            else:
                st.error("User not found")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ---------------------------------------
# SIDEBAR
# ---------------------------------------
if st.sidebar.button("Logout"):
    st.session_state.logged_in=False
    st.rerun()

st.sidebar.markdown("### 🎨 Theme")
st.session_state.theme = st.sidebar.radio("Mode",["Dark","Light"])

menu = st.sidebar.radio(
    "Navigation",
    ["Upload & Analyze","Templates","Knowledge Base"]
)

# ---------------------------------------
# HEADER
# ---------------------------------------
st.markdown("""
# ⚖️ GenAI Legal Assistant for SMEs  
### Understand contracts • Detect risks • Get simple explanations
""")

# ---------------------------------------
# UPLOAD & ANALYZE
# ---------------------------------------
if menu=="Upload & Analyze":

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 🎙 Speak Contract Clause")

    if st.button("Start Voice Input"):
        spoken_text = get_voice_text()

        if spoken_text:
            st.success("Voice captured successfully!")
            st.text_area("Recognized Text", spoken_text, height=120)
        else:
            st.error("Could not recognize speech. Try again.")

    st.markdown('</div>', unsafe_allow_html=True)


    st.markdown('<div class="card">',unsafe_allow_html=True)
    st.markdown("## 📤 Upload Contract")
    file = st.file_uploader("Upload PDF / DOCX / TXT",
            type=["pdf","docx","txt"])
    st.markdown('</div>',unsafe_allow_html=True)

    if file:
        with st.spinner("Analyzing contract with AI..."):

            st.markdown('<div class="card">',unsafe_allow_html=True)
            st.markdown("## 📄 Clause Risk Analysis")

            st.write("Clause: Payment must be made within 7 days.")
            st.error("High Risk")

            st.write("Clause: Either party may terminate with notice.")
            st.warning("Medium Risk")

            st.write("Clause: Confidentiality obligations apply.")
            st.success("Low Risk")

            st.markdown('</div>',unsafe_allow_html=True)

            st.markdown('<div class="card">',unsafe_allow_html=True)
            st.markdown("## 📊 Risk Dashboard")

            c1,c2,c3=st.columns(3)
            c1.metric("🔴 High",1)
            c2.metric("🟠 Medium",1)
            c3.metric("🟢 Low",1)

            st.bar_chart({
                "Risk":["High","Medium","Low"],
                "Count":[1,1,1]
            },x="Risk",y="Count")

            st.success("Overall Contract Risk: MEDIUM")
            st.markdown('</div>',unsafe_allow_html=True)

# ---------------------------------------
# TEMPLATES
# ---------------------------------------
if menu=="Templates":

    st.markdown('<div class="card">',unsafe_allow_html=True)
    st.markdown("## 📑 Templates")

    temp = st.selectbox("Choose Template",
            ["Employment Agreement","Service Agreement"])

    if temp=="Employment Agreement":
        text="""EMPLOYMENT AGREEMENT
Employer: _______
Employee: _______
Salary: _______
Notice Period: _______
"""
    else:
        text="""SERVICE AGREEMENT
Client: _______
Provider: _______
Scope: _______
Payment: _______
"""

    st.text_area("Preview",text,height=250)
    st.download_button("Download Template",text)
    st.markdown('</div>',unsafe_allow_html=True)

# ---------------------------------------
# KNOWLEDGE BASE
# ---------------------------------------
if menu=="Knowledge Base":

    st.markdown('<div class="card">',unsafe_allow_html=True)
    st.markdown("## 📚 Common Contract Issues")

    st.write("• Late payment penalties")
    st.write("• One-sided termination")
    st.write("• Broad indemnity")
    st.write("• No IP ownership clarity")

    st.markdown('</div>',unsafe_allow_html=True)
