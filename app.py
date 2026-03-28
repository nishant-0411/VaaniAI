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

# Custom CSS for Premium Design
st.markdown("""
<style>
    /* Main container and text */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
    }
    
    /* Header Styling */
    .main-header {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 2.8rem;
        background: -webkit-linear-gradient(45deg, #FF4B2B, #FF416C);
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
    
    st.markdown("#### Audio Inputs (STT)")
    stt_option = st.selectbox("Speech-to-Text Engine", ["Google STT", "Whisper"])
    whisper_model = "base"
    if stt_option == "Whisper":
        whisper_model = st.selectbox("Whisper Model", ["tiny", "base", "small", "medium"], index=1)
    
    st.markdown("#### Audio Outputs (TTS)")
    tts_option = st.selectbox("Text-to-Speech Engine", ["gTTS", "ElevenLabs"])
    
    st.markdown("---")
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        if "llm_client" in st.session_state:
            # Memory should be cleared but LLMClient doesn't expose a clear method directly
            # Recreate the client
            st.session_state.llm_client = LLMClient()
        st.rerun()
        
    st.markdown("---")
    st.caption("VaaniAI v1.0 | Developed for natural conversation.")


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
st.markdown('<div class="main-header">🎙️ VaaniAI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">An advanced, real-time conversational AI agent that listens, thinks, and speaks naturally.</div>', unsafe_allow_html=True)

# Audio Input Section (Top for accessibility)
st.markdown("#### 🎤 Voice Interaction")
audio_value = st.audio_input("Record your voice message to chat...")

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
            
            with st.spinner("Thinking..."):
                try:
                    for token in st.session_state.llm_client.get_response_stream(text):
                        if token:
                            full_response += token
                            response_placeholder.markdown(full_response + "▌")
                    response_placeholder.markdown(full_response)
                except Exception as e:
                    st.error(f"LLM Error: {e}")
                    if not full_response:
                        full_response = "I encountered an error while thinking."
                    response_placeholder.markdown(full_response)
            
            with st.spinner("Generating audio..."):
                audio_bytes = None
                try:
                    audio_bytes = tts.speak(full_response)
                    if audio_bytes:
                        st.audio(audio_bytes, format="audio/mp3", autoplay=True)
                except Exception as e:
                    st.error(f"TTS Error: {e}")
            
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
            
        with st.spinner("Transcribing audio..."):
            r = sr.Recognizer()
            try:
                with sr.AudioFile(audio_value) as source:
                    audio_data = r.record(source)
                
                transcribed_text = stt.transcribe(audio_data)
                    
                if transcribed_text:
                    st.toast(f"Transcribed: {transcribed_text}", icon="✅")
                else:
                    st.warning("Could not transcribe audio. Try again.")
                    transcribed_text = None
            except Exception as e:
                st.error(f"STT Error: {e}")
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
