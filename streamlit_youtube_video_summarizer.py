import os
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import streamlit_authenticator as stauth

names = ['John Smith', 'Rebecca Briggs']
usernames = ['jsmith', 'rbriggs']
passwords = ['$2b$12$ikUrwI2x2hpp6Geu1jvkCuAWDI8aCRSC6hlTQik1Pj6P7t1anywc.', '$2b$12$dlr.rPEzKG.xEUaTB/mk1.hlZyCsoUYZ3wCBmtRTWgLQZsoaPEOyG']

#hashed_passwords = stauth.Hasher(passwords).generate()

# Create authenticator object
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Authenticate user
name, authentication_status, username = authenticator(location = "main")

if authentication_status:
    genai.configure(api_key=os.getenv("GEMINI_KEY"))

    # Function to extract transcript details
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

    # Function to generate content using Gemini
    def generate_gemini_content(transcript_text, prompt):
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt + transcript_text)
        return response.text

    # Streamlit app
    st.title("Jake's YouTube Video Summarizer")
    youtube_link = st.text_input("Enter YouTube Video Link:")

    if youtube_link:
        video_id = youtube_link.split("=")[1]
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

    # Text area for custom prompt input
    custom_prompt = st.text_area("Enter your custom prompt:", 
                                 value="""Welcome, Video Summarizer! Your task is to distill the essence of a given YouTube video transcript into expository essay format. 
                                          Your essay should capture the key points, timelines, and essential information within a 800-word limit. 
                                          Let's dive into the provided transcript and extract the vital details for our audience.""")

    # Button to trigger summary generation
    if st.button("Get Detailed Notes"):
        transcript_text = extract_transcript_details(youtube_link)

        if transcript_text:
            # Generate content using the custom prompt
            essay = generate_gemini_content(transcript_text, custom_prompt)
            
            # Display essay
            st.markdown("## Essay Form:")
            st.write(essay)

elif authentication_status == False:
    st.error("Username/password is incorrect")
elif authentication_status == None:
    st.warning("Please enter your username and password")
