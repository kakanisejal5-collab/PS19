import io
import speech_recognition as sr


def transcribe_audio(audio_bytes: bytes) -> tuple[bool, str]:
    """
    Converts raw WAV audio bytes into readable text using SpeechRecognition.
    """
    if not audio_bytes or len(audio_bytes) < 100:
        return False, "Empty recording detected. Please speak clearly into the microphone and try again."

    recognizer = sr.Recognizer()

    try:
        audio_stream = io.BytesIO(audio_bytes)
        with sr.AudioFile(audio_stream) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.2)
            audio_data = recognizer.record(source)

        transcribed_text = recognizer.recognize_google(audio_data)

        if not transcribed_text.strip():
            return False, "No speech detected in the recording. Please try again."

        return True, transcribed_text.strip()

    except sr.UnknownValueError:
        return False, "Could not understand the audio. Please speak more clearly or reduce background noise."
    except sr.RequestError as e:
        return False, f"Speech recognition service unavailable. Check your internet connection. (Details: {e})"
    except Exception as e:
        return False, f"Unexpected audio processing error: {str(e)}"
