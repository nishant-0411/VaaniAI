import streamlit as st
import io
import speech_recognition as sr
from src.intelligence.llm_client import LLMClient
from src.audio.stt_engine import STTEngine
from src.audio.tts_engine import TTSEngine

st.set_page_config(page_title="VaaniAI - Voice Assistant", page_icon="🎙️")

st.title("🎙️ VaaniAI - Voice Assistant")
st.markdown("An advanced, real-time conversational AI agent that listens, thinks, and speaks naturally.")

# Initialize models
@st.cache_resource
def get_engines():
    stt = STTEngine()
    tts = TTSEngine(mode="gtts") # Defaulting to gtts to avoid elevenlabs api limit if needed, or elevenlabs if user set the key
    return stt, tts

stt, tts = get_engines()

# Initialize LLMClient in session state to hold memory
if "llm_client" not in st.session_state:
    st.session_state.llm_client = LLMClient()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history from session state
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "audio" in msg:
            st.audio(msg["audio"], format="audio/mp3")

def process_user_input(text):
    if not text.strip():
        return
    
    # Add user message to UI state
    st.session_state.messages.append({"role": "user", "content": text})
    with st.chat_message("user"):
        st.write(text)
    
    # Process with LLM
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response_placeholder = st.empty()
            full_response = ""
            for token in st.session_state.llm_client.get_response_stream(text):
                full_response += token
                response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
        
        with st.spinner("Generating audio..."):
            try:
                # Try getting elevenlabs key from env dynamically inside the speak if mode is elevenlabs, 
                # but tts logic falls back to gTTS if it fails anyway
                audio_bytes = tts.speak(full_response)
                st.audio(audio_bytes, format="audio/mp3", autoplay=True)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": full_response, 
                    "audio": audio_bytes
                })
            except Exception as e:
                st.error(f"TTS Error: {e}")
                st.session_state.messages.append({"role": "assistant", "content": full_response})

# Voice Input
st.write("---")
st.subheader("Voice Input")
audio_value = st.audio_input("Record a voice message")
    
if audio_value:
    audio_id = hash(audio_value.getvalue())
        
    if "last_audio_id" not in st.session_state or st.session_state.last_audio_id != audio_id:
        st.session_state.last_audio_id = audio_id
            
        with st.spinner("Transcribing audio..."):
            r = sr.Recognizer()
            try:
                with sr.AudioFile(audio_value) as source:
                    audio_data = r.record(source)
                text = stt.transcribe(audio_data)
                    
                if text:
                    process_user_input(text)
                else:
                    st.warning("Could not transcribe audio. Try again.")
            except Exception as e:
                st.error(f"STT Error: {e}")

# Text Input
st.write("---")
user_text = st.chat_input("Type a message here...")
if user_text:
    process_user_input(user_text)
