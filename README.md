
# 🎙️ AI Accent Shifter

An end-to-end demo app that:
1. Takes an uploaded English speech audio clip
2. Uses an AI ASR model (Whisper) to transcribe it to text
3. Re-speaks the same text using TTS in a user-selected English accent (US, UK, Australian, Indian, etc.)

Built with **Python**, **Streamlit**, **Whisper (openai-whisper)**, and **gTTS**.

---

## 🚀 Features

- Upload audio in WAV / MP3 / M4A / OGG / FLAC
- Transcription using a deep learning ASR model
- Accent selection from a list of English accents
- Playback of original and converted audio
- Downloadable MP3 of the converted speech

---

## 🧱 Project Structure

```text
ai_accent_shifter/
├── app.py           # Streamlit front-end and app logic
├── asr.py           # Whisper ASR model loading and transcription helpers
├── tts.py           # gTTS-based accent TTS helpers and accent config
├── requirements.txt # Python dependencies
└── README.md        # This file
```

---

## 🛠️ Setup

1. **Create and activate a virtual environment** (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
# or:
# .venv\Scripts\activate  # Windows
```

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

> ℹ️ Note: `openai-whisper` requires `ffmpeg` installed on your system.

- macOS (Homebrew):

```bash
brew install ffmpeg
```

- Ubuntu / Debian:

```bash
sudo apt-get install ffmpeg
```

- Windows:  
Download from the official FFmpeg site or use a package manager (e.g. `choco install ffmpeg`).

---

## ▶️ Running the App

From the `ai_accent_shifter` folder, run:

```bash
streamlit run app.py
```

Then open the local URL that Streamlit prints in your terminal (usually `http://localhost:8501`).

---

## 💡 How It Works (High-Level)

1. **ASR (Automatic Speech Recognition)**  
   - `asr.py` uses `openai-whisper` to load a pre-trained deep learning model.
   - Your uploaded audio is passed through the model to produce a text transcript.

2. **TTS (Text-to-Speech)**  
   - `tts.py` defines a set of English accent options via `gTTS` configuration.
   - The same text is synthesized into speech using the selected accent configuration.

3. **Streamlit Front-End**  
   - `app.py` connects these pieces:
     - audio upload widget
     - accent selection dropdown
     - transcription display
     - playback and download of the converted MP3.

---

## 🔒 Notes & Limitations

- This project is for **educational and demo purposes**.
- It does **not** preserve your original voice; it only preserves your *words* and re-synthesizes them in different accents.
- Audio quality and accent realism depend on the underlying TTS and may vary.

---

Enjoy exploring accents with AI! 🎧
