import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from faster_whisper import WhisperModel

model = WhisperModel("base")

def audio_to_text(audio_path: str) -> str:
    segments, _ = model.transcribe(audio_path)
    text = ""
    for segment in segments:
        text += segment.text
    return text.strip()