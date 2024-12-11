import streamlit as st
from pydub import AudioSegment
import speech_recognition as sr
import os
from openai import OpenAI

os.environ["OPENAI_API_KEY"] = "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"
client = OpenAI(api_key = "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")

st.title("Audio Recorder")
audio_file = st.file_uploader('Upload', type=['mp3', 'wav', 'm4a'])
if audio_file:
    st.audio(audio_file)
    st.title('Audio Transcript')
    transcription = client.audio.transcriptions.create(
        model='whisper-1',
        file = audio_file,
        prompt = 'Descreva a transcrição para o audio em questão'

    )