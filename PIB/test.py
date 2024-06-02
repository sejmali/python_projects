import streamlit as st
from gtts import gTTS
from moviepy.editor import *
import os

def text_to_audio(text, audio_file):
    tts = gTTS(text=text, lang='en')
    tts.save(audio_file)

def combine_audio_with_video(audio_file, video_file, output_file):
    video_clip = VideoFileClip(video_file)
    audio_clip = AudioFileClip(audio_file)
    
    video_clip = video_clip.set_audio(audio_clip)
    video_clip.write_videofile(output_file, codec='libx264', audio_codec='aac')
    
    # Close the clips
    video_clip.close()
    audio_clip.close()

def main():
    st.title("Text-to-Video Generator")

    # Text input
    text = st.text_area("Enter your text:", "AI is playing a crucial role in medical research...")

    # Upload video
    uploaded_video = st.file_uploader("Upload a video file (MP4 format)", type=["mp4"])

    if st.button("Generate Video"):
        if uploaded_video:
            # Save uploaded video
            with open("input_video.mp4", "wb") as f:
                f.write(uploaded_video.read())

            # Convert text to audio
            text_to_audio(text, "audio.mp3")

            # Combine audio with video
            combine_audio_with_video("audio.mp3", "input_video.mp4", "output_video.mp4")

            # Remove temporary audio file
            os.remove("audio.mp3")

            # Display the output video
            st.video("output_video.mp4")
        else:
            st.error("Please upload a video file.")

if __name__ == "__main__":
    main()

