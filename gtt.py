from gtts import gTTS

def text_to_audio(text: str, output_path: str):
    tts = gTTS(text)
    tts.save(output_path)