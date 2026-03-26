<div align="center">
  <h1>🎙️ VaaniAI</h1>
  <p><strong>An advanced, real-time conversational AI agent that listens, thinks, and speaks naturally.</strong></p>

  <p>
    <img alt="Python Version" src="https://img.shields.io/badge/Python-3.11+-blue.svg?logo=python&logoColor=white">
    <img alt="License" src="https://img.shields.io/badge/License-MIT-green.svg">
    <img alt="Status" src="https://img.shields.io/badge/Status-Active-success.svg">
  </p>
</div>

---

## 📖 Overview

**VaaniAI** is a next-generation voice assistant designed to bridge the gap between human and machine interaction. Moving beyond simple text-based chatbots, VaaniAI provides a rich, multi-modal experience by combining state-of-the-art **Speech-to-Text (STT)**, intelligent **Large Language Models (LLMs)**, and lifelike **Text-to-Speech (TTS)**.

Whether you're looking for a vocal coding companion, a language practice partner, or the foundation for a complex smart-home system, VaaniAI delivers low-latency, context-aware, and natural dialogues.

## ✨ Key Features

- **🗣️ Advanced Speech Recognition:** Seamlessly captures and transcribes spoken audio using powerful STT models (e.g., Whisper).
- **🧠 Context-Aware Intelligence:** Integrates with OpenAI's LLMs and maintains a dynamic conversation memory, allowing for deep, continuous discussions.
- **🔊 Expressive Voice Output:** Utilizes premium TTS services like ElevenLabs (or local alternatives) for incredibly realistic and emotive speech.
- **⚡ Streaming Architecture:** Built for real-time interaction. Audio is captured in chunks, and responses are processed efficiently to minimize latency.
- **⚙️ Modular & Extensible:** The architecture is decoupled into distinct intelligence, audio, and core components, making it trivial to swap or upgrade models.

## 🛠️ Tech Stack

VaaniAI leverages a modern Python ecosystem:

- **Core & Logic:** Python 3.11+, `pyaudio` for streaming.
- **Speech-to-Text (STT):** `speechrecognition`, `openai-whisper`.
- **Language Intelligence (LLM):** `openai` API.
- **Text-to-Speech (TTS):** `elevenlabs` (premium), `pyttsx3`, `gtts`.

## 📂 Architecture & Structure

The repository is modularized for clean separation of concerns:

```text
VaaniAI/
├── src/
│   ├── audio/              # STT, TTS engines, and audio I/O streaming
│   ├── core/               # Main application loop and configurations
│   ├── intelligence/       # LLM clients and contextual memory management
│   └── utils/              # Helper modules (e.g., custom loggers)
├── tests/                  # Unit and integration test suite
├── .env                    # Environment variables (API keys)
├── pyproject.toml          # Modern dependency management
├── requirements.txt        # Classic dependency list
└── README.md
```

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nishant-0411/VaaniAI.git
   cd VaaniAI
   ```

2. **Set up a Python virtual environment (Requires Python 3.11+):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   Using the standard `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
   *(Alternatively, you can install via `pip install .` using `pyproject.toml`)*

4. **Configure Environment Variables:**
   Copy the example environment file and add your API keys (e.g., OpenAI, ElevenLabs).
   ```bash
   cp .env.example .env
   ```
   *Note: Ensure all required keys specific to your chosen LLM and TTS engines are populated.*

## 🎮 Usage

Start interacting with the VaaniAI assistant by executing the core module from the project root:

```bash
python -m src.core.main
```

- **Listening Mode:** When the console displays `STATE: LISTENING`, simply speak into your microphone.
- **Thinking Mode:** The AI will process the transcription and stream its thought process.
- **Speaking Mode:** The generated response will be spoken aloud immediately.
- **Exit:** Use `Ctrl + C` at any time to gracefully shut down the assistant.

## 🔮 Roadmap & Future Improvements

- [ ] **Wake Word Detection:** Activate VaaniAI entirely hands-free (e.g., "Hey Vaani").
- [ ] **Vector Database Memory:** Integrate ChromaDB or Pinecone for long-term, semantic memory spanning across multiple sessions.
- [ ] **Function Calling & Tool Use:** Allow the AI to interact with external APIs, check the weather, or execute system commands.
- [ ] **Web GUI Interface:** Develop a rich visual frontend using React or Streamlit.

## 🤝 Contributing

Contributions are highly encouraged! Whether it's adding a new TTS engine integration, fixing bugs, or improving documentation:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/NewAwesomeEngine`
3. Commit your changes: `git commit -m 'Add support for NewAwesomeEngine'`
4. Push to the branch: `git push origin feature/NewAwesomeEngine`
5. Open a Pull Request.

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
