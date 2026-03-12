<h1 align="center">🎙️ VaaniAI</h1>

<p align="center">
  <strong>An AI-based conversational agent that listens, understands, and responds naturally using speech and text.</strong>
</p>

<p align="center">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-blue.svg">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.8+-blue.svg">
  <img alt="Status" src="https://img.shields.io/badge/status-active-success.svg">
</p>

---

## 📖 Overview

**VaaniAI** is a next-generation AI talking agent designed to create seamless, natural interactions between humans and machines. By combining advanced speech recognition, large language models (LLMs), and text-to-speech technology, VaaniAI acts as an intelligent conversational assistant that you can talk to, just like a human.

Whether you're building a voice-controlled application, an interactive learning tool, or a personal assistant, VaaniAI provides the foundation for rich, real-time voice and text interactions.

## ✨ Features

- **🗣️ Speech-to-Text (STT):** Highly accurate voice input processing to understand spoken commands.
- **🧠 AI Conversation Engine:** Leverages powerful LLMs to generate context-aware, intelligent, and human-like responses.
- **🔊 Text-to-Speech (TTS):** Natural and expressive voice output for a truly conversational experience.
- **⚡ Real-time Interaction:** Low-latency processing ensures smooth, uninterrupted back-and-forth dialogue.
- **⌨️ Multi-Modal Support:** Interact seamlessly via voice or text input.
- **⚙️ Extensible Architecture:** Easily modularized to swap out different STT, LLM, or TTS engines depending on your needs.

## 🛠️ Tech Stack

VaaniAI is built using modern and robust technologies:

- **Language:** Python 3.8+
- **Speech Recognition (STT):** *e.g., OpenAI Whisper, SpeechRecognition, or Google Speech API*
- **Intelligence (LLM):** *e.g., OpenAI Models, Anthropic Claude, or local models via Llama.cpp*
- **Text-to-Speech (TTS):** *e.g., ElevenLabs, pyttsx3, or Google TTS (gTTS)*

## 📂 Project Structure

A typical layout of the VaaniAI repository:

```text
VaaniAI/
├── src/                  # Main source code
│   ├── main.py           # Application entry point
│   ├── audio_input.py    # Speech-to-Text logic
│   ├── llm_engine.py     # AI interaction and prompt handling
│   └── audio_output.py   # Text-to-Speech logic
├── tests/                # Unit and integration tests
├── requirements.txt      # Project dependencies
├── .env.example          # Example environment variables
├── README.md             # Project documentation (you are here)
└── LICENSE               # License file
```

## 🚀 Installation

Follow these steps to get VaaniAI running locally on your machine.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nishant-0411/VaaniAI.git
   cd VaaniAI
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Copy `.env.example` to `.env`.
   - Add your necessary API keys (e.g., OpenAI, ElevenLabs) inside the `.env` file.
   ```bash
   cp .env.example .env
   ```

## 🎮 Usage

To start interacting with VaaniAI, simply run the main script:

```bash
python src/main.py
```

- **Voice Mode:** Speak into your microphone when prompted. VaaniAI will listen, process your request, and reply verbally.
- **Text Mode:** Alternatively, you can type your queries if you prefer a silent interaction.
- **Exit:** Say "Goodbye", type "exit", or press `Ctrl + C` to stop the agent.

## 🔮 Future Improvements

- [ ] **Wake Word Detection:** Activate the agent hands-free by saying a specific wake word (e.g., "Hey Vaani").
- [ ] **Memory & Context Retention:** Implement vector databases (like ChromaDB or Pinecone) for long-term user memory and context across sessions.
- [ ] **Multi-language Support:** Allow VaaniAI to converse fluently in different languages.
- [ ] **Web/GUI Interface:** Build a sleek frontend (e.g., using Streamlit, React, or PyQt) for easier user interaction.

## 🤝 Contributing

Contributions are what make the open-source community an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
