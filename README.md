# PS19 – Voice Assistant with LLM
**Submitted by:** Sejal Kakani | **Class:** LY Core 2, MIT SOC | **Enrollment:** ADT23SOCB1003 | **Roll No:** 19


## Features

- Record voice using Streamlit's microphone control
- Speech-to-text using SpeechRecognition with Google's online recognition service
- AI answers using the Gemini API
- Text-to-speech using gTTS
- Conversation history
- Text input as an alternative to voice
- Download generated MP3 replies

## Technology

- Python
- Streamlit
- SpeechRecognition
- Google Gemini (`google-genai`)
- gTTS
- python-dotenv

## Requirements

- Python 3.10 or newer
- Internet connection
- Microphone and browser microphone permission
- A Gemini API key

## Setup

1. Extract the ZIP file.
2. Open the extracted `PS19_Voice_Assistant` folder in VS Code.
3. Open a terminal in that folder.
4. Create and activate a virtual environment (recommended):

   **Windows**
   ```bash
   py -m venv venv
   venv\Scripts\activate
   ```

   **macOS/Linux**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

5. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Get a Gemini API key from Google AI Studio: https://aistudio.google.com/app/apikey
7. Copy `.env.example` and rename the copy to `.env`.
8. Open `.env` and replace `your_gemini_api_key_here` with your own key. Do not share or upload `.env`.

## Run the app

```bash
streamlit run app.py
```

Streamlit will show a local URL, usually `http://localhost:8501`. Open it in your browser.

## How to use

1. Allow microphone access when your browser asks.
2. Record a question in the voice input section.
3. Select **Transcribe and ask**.
4. Check the transcription and Gemini response.
5. Select **Generate spoken answer** to hear the reply.
6. Alternatively, type a question in the text input section.

## Sample tests

1. "What is artificial intelligence?"
2. "Explain cloud computing in simple words."
3. "Give me three tips to prepare for an exam."
4. "What is the difference between RAM and storage?"
5. "Tell me a short motivational message."

Check that voice transcription, the generated response, and spoken audio work. The speech recognition and gTTS services require internet access.

## Project structure

```text
PS19_Voice_Assistant/
├── app.py
├── text_to_speech.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── llm_servoce.py
└── speech_text.py
```

## Troubleshooting

- **Microphone not visible:** Use a supported browser, allow microphone permission, and reload the page.
- **Speech not recognized:** Speak clearly, reduce background noise, and record again.
- **Gemini API error:** Check the API key, internet connection, API availability, and model access.
- **gTTS error:** Check internet access and try again.
- **Module not found:** Activate the virtual environment and run `pip install -r requirements.txt`.

## GitHub safety

Commit `.env.example`, not `.env`. The `.gitignore` file excludes `.env` and virtual environments. Before publishing, confirm that no real API key is present in your files or commit history.

## Academic project

**Problem Statement:** Typing is slow or inconvenient for some users. This project provides a voice-based chatbot that converts speech into text, uses a Large Language Model to generate a response, and converts the response into audio.
