from io import BytesIO

import openai
import speech_recognition as sr
from pydub import AudioSegment

from config import Config

openai.api_key = Config.OPENAI_API_KEY
AudioSegment.converter = "ffmpeg/ffmpeg.exe"


def speech_to_text(audio: BytesIO):

    r = sr.Recognizer()
    sound = AudioSegment.from_file(audio, format="wav")
    to_wav = BytesIO()
    sound.export(to_wav, format="wav")
    to_wav.seek(0)
    with sr.AudioFile(to_wav) as source:
        audio = r.record(source)
    text = r.recognize_google(audio)
    return text


def ask_chat_gpt(prompt: str):
    print(prompt)
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt + "\nStudent question: " + prompt + "\n",
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(response)
    return response.choices[0].text.strip()
