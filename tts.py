
from io import BytesIO

from gtts import gTTS


ACCENT_OPTIONS = {
    "US English": {"lang": "en", "tld": "com"},
    "UK English": {"lang": "en", "tld": "co.uk"},
    "Australian English": {"lang": "en", "tld": "com.au"},
    "Indian English": {"lang": "en", "tld": "co.in"},
    "Irish English": {"lang": "en", "tld": "ie"},
    "South African English": {"lang": "en", "tld": "co.za"},
}


def synthesize_speech(text: str, accent_name: str) -> BytesIO:
    """
    Synthesize speech audio from text using gTTS with a chosen accent.

    Args:
        text: The input text to speak.
        accent_name: A key from ACCENT_OPTIONS.

    Returns:
        BytesIO containing MP3 audio data.
    """
    if accent_name not in ACCENT_OPTIONS:
        raise ValueError(f"Unknown accent: {accent_name}")

    cfg = ACCENT_OPTIONS[accent_name]
    tts = gTTS(text=text, lang=cfg["lang"], tld=cfg["tld"], slow=False)

    audio_bytes = BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes
