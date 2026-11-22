import io
import re
from gtts import gTTS


def clean_text_for_speech(text: str) -> str:
    """
    Removes markdown formatting characters so the TTS engine reads smoothly.
    """
    cleaned = re.sub(r"[*#_`~]", "", text)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


def text_to_speech_bytes(text: str, lang: str = "en") -> tuple[bool, bytes | str]:
    """
    Converts text into MP3 audio bytes using gTTS.
    """
    if not text or not text.strip():
        return False, "Cannot generate audio from empty text."

    try:
        spoken_text = clean_text_for_speech(text)
        tts = gTTS(text=spoken_text, lang=lang, slow=False)

        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        return True, audio_buffer.read()

    except Exception as e:
        return False, f"Text-to-Speech conversion failed. Check internet connectivity. (Details: {e})"
