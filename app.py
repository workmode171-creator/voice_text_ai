
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from transcription import transcribe_audio

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Voice to Text AI",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

/* Main background */
.stApp {
    background: #F1F5F9 !important;
    color: #172033 !important;
    font-family: Arial, sans-serif;
}

/* Main text */
.stApp p,
.stApp label,
.stMarkdown,
.stCaption,
.stApp li {
    color: #172033 !important;
    font-size: 17px !important;
    font-weight: 500 !important;
}

/* Headings */
h1, h2, h3 {
    color: #172554 !important;
    font-weight: 800 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #E2E8F0 !important;
}

/* Cards */
[data-testid="stMetric"] {
    background: #FFFFFF !important;
    padding: 18px !important;
    border-radius: 14px !important;
}

/* Text area */
.stTextArea textarea {
    background: #FFFFFF !important;
    color: #172033 !important;
    -webkit-text-fill-color: #172033 !important;
    font-size: 18px !important;
    font-weight: 600 !important;
    border: 2px solid #94A3B8 !important;
}

/* Dropdown */
.stSelectbox div[data-baseweb="select"] {
    background: #FFFFFF !important;
    color: #172033 !important;
    font-size: 17px !important;
}

/* Buttons */
.stButton button {
    background: #0F766E !important;
    color: #FFFFFF !important;
    font-size: 17px !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
}

/* Placeholder */
textarea::placeholder {
    color: #64748B !important;
    opacity: 1 !important;
}

</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------

st.markdown("""
<div class="hero">
    <h1>🎙️ Voice to Text AI</h1>
    <p>
        Your voice. Your words. Instantly.
        <br>
        Convert speech into text using English,
        Tamil and Hindi recognition.
    </p>
</div>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.markdown("## 🎙️ Voice to Text AI")
    st.caption("Speech recognition workspace")

    st.markdown("---")

    st.markdown("### 🌐 Supported languages")

    st.markdown("""
    - 🇬🇧 English
    - 🇮🇳 தமிழ் (Tamil)
    - 🇮🇳 हिन्दी (Hindi)
    """)

    st.markdown("---")

    st.markdown("### 💡 Recording tips")
    st.write("• Speak clearly.")
    st.write("• Reduce background noise.")
    st.write("• Keep your microphone close.")
    st.write("• Use a stable internet connection.")

    st.markdown("---")
    st.caption("Powered by Google Speech Recognition")


# ---------------- STATISTICS ----------------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="stat-card">
        <h2>03</h2>
        <p>Languages</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-card">
        <h2>🎤</h2>
        <p>Voice Recording</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-card">
        <h2>TXT</h2>
        <p>Text Download</p>
    </div>
    """, unsafe_allow_html=True)


st.write("")


# ---------------- LANGUAGE SELECTION ----------------

st.markdown("## 🌍 Choose your language")

language_options = {
    "🇬🇧 English": "en-IN",
    "🇮🇳 தமிழ் (Tamil)": "ta-IN",
    "🇮🇳 हिन्दी (Hindi)": "hi-IN"
}

selected_language = st.selectbox(
    "Select the language you will speak:",
    list(language_options.keys())
)

language_code = language_options[selected_language]


# ---------------- RECORDING SECTION ----------------

st.markdown("""
<div class="section-card">
    <h3>🎙️ Record your voice</h3>
    <p>Click the microphone button below to start recording.</p>
</div>
""", unsafe_allow_html=True)

audio_bytes = audio_recorder(
    text="Click to record / stop",
    recording_color="#E74C3C",
    neutral_color="#20B9A8",
    icon_name="microphone",
    icon_size="3x",
    pause_threshold=2.0,
    sample_rate=16000
)


# ---------------- AUDIO PROCESSING ----------------

if audio_bytes:

    st.success("✅ Audio recorded successfully!")

    st.audio(
        audio_bytes,
        format="audio/wav"
    )

    if st.button(
        "✨ Convert Voice to Text",
        use_container_width=True
    ):

        with st.spinner(
            "Processing your speech... Please wait."
        ):

            result = transcribe_audio(
                audio_bytes,
                language=language_code
            )

        if result.startswith("Error:"):
            st.error(result)

        elif (
            result.startswith("Sorry")
            or result.startswith("Internet")
        ):
            st.warning(result)

        else:

            st.session_state["transcribed_text"] = result

            st.success("🎉 Transcription completed!")


# ---------------- RESULT SECTION ----------------

if "transcribed_text" in st.session_state:

    st.markdown("---")

    st.markdown("## 📝 Your Transcribed Text")

    edited_text = st.text_area(
        "You can edit your converted text here:",
        value=st.session_state["transcribed_text"],
        height=220,
        key="editable_transcription"
    )

    st.download_button(
        label="⬇️ Download Text File",
        data=edited_text,
        file_name="voice_to_text.txt",
        mime="text/plain",
        use_container_width=True
    )

    st.code(edited_text, language=None)

    if st.button(
        "🗑️ Clear Transcription",
        use_container_width=True
    ):
        del st.session_state["transcribed_text"]
        st.rerun()


# ---------------- FOOTER ----------------

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; padding:15px;">
        <h4 style="color:#142B4A;">
            🎙️ Voice to Text AI
        </h4>
        <p style="color:#64748b;">
            Making speech conversion simple and accessible.
        </p>
        <p style="color:#20A995; font-size:13px;">
            English | தமிழ் | हिन्दी
        </p>
    </div>
    """,
    unsafe_allow_html=True
)



