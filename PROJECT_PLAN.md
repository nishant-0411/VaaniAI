# VaaniAI - Comprehensive Project Plan & Milestones

This document outlines the extensive, step-by-step roadmap for building the **VaaniAI** conversational agent. The plan is designed to be executed **without hurry**, ensuring that all edge cases, robust error handling, scalability, and performance optimizations are considered from the ground up.

---

## 🎯 1. Project Overview & Goals
**Objective:** Build a highly responsive, intelligent, and context-aware conversational AI agent with voice-in and voice-out capabilities.
**Key Principles:**
- **Reliability:** The app should handle network drops, hardware disconnections, and API limits gracefully.
- **Low Latency:** Optimize the pipeline to feel as close to a real human conversation as possible.
- **Modularity:** Ensure each component (STT, LLM, TTS, DB) can be swapped out easily in the future.
- **Interruptibility:** Allow the user to cut the AI off mid-sentence to simulate natural conversation flow.

---

## 📂 2. Ultimate Project Structure

```text
VaaniAI/
├── src/                      # Main source code
│   ├── core/                 # Core engine and orchestrator
│   │   ├── __init__.py
│   │   ├── main.py           # Application entry point and main loop
│   │   └── config.py         # Centralized configuration loading
│   ├── audio/                # Audio processing modules
│   │   ├── __init__.py
│   │   ├── input_capture.py  # Microphone handling, noise reduction
│   │   ├── stt_engine.py     # Speech-to-Text logic
│   │   └── tts_engine.py     # Text-to-Speech logic
│   ├── intelligence/         # AI and LLM handling
│   │   ├── __init__.py
│   │   ├── llm_client.py     # API client for LLM provider
│   │   ├── memory.py         # Context sliding windows, long-term memory
│   │   └── prompt_manager.py # System prompts and persona definitions
│   ├── utils/                # Helper functions
│   │   ├── __init__.py
│   │   ├── logger.py         # Application-wide logging configuration
│   │   └── decorators.py     # Retry logic, timing, async wrappers
│   └── ui/                   # Future GUI / Web components
│       └── app.py            # Streamlit or PyQt entry point
├── tests/                    # Unit and integration tests
│   ├── test_audio.py
│   ├── test_llm.py
│   └── conftest.py           # Pytest fixtures and mocks
├── requirements.txt          # Project dependencies
├── requirements-dev.txt      # Development & testing dependencies
├── .env.example              # Example environment variables
├── pyproject.toml            # Modern Python project configuration
├── README.md                 # Project documentation
└── PROJECT_PLAN.md           # This document
```

---

## 📅 3. Execution Roadmap (Un-hurried, Edge-Case Focused)

### **Phase 1: Environment & Foundation (Days 1 - 4)**
*Focus: Setting up a bulletproof development environment and enforcing coding standards.*

- **Tasks:**
  - [Done] Set up a virtual environment (e.g., `venv` or `conda`).
  - [Done] Pin dependencies securely in `requirements.txt` to prevent future breaking changes.
  - [] Configure `pyproject.toml` with `black` for formatting and `flake8`, `mypy` for linting/type-checking.
  - [] Implement central logging (`src/utils/logger.py`) to rotate logs, preventing disk overflow and helping with deep debugging.
  - [] Build a robust centralized config loader (`src/core/config.py`) using `python-dotenv` and fallback default values.
- **Edge Cases Handled:**
  - What if `.env` is missing? (Fallback to defaults or raise a clear, readable error on startup).
  - Dependency conflicts between audio libraries on different OS (Mac vs Windows).

### **Phase 2: Robust Audio Input & STT (Days 5 - 10)**
*Focus: Capturing clean audio and transcribing it accurately, regardless of environment.*

- **Tasks:**
  - [ ] Implement microphone enumeration to allow users to select the correct audio input device.
  - [ ] Integrate background noise cancellation logic (`webrtcvad` or native PyAudio noise gates) to only wake STT on actual speech.
  - [ ] Integrate local (e.g., Whisper) or cloud-based (e.g., Google/Deepgram) STT.
  - [ ] Implement streaming audio capture to process chunks of audio for lower latency.
- **Edge Cases Handled:**
  - User's microphone disconnects mid-sentence.
  - Complete silence or high background static.
  - Transcription returns empty strings or gibberish.

### **Phase 3: Intelligence & Context Management (Days 11 - 16)**
*Focus: Connecting the brain of the agent while managing conversational state.*

- **Tasks:**
  - [ ] Create `src/intelligence/llm_client.py` using `openai` SDK or `Langchain`.
  - [ ] Implement streaming LLM responses (yielding tokens as they generate) to dramatically reduce wait times.
  - [ ] Build `memory.py` to maintain a sliding window of recent conversation history to avoid context limit exceeded errors (Token limit management).
  - [ ] Define system prompts that prevent the AI from generating excessively long, un-speakable text (e.g., formatting lists natively for voice).
- **Edge Cases Handled:**
  - API rate limiting (429 errors) - implementing exponential backoff (`tenacity` library).
  - User says something unsafe/filtered by the API provider.
  - Context grows too large (automatically summarize older messages to maintain memory).

### **Phase 4: Fluid Text-to-Speech (Days 17 - 22)**
*Focus: Giving the agent a voice that sounds natural and plays without stutter.*

- **Tasks:**
  - [ ] Implement `src/audio/tts_engine.py` using high-quality providers (e.g., ElevenLabs, OpenAI TTS).
  - [ ] Implement fallback to local offline TTS (`pyttsx3`) if the network drops or API quota is exhausted.
  - [ ] Setup an audio playback buffer. As the LLM streams text, chunk it into sentences, send to TTS, and queue for playback concurrently.
  - [ ] **Crucial Feature:** Interruptibility. If the user starts talking while the agent is speaking, instantly halt the audio playback and clear the queue.
- **Edge Cases Handled:**
  - TTS API takes too long to respond.
  - Playing audio crashes the main thread (fixed by threaded/async playback).
  - Preventing the microphone from picking up the speakers (echo cancellation/muting mic during playback).

### **Phase 5: The Orchestrator & Concurrency (Days 23 - 28)**
*Focus: Tying it all together in a continuous, non-blocking loop.*

- **Tasks:**
  - [ ] Write `src/core/main.py` leveraging `asyncio` or robust multithreading.
  - [ ] State management: `LISTENING` -> `THINKING` -> `SPEAKING`.
  - [ ] Implement graceful shutdown. Capturing `Ctrl+C` (SIGINT) to close audio streams, save memory to disk, and exit cleanly.
- **Edge Cases Handled:**
  - Deadlocks in threading when sharing the microphone stream.
  - Unhandled exceptions in background threads silently failing.

### **Phase 6: Comprehensive Testing (Days 29 - 34)**
*Focus: Ensuring reliability without manual testing every time.*

- **Tasks:**
  - [ ] Write unit tests for the Config and Logger modules.
  - [ ] Create mock fixtures (`tests/conftest.py`) for the LLM and TTS APIs so tests don't consume paid credits or require internet.
  - [ ] Write integration tests simulating the full pipeline using pre-recorded `.wav` files.
  - [ ] Add exception testing (forcing the mocked API to throw a 500 error to ensure the app doesn't crash).
- **Edge Cases Handled:**
  - Identifying memory leaks in the continuous audio loop.
  - CI/CD pipeline compatibility.

### **Phase 7: GUI, Polish, and Deployment (Days 35+)**
*Focus: Moving beyond the terminal and sharing the project.*

- **Tasks:**
  - [ ] Migrate the text output to a minimal visual interface using Streamlit or PyQt (`src/ui/app.py`).
  - [ ] Add visual cues (e.g., an animated waveform or status indicator showing when the bot is listening/speaking).
  - [ ] Create a `Dockerfile` for standardized execution across any OS.
  - [ ] Package the app as a standalone executable using `PyInstaller`.

---

## 🛡️ 4. Global Edge Cases & Mitigation Strategies

1. **Network Instability:** 
   - *Issue:* High latency or packet loss causes TTS/STT APIs to hang.
   - *Mitigation:* Implement strict HTTP timeouts (e.g., `timeout=5.0` seconds). If a timeout occurs, fallback to a local model or play a pre-recorded standard response like, "I'm having trouble connecting right now."
2. **Resource Exhaustion:**
   - *Issue:* Over hours of use, RAM spikes.
   - *Mitigation:* Explicitly garbage collect and delete audio chunk variables. Use context managers (`with microphone as source:`) to guarantee resources are released.
3. **Data Privacy & Security:**
   - *Issue:* Accidental logging of sensitive user audio or API keys.
   - *Mitigation:* Ensure `.env` is strictly in `.gitignore`. Mask API keys if logged. Do not write transcribed text to permanent disk storage unless explicitly requested in a configuration file.
4. **Cost Overruns:**
   - *Issue:* Leaving the bot on in a noisy room draining API credits.
   - *Mitigation:* Implement "Wake Word" functionality (e.g., Porcupine) where the expensive LLM/TTS is only triggered if the user specifically says "Hey Vaani". Include a hard-cap token counter that shuts the agent down if daily limits are breached.

---
