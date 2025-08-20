import os
import streamlit as st
import base64
from utils.generator import generate_content_ideas 

st.set_page_config(
    page_title="Ufuq AI Generator",
    layout="wide",  # This is critical
)

# --- Load styles ---
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- global styles ---
st.markdown("""
    <style>
        /* Full-width body */
        .main {
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            padding-top: 0rem !important;
        }

        /* Maximize width for container */
        .block-container {
            padding: 0rem 2rem 2rem 2rem;
            margin: 0 auto;
            width: 100%;
        }

        /* Remove unnecessary space at top */
        header[data-testid="stHeader"] {
            height: 0rem;
        }

        /* Remove default blank space */
        [data-testid="stToolbar"] {
            visibility: hidden;
            height: 0%;
            position: fixed;
        }
/* Responsive tweaks for small screens */
@media (max-width: 768px) {
    .header-container {
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;
    }

    .logo-title h3 {
        font-size: 18px;
    }

    .menu-links {
        flex-direction: column;
        gap: 8px;
    }

    .content-card {
        font-size: 14px;
    }
}
    </style>
""", unsafe_allow_html=True)

# ===== Header navigation with aligned logo + title --- Include custom CSS=====
st.markdown("""
    <style>
        .header {
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: #1e1e1e;
            padding: 10px 0;
        }
        .header img {
        height: 50px;
        width: 50px;
        }
        .header-title {
            color: white;
            font-size: 32px;
            font-weight: 700;
        }
        .nav-bar {
            display: flex;
            justify-content: center;
            background-color: #000;
            padding: 10px 0;
            margin-bottom: 20px;
        }
        .nav-bar a {
            margin: 0 15px;
            color: gold;
            text-decoration: none;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# =======Render header with logo and title===========

st.markdown("""
    <div class="header" style="display: flex; align-items: center; justify-content: space-between; padding: 1rem 2rem; background-color: #5c95d2; border-bottom: 1px solid #e0e0e0;">
        <img src="data:image/png;base64,{}" alt="Logo">
        <a href="#"><button style='margin:5px' background-color: #007bff; hover: #007bff;>Home</button></a>
        <a href="#"><button style='margin:5px' background-color: #007bff; hover: #007bff;>About Us</button></a>
        <h2 class="header-title"> Ufuq AI GenAI </h2>
        <a href="#"><button style='margin:5px' background-color: #007bff; hover: #007bff;>Contact</button></a>
        <a href="#"><button style='margin:5px' background-color: #007bff; hover: #007bff;>Feedback</button></a>
    </div>
""".format(base64.b64encode(open("assets/logo.png", "rb").read()).decode()), unsafe_allow_html=True)


# --- Language and Platform (on one line) ---
st.markdown("### Set Your Preferences Language and Platform:")
lang_col, plat_col = st.columns(2)
with lang_col:
    language = st.selectbox("Language:", ["English", "Amharic", "Arabic", "French","Oromo","Swahili"])
with plat_col:
    platform = st.selectbox("Platform:", ["TikTok", "YouTube", "Instagram", "Facebook","Instagram"])

# --- User Inputs ---
niche = st.text_input("Your Niche (e.g. Tech, Business, Cooking, Travel)", "")
audience = st.text_input("Target Audience (e.g. Students, Parents, Entrepreneurs,Youth)", "")
history = st.text_area("What topics have you covered before? (optional)", "")

# # --- Generate Button ---
import streamlit.components.v1 as components

# --- Generate Button ---
if st.button("🚀 Generate", type="primary"):
    if not niche or not audience:
        st.warning("⚠️ Please fill in the required fields both niche and audience.")
    else:
        with st.spinner("Generating ideas..."):
            try:
                result = generate_content_ideas(niche, audience, history, platform, language)

                st.markdown("### 💡 Your AI-Powered Content Ideas:")

                ideas = [idea.strip() for idea in result.split("---") if idea.strip()]

                for i, idea in enumerate(ideas):
                    st.markdown(f"<div class='content-card'>{idea}</div>", unsafe_allow_html=True)
                    unique_id = f"copy_button_{i}"

                    # Add copy button for each idea
                    components.html(f"""
                        <button onclick="copyToClipboard_{unique_id}()" style="
                            background-color:#007bff;
                            color:white;
                            border:none;
                            padding:8px 12px;
                            border-radius:5px;
                            margin-bottom:20px;
                            cursor:pointer;
                        "> 📋 Copy </button>

                        <script>
                        function copyToClipboard_{unique_id}() {{
                            const text = `{idea.replace("`", "\\`")}`;
                            navigator.clipboard.writeText(text).then(function() {{
                                alert("✅ Copied");
                            }}, function(err) {{
                                alert("❌ Failed to copy!");
                            }});
                        }}
                        </script>
                    """, height=100)

            except Exception as e:
                st.error(f"❌ Error: {e}")


# ====== FEEDBACK FORM ======
with st.expander("💬 Give Us Your Feedback", expanded=False):
    with st.form("feedback_form"):
        st.write("We’d love to hear your thoughts about the Ufuq AI Content Generator!")

        name = st.text_input("Your Name")
        email = st.text_input("Email Address")
        rating = st.selectbox("How would you rate your experience?", ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐", "⭐"])
        message = st.text_area("Your Feedback")

        send = st.form_submit_button("Send Feedback")

        if send:
            if not message.strip():
                st.warning("Please write your feedback before submitting." + " 🚀")
            else:
                # Later: Store to database or send to email
                st.success("✅ Thank you for your feedback!")

# --- Footer ---
st.markdown("""
 <div class="footer">
     <p>Developed with ❤️ by Ufuq AI | <a href="#Contact">Contact</a> | <a href="#Feedback">Feedback</a></p>
     <div class="footer-icons">
        <a href='#facebook'><button style='margin:5px'>Facebook</button></a>
        <a href='#Instagram'><button style='margin:5px'>Instagram</button></a>
        <a href='#LinkedIn'><button style='margin:5px'>LinkedIn</button></a>
        <a href='#GitHub'><button style='margin:5px'>GitHub</button></a>
        <a href='#YouTube'><button style='margin:5px'>YouTube</button></a>
        <a href='#TikTok'><button style='margin:5px'>TikTok</button></a>
    </div>
 </div>
""", unsafe_allow_html=True)
