# Packages
import hmac
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI

# OpenAI API Configuration
client = OpenAI(api_key=st.secrets["api_key"]) 

# Functions
def extract_transcript_details(youtube_video_url):
    """
    Extract the transcript from a YouTube video and return it as a string.
    """
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([item["text"] for item in transcript_data])
        return transcript
    except Exception as e:
        raise e

def generate_openai_response(transcript_text, prompt, model="gpt-4o"):
    """
    Generate response using OpenAI's NEW 1.0.0+ syntax
    """
    try:
        response = client.chat.completions.create(  # Updated method chain
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert at interpreting and processing transcripts into relatable summaries."},
                {"role": "user", "content": f"{prompt}\n\nTRANSCRIPT:\n{transcript_text}"}
            ]
        )
        return response.choices[0].message.content  # Updated response access
    except Exception as e:
        return f"Error: {str(e)}"

def convert_youtube_link(link):
    """
    Convert a shortened or mobile YouTube link to the standard desktop format.
    """
    if "youtube.com/watch" in link:
        return link
    elif "youtu.be" in link:
        video_id = link.split('/')[-1].split('?')[0]
        return f"https://www.youtube.com/watch?v={video_id}"
    return "Invalid YouTube link"

# Authentication
def check_password():
    """
    Validate the password entered by the user.
    """
    def password_entered():
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state and not st.session_state["password_correct"]:
        st.error("😕 Password incorrect")
    return False

# Main App
if not check_password():
    st.stop()

# App Design
st.title("YouTube Video Summarizer")
st.markdown("<h6>Built by: Jake Waddle<br>AI: OpenAI</h6>", unsafe_allow_html=True)
st.markdown('<h4>Copy and paste a YouTube video link into the input box below</h4>', unsafe_allow_html=True)

# Input: YouTube Link
raw_youtube_link = st.text_input("Paste YouTube link here")

if raw_youtube_link:
    converted_youtube_link = convert_youtube_link(raw_youtube_link)
    if converted_youtube_link != "Invalid YouTube link":
        video_id = converted_youtube_link.split("=")[1]
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
        st.write(f"Converted Link: {converted_youtube_link}")
    else:
        st.error("Invalid YouTube link provided.")

# Input: Custom Prompt
st.markdown('<h4>Enter your question or prompt about the video</h4>', unsafe_allow_html=True)
custom_prompt = st.text_area(
    "Enter prompt below",
    value="Write a question or ask for a summary about this video, and AI will respond."
)

# Button: Generate Response
if st.button("Get Response"):
    if raw_youtube_link:
        try:
            transcript_text = extract_transcript_details(converted_youtube_link)
            if transcript_text:
                response = generate_openai_response(transcript_text, custom_prompt)
                st.markdown("<h5>Response</h5>", unsafe_allow_html=True)
                st.write(response)
            else:
                st.error("Unable to fetch or parse transcript from the video.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please provide a valid YouTube link.")
