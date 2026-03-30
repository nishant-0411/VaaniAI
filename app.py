import streamlit as st
import io
import speech_recognition as sr
from src.intelligence.llm_client import LLMClient
from src.audio.stt_engine import STTEngine
from src.audio.tts_engine import TTSEngine

st.set_page_config(
    page_title="VaaniAI - Advanced Voice Assistant", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "voice_speed" not in st.session_state:
    st.session_state.voice_speed = 1.0
if "auto_play" not in st.session_state:
    st.session_state.auto_play = True

# Custom CSS for Premium Design
st.markdown("""
<style>
    /* Main container and text */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1200px;
    }
    
    /* Dark mode support */
    .stApp {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%); /* White gradient */
    }
    
    /* Animated background */
    .animated-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(270deg, #ffffff, #f8f9fa, #f1f3f4, #e8eaed, #f5f5f5);
        background-size: 800% 800%;
        animation: gradientShift 15s ease infinite;
        z-index: -1;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Header Styling */
    .main-header {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 2.8rem;
        background: -webkit-linear-gradient(45deg, #424242, #616161, #757575);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        padding-bottom: 0px;
    }
    
    .sub-header {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        color: #888;
        margin-top: -10px;
        margin-bottom: 30px;
    }

    /* Standardize Chat message design */
    [data-testid="stChatMessage"] {
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        backdrop-filter: blur(10px);
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(200, 200, 200, 0.5);
        box-shadow: 0 8px 32px rgba(150, 150, 150, 0.1);
    }
    
    /* Voice recording button animation */
    .recording {
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(245, 245, 245, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(200, 200, 200, 0.7);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(150, 150, 150, 0.8);
    }

    div[data-testid="stChatInput"] {
        padding-bottom: 20px;
    }

</style>
""", unsafe_allow_html=True)

# -----------------
# Sidebar Settings
# -----------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/8644/8644102.png", width=60)
    st.markdown("### ⚙️ Settings & Configuration")
    
    # Theme toggle
    theme_option = st.selectbox("🎨 Theme", ["Dark", "Light"], index=0)
    st.session_state.theme = theme_option.lower()
    
    st.markdown("#### 🎤 Audio Inputs (STT)")
    stt_option = st.selectbox("Speech-to-Text Engine", ["Google STT", "Whisper"])
    whisper_model = "base"
    if stt_option == "Whisper":
        whisper_model = st.selectbox("Whisper Model", ["tiny", "base", "small", "medium"], index=1)
    
    st.markdown("#### 🔊 Audio Outputs (TTS)")
    tts_option = st.selectbox("Text-to-Speech Engine", ["gTTS", "ElevenLabs"])
    
    # Voice settings
    st.session_state.voice_speed = st.slider("🗣️ Voice Speed", 0.5, 2.0, 1.0, 0.1)
    st.session_state.auto_play = st.checkbox("🔊 Auto-play Audio", value=True)
    
    # Statistics
    st.markdown("#### 📊 Session Stats")
    if "messages" in st.session_state:
        total_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
        st.metric("Total Interactions", total_messages)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.messages = []
            if "llm_client" in st.session_state:
                st.session_state.llm_client = LLMClient()
            st.rerun()
    with col2:
        if st.button("💾 Export", use_container_width=True):
            if "messages" in st.session_state:
                st.download_button(
                    label="Download Chat",
                    data=str(st.session_state.messages),
                    file_name="vaani_chat.txt",
                    mime="text/plain"
                )
        
    st.markdown("---")
    st.caption("VaaniAI v1.0 | Developed for natural conversation.")
    
    # API Status
    st.markdown("#### 🔌 API Status")
    try:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        # Check Ollama status
        import requests
        try:
            ollama_response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if ollama_response.status_code == 200:
                models = ollama_response.json().get("models", [])
                model_names = [m["name"] for m in models]
                st.success(f"✅ Ollama Connected - Models: {', '.join(model_names)}")
            else:
                st.warning("⚠️ Ollama not responding")
        except:
            st.warning("⚠️ Ollama not running - Start with: ollama serve")
            
        if os.getenv("ELEVENLABS_API_KEY"):
            st.success("✅ ElevenLabs Connected")
        else:
            st.info("ℹ️ ElevenLabs API Key Missing - Using gTTS instead")
    except:
        st.error("❌ Could not verify API status")


# -----------------
# Initialization
# -----------------
@st.cache_resource
def get_engines(stt_engine_name, whisper_model_name, tts_engine_name):
    use_whisper = (stt_engine_name == "Whisper")
    stt = STTEngine(use_whisper=use_whisper, whisper_model=whisper_model_name)
    
    mode_tts = "elevenlabs" if tts_engine_name == "ElevenLabs" else "gtts"
    tts = TTSEngine(mode=mode_tts)
    return stt, tts

stt, tts = get_engines(stt_option, whisper_model, tts_option)

if "llm_client" not in st.session_state:
    st.session_state.llm_client = LLMClient()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am VaaniAI. How can I assist you today?"}]


# -----------------
# Main Interface
# -----------------
# Add animated background
st.markdown('<div class="animated-bg"></div>', unsafe_allow_html=True)

# Main Header with enhanced styling
st.markdown('<div class="main-header">🎙️ VaaniAI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">An advanced, real-time conversational AI agent that listens, thinks, and speaks naturally.</div>', unsafe_allow_html=True)

st.markdown("---")

# Enhanced Audio Input Section
st.markdown("#### 🎤 Voice Interaction")
col1, col2 = st.columns([3, 1])
with col1:
    audio_value = st.audio_input("Record your voice message to chat...")
with col2:
    if st.button("🎙️", help="Click to start recording"):
        st.info("Use the audio input on the left to record your voice")

if "last_audio_id" not in st.session_state:
    st.session_state.last_audio_id = None

# -----------------
# Chat Functions
# -----------------
def process_user_input(text):
    if not text.strip():
        return
    
    # Add user message to UI state
    st.session_state.messages.append({"role": "user", "content": text})
    
    # Display the new user message immediately
    with chat_container:
        with st.chat_message("user", avatar="👤"):
            st.write(text)
        
        # Process with LLM
        with st.chat_message("assistant", avatar="🤖"):
            response_placeholder = st.empty()
            full_response = ""
            
            with st.spinner("🤔 Thinking..."):
                try:
                    for token in st.session_state.llm_client.get_response_stream(text):
                        if token:
                            full_response += token
                            response_placeholder.markdown(full_response + "▌")
                    response_placeholder.markdown(full_response)
                except Exception as e:
                    st.error(f"🚨 LLM Error: {e}")
                    if not full_response:
                        full_response = "I encountered an error while thinking. Please try again."
                    response_placeholder.markdown(full_response)
            
            if st.session_state.auto_play:
                with st.spinner("🔊 Generating audio..."):
                    audio_bytes = None
                    try:
                        audio_bytes = tts.speak(full_response)
                        if audio_bytes:
                            st.audio(audio_bytes, format="audio/mp3", autoplay=True)
                            st.success("✅ Audio generated successfully")
                    except Exception as e:
                        st.error(f"🚨 TTS Error: {e}")
            
            # Save to messages state
            msg_data = {
                "role": "assistant", 
                "content": full_response
            }
            if audio_bytes:
                msg_data["audio"] = audio_bytes
                
            st.session_state.messages.append(msg_data)

# Process Voice Input
if audio_value:
    audio_id = hash(audio_value.getvalue())
    if st.session_state.last_audio_id != audio_id:
        st.session_state.last_audio_id = audio_id
            
        with st.spinner("🎤 Transcribing audio..."):
            r = sr.Recognizer()
            try:
                with sr.AudioFile(audio_value) as source:
                    audio_data = r.record(source)
                
                transcribed_text = stt.transcribe(audio_data)
                    
                if transcribed_text:
                    st.toast(f"✅ Transcribed: {transcribed_text}", icon="✅")
                else:
                    st.warning("⚠️ Could not transcribe audio. Try again.")
                    transcribed_text = None
            except Exception as e:
                st.error(f"🚨 STT Error: {e}")
                transcribed_text = None

# Layout the chat interface
chat_container = st.container()

with chat_container:
    for msg in st.session_state.messages:
        avatar = "👤" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
            if "audio" in msg and msg["audio"]:
                st.audio(msg["audio"], format="audio/mp3")

if audio_value and 'transcribed_text' in locals() and transcribed_text:
    process_user_input(transcribed_text)

# Text Input
user_text = st.chat_input("Or type a message here...")
if user_text:
    process_user_input(user_text)
