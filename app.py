import streamlit as st
from speech_to_text import transcribe_audio
from llm_service import get_gemini_response
from text_to_speech import text_to_speech_bytes

st.set_page_config(
    page_title="Voice Assistant with LLM",
    page_icon="🎙️",
    layout="centered",
)

st.markdown(
    """
    <style>
    .main-header {
        text-align: center;
        padding-bottom: 10px;
    }
    .stAudio {
        margin-top: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_audio_id" not in st.session_state:
    st.session_state.last_audio_id = None


def process_user_query(user_text: str):
    st.session_state.messages.append({
        "role": "user",
        "content": user_text,
        "audio": None,
    })

    with st.spinner("Thinking with Gemini Flash..."):
        llm_success, llm_reply = get_gemini_response(
            user_prompt=user_text,
            chat_history=st.session_state.messages[:-1],
        )

    if not llm_success:
        st.error(llm_reply)
        return

    with st.spinner("Generating voice response..."):
        tts_success, audio_result = text_to_speech_bytes(llm_reply)

    audio_bytes = audio_result if tts_success else None
    if not tts_success:
        st.warning(f"Text reply generated, but audio failed: {audio_result}")

    st.session_state.messages.append({
        "role": "assistant",
        "content": llm_reply,
        "audio": audio_bytes,
    })


st.markdown("<h1 class='main-header'>🎙️ Voice Assistant with LLM</h1>", unsafe_allow_html=True)
st.caption("Speak into your microphone or type below to chat with Gemini Flash and hear spoken answers.")

with st.sidebar:
    st.header("Student Details")
    st.markdown(
        """
        - **Name:** Sejal Kakani
        - **Class:** LY Core 2, MIT SOC
        - **Enrollment:** ADT23SOCB1003
        - **Roll No:** 19 | **PS19**
        """
    )
    st.divider()
    st.header("Controls & Info")
    st.markdown(
        """
        **How to use:**
        1. Click the **Microphone icon** to record your question.
        2. Click **Stop** when finished.
        3. Or type your question in the text box and click **Submit**.
        """
    )
    st.divider()
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_audio_id = None
        st.rerun()

st.subheader("Ask a Question")

tab_voice, tab_text = st.tabs(["🎤 Voice Input", "⌨️ Text Input"])

with tab_voice:
    st.info("Tip: Allow browser microphone permission when prompted. Speak clearly and click stop.")
    recorded_audio = st.audio_input("Record your voice message")

    if recorded_audio is not None:
        audio_bytes = recorded_audio.getvalue()
        current_audio_id = hash(audio_bytes)

        if current_audio_id != st.session_state.last_audio_id:
            st.session_state.last_audio_id = current_audio_id

            with st.spinner("Transcribing your voice..."):
                stt_success, stt_result = transcribe_audio(audio_bytes)

            if stt_success:
                st.success(f"**Transcribed Text:** {stt_result}")
                process_user_query(stt_result)
                st.rerun()
            else:
                st.error(stt_result)

with tab_text:
    with st.form(key="text_input_form", clear_on_submit=True):
        user_typed_text = st.text_input(
            "Type your question here:",
            placeholder="e.g., Explain artificial intelligence in simple terms...",
        )
        submit_button = st.form_submit_button("Submit", type="primary")

        if submit_button:
            if user_typed_text.strip():
                process_user_query(user_typed_text.strip())
                st.rerun()
            else:
                st.warning("Please enter a valid question before clicking Submit.")

st.divider()

st.subheader("Conversation History")

if not st.session_state.messages:
    st.markdown("*No messages yet. Record your voice or type a question above to start!*")
else:
    for idx, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            if msg["role"] == "user":
                st.markdown(f"**You:** {msg['content']}")
            else:
                st.markdown(f"**Assistant:** {msg['content']}")
                if msg.get("audio"):
                    is_latest = idx == len(st.session_state.messages) - 1
                    st.audio(msg["audio"], format="audio/mp3", autoplay=is_latest)
