from io import BytesIO
from elevenlabs import ElevenLabs


# ElevenLabs voices mapped to accents
# These are pre-made voices available on ElevenLabs with distinct accents
ACCENT_OPTIONS = {
    "US English (Rachel)": {
        "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel - American female
        "description": "Warm American female voice"
    },
    "US English (Josh)": {
        "voice_id": "TxGEqnHWrfWFTfGW9XjX",  # Josh - American male
        "description": "Deep American male voice"
    },
    "British English (Charlotte)": {
        "voice_id": "XB0fDUnXU5powFXDhCwa",  # Charlotte - British female
        "description": "Elegant British female voice"
    },
    "British English (George)": {
        "voice_id": "JBFqnCBsd6RMkjVDRZzb",  # George - British male
        "description": "Warm British male voice"
    },
    "Australian English (Matilda)": {
        "voice_id": "XrExE9yKIg1WjnnlVkGX",  # Matilda - Australian female
        "description": "Friendly Australian female voice"
    },
    "Indian English (Aria)": {
        "voice_id": "9BWtsMINqrJLrRacOk9x",  # Aria - can handle Indian accent
        "description": "Expressive female voice"
    },
}


def get_elevenlabs_client(api_key: str) -> ElevenLabs:
    """Create an ElevenLabs client with the provided API key."""
    return ElevenLabs(api_key=api_key)


def synthesize_speech(text: str, accent_name: str, api_key: str) -> BytesIO:
    """
    Synthesize speech audio from text using ElevenLabs with a chosen voice/accent.

    Args:
        text: The input text to speak.
        accent_name: A key from ACCENT_OPTIONS.
        api_key: ElevenLabs API key.

    Returns:
        BytesIO containing MP3 audio data.
    """
    if accent_name not in ACCENT_OPTIONS:
        raise ValueError(f"Unknown accent: {accent_name}")

    voice_id = ACCENT_OPTIONS[accent_name]["voice_id"]
    
    client = get_elevenlabs_client(api_key)
    
    # Generate audio using ElevenLabs
    audio_generator = client.text_to_speech.convert(
        voice_id=voice_id,
        text=text,
        model_id="eleven_multilingual_v2",  # Best quality multilingual model
        output_format="mp3_44100_128",
    )
    
    # Collect audio bytes from generator
    audio_bytes = BytesIO()
    for chunk in audio_generator:
        audio_bytes.write(chunk)
    audio_bytes.seek(0)
    
    return audio_bytes


def list_available_voices(api_key: str) -> list:
    """List all available voices from ElevenLabs (for debugging/exploration)."""
    client = get_elevenlabs_client(api_key)
    response = client.voices.get_all()
    return [(v.voice_id, v.name, v.labels) for v in response.voices]
