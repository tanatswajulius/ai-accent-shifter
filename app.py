import os
import tempfile
from io import BytesIO

import streamlit as st

from asr import load_asr_model, transcribe_audio_file
from tts import synthesize_speech, ACCENT_OPTIONS


st.set_page_config(page_title="AI Accent Shifter", page_icon="🎙️")

st.title("🎙️ AI Accent Shifter")
st.write(
    "Upload an English speech audio clip, choose a target accent, and this app will:\n"
    "1. Transcribe your speech using an ASR model (Whisper)\n"
    "2. Re-speak the same text using a natural AI voice with your chosen accent."
)

# Sidebar for API key
st.sidebar.header("⚙️ Configuration")
api_key = st.sidebar.text_input(
    "ElevenLabs API Key",
    type="password",
    help="Get your free API key at https://elevenlabs.io",
    placeholder="Enter your API key..."
)

if not api_key:
    st.sidebar.warning("⚠️ Please enter your ElevenLabs API key to use the TTS feature.")
    st.sidebar.markdown(
        """
        **How to get a free API key:**
        1. Go to [elevenlabs.io](https://elevenlabs.io)
        2. Sign up for a free account
        3. Go to Profile → API Key
        4. Copy and paste it here
        
        *Free tier includes 10,000 characters/month*
        """
    )


@st.cache_resource
def get_asr_model():
    # You can change "base" to "small", "medium", etc. if you have more compute
    return load_asr_model("base")


model = get_asr_model()

st.markdown("### 1. Upload your audio")
uploaded_file = st.file_uploader(
    "Supported formats: WAV, MP3, M4A, OGG, FLAC",
    type=["wav", "mp3", "m4a", "ogg", "flac"],
)

st.markdown("### 2. Choose target voice & accent")
accent_name = st.selectbox(
    "Target voice:",
    list(ACCENT_OPTIONS.keys()),
    format_func=lambda x: f"{x} - {ACCENT_OPTIONS[x]['description']}"
)

st.markdown("### 3. Convert")
convert_button = st.button("🎤 Convert to selected accent", type="primary")

transcript_placeholder = st.empty()
original_audio_placeholder = st.empty()
output_audio_placeholder = st.empty()
download_placeholder = st.empty()

if convert_button:
    if not api_key:
        st.error("❌ Please enter your ElevenLabs API key in the sidebar first.")
    elif uploaded_file is None:
        st.error("❌ Please upload an audio file first.")
    else:
        # Show original audio player
        original_audio_placeholder.markdown("#### 🎵 Original Audio")
        original_audio_placeholder.audio(uploaded_file, format="audio/*")

        # Save uploaded file to a temporary path
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        # Transcribe
        with st.spinner("🔍 Transcribing audio with Whisper..."):
            try:
                text = transcribe_audio_file(model, tmp_path, language="en")
            except Exception as e:
                st.error(f"Error during transcription: {e}")
                text = ""

        # Clean up temp file
        try:
            os.remove(tmp_path)
        except OSError:
            pass

        if not text:
            st.error("Could not extract any text from the audio. Try a clearer or longer clip.")
        else:
            transcript_placeholder.markdown("#### 📝 Transcribed Text")
            transcript_placeholder.info(text)

            with st.spinner(f"🎙️ Generating natural speech with {accent_name.split('(')[0].strip()} accent..."):
                try:
                    audio_bytes = synthesize_speech(text, accent_name, api_key)
                except Exception as e:
                    st.error(f"Error during TTS synthesis: {e}")
                    audio_bytes = None

            if audio_bytes is not None:
                output_audio_placeholder.markdown(f"#### 🔊 Output Audio ({accent_name})")
                output_audio_placeholder.audio(audio_bytes, format="audio/mp3")

                # Reset stream position for download
                audio_bytes.seek(0)
                download_placeholder.download_button(
                    label="⬇️ Download converted audio (MP3)",
                    data=audio_bytes,
                    file_name="accent_shifted_output.mp3",
                    mime="audio/mpeg",
                )
                
                st.success("✅ Conversion complete! Your audio has been transformed with a natural-sounding voice.")
