import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

def get_transcript(video_url):
    try:
        video_id = video_url.split("v=")[-1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([t["text"] for t in transcript])
        return text
    except Exception as e:
        return f"Error: {str(e)}"

def summarize(text):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You summarize YouTube transcripts in a clear and concise way."},
            {"role": "user", "content": f"Please summarize the following transcript:\n\n{text}"}
        ],
        temperature=0.5,
        max_tokens=800
    )
    return response.choices[0].message.content

st.title("🎥 YouTube Video Summarizer")
video_url = st.text_input("Enter YouTube video URL:")

if st.button("Summarize") and video_url:
    with st.spinner("Fetching transcript and summarizing..."):
        transcript = get_transcript(video_url)
        if transcript.startswith("Error"):
            st.error(transcript)
        else:
            summary = summarize(transcript)
            st.subheader("📌 Summary:")
            st.write(summary)
