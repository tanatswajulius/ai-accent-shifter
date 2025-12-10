
import whisper


def load_asr_model(model_name: str = "base"):
    """
    Load a Whisper ASR model.

    Args:
        model_name: One of ["tiny", "base", "small", "medium", "large"].

    Returns:
        Loaded Whisper model.
    """
    return whisper.load_model(model_name)


def transcribe_audio_file(model, audio_path: str, language: str = "en") -> str:
    """
    Transcribe an audio file to text using a Whisper model.

    Args:
        model: Loaded Whisper model.
        audio_path: Path to the audio file.
        language: Language code for transcription (e.g. "en").

    Returns:
        Transcribed text.
    """
    result = model.transcribe(audio_path, language=language)
    return result.get("text", "").strip()
