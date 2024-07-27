import os
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import streamlit_authenticator as stauth

names = ['John Smith', 'Rebecca Briggs']
usernames = ['jsmith', 'rbriggs']
passwords = ['$2b$12$ikUrwI2x2hpp6Geu1jvkCuAWDI8aCRSC6hlTQik1Pj6P7t1anywc.', '$2b$12$dlr.rPEzKG.xEUaTB/mk1.hlZyCsoUYZ3wCBmtRTWgLQZsoaPEOyG']

#hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(names, usernames, passwords,
    'some_cookie_name', 'some_signature_key')

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')
    st.title('Some content')
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')