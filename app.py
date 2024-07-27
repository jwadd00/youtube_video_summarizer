#packages 
import hmac
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

# google ai key
genai.configure(api_key=st.secrets["api_key"])

# functions
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript
    except Exception as e:
        raise e
        
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

# auth functions
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False

if not check_password():
    st.stop()  # Do not continue if check_password is not True.

# Streamlit app
st.title("YouTube Video Summarizer")
st.html("<h6>built by: jake waddle<br>ai: google-gemini</h6>")
st.html('<h4>COPY AND PASTE YOUTUBE VIDEO LINK INTO THE INPUT BOX BELOW</h4>')
youtube_link = st.text_input("copy link here")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

st.html('<h4>REMOVE THE DEFAULT VALUES BELOW AND ENTER YOUR OWN QUESTION OR PROMPT ABOUT THE VIDEO</h4>')
# Text area for custom prompt input
custom_prompt = st.text_area("enter prompt below", 
                                value="""write a question or something about this video and ai will respond\nexample: summarize this video and capture the key points, timelines, and essential information within a 800-word limit""")

# Button to trigger summary generation
if st.button("Get Response"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        # Generate content using the custom prompt
        essay = generate_gemini_content(transcript_text, custom_prompt)
        
        # Display essay
        st.html("<h5>Reponse</h5>")
        st.write(essay)