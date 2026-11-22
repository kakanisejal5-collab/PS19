import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from local .env file if present
load_dotenv()


def get_api_key() -> str | None:
    """
    Retrieves GEMINI_API_KEY from local .env/environment or Streamlit Cloud Secrets.
    """
    key = os.getenv("GEMINI_API_KEY")
    if key and key != "your_gemini_api_key_here":
        return key

    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    return None


def get_gemini_response(user_prompt: str, chat_history: list[dict]) -> tuple[bool, str]:
    """
    Sends the user's message and recent conversation history to Gemini Flash.
    """
    api_key = get_api_key()

    if not api_key:
        return False, "API Key missing! Add GEMINI_API_KEY in Streamlit App Settings -> Secrets (or .env locally)."

    if not user_prompt or not user_prompt.strip():
        return False, "Input text is empty. Please say or type a question."

    try:
        client = genai.Client(api_key=api_key)

        formatted_contents = []
        for msg in chat_history[-6:]:
            role = "user" if msg["role"] == "user" else "model"
            formatted_contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=msg["content"])]
                )
            )

        formatted_contents.append(
            types.Content(
                role=role if False else "user",
                parts=[types.Part.from_text(text=user_prompt)]
            )
        )

        config = types.GenerateContentConfig(
            system_instruction=(
                "You are a friendly, intelligent AI Voice Assistant. "
                "Provide clear, accurate, and conversational answers. "
                "Keep responses concise (2 to 4 sentences) and avoid heavy markdown symbols "
                "like asterisks or bullet tables so your answer sounds natural when spoken aloud."
            ),
            temperature=0.7,
            max_output_tokens=300,
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=formatted_contents,
            config=config,
        )

        if response and response.text:
            return True, response.text.strip()
        return False, "Gemini returned an empty response. Please try asking differently."

    except Exception as e:
        error_msg = str(e).lower()
        if "api_key" in error_msg or "403" in error_msg or "401" in error_msg:
            return False, "Invalid Gemini API key. Please verify your key in Google AI Studio."
        if "quota" in error_msg or "429" in error_msg:
            return False, "API rate limit exceeded. Please wait a moment and try again."
        if "connection" in error_msg or "network" in error_msg or "getaddrinfo" in error_msg:
            return False, "Network error: Unable to reach Gemini servers. Check your internet connection."
        return False, f"Gemini API Error: {str(e)}"
