#libraries
import os
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_KEY"))

# prompt
prompt = """Welcome, Video Summarizer!
            Your summary should capture the key points and essential information, presented in bullet points, within a 900-word limit.
            Focus on attitudes, actions, spiritual habits, biblical scripture, and practical next steps. 
            Let's dive into the provided transcript and extract the vital details for our audience.            
            """
            
prompt2 = """Welcome, Video Summarizer! Your task is to distill the essence of a given YouTube video transcript into expository essay format. 
             Your essay should capture the key points,timelines, and essential information within a 800-word limit. 
             Let's dive into the provided transcript and extract the vital details for our audience."""
             
prompt3 = """Welcome, Video Summarizer! Your task is to distill the essence of a given YouTube video transcript into expository essay format. 
             Your essay should capture the key points,timelines, and essential information within a 800-word limit. 
             Extract one key insight that can be directly correlated with biblical scripture and translatable to modern times - please use one example and provide the relating scripture. 
             Let's dive into the provided transcript and extract the vital details for our audience."""

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

def generate_gemini_content2(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response2 = model.generate_content(prompt2 + transcript_text)
    return response2.text

# treamlit
st.title(
    "Jake's YouTube Video Summarizer"
)
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

# Button to trigger summary generation
if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        # Generate summary using Gemini Pro
        #summary = generate_gemini_content(transcript_text, prompt)
        essay = generate_gemini_content2(transcript_text, prompt2)
        #essay = generate_gemini_content2(transcript_text, prompt3)
        #essay = generate_gemini_content2(transcript_text, custom_prompt)

        # Display summary
        #st.markdown("## Detailed Notes:")
        #st.write(summary)
        #st.markdown("## Essay Form:")
        st.write(essay)