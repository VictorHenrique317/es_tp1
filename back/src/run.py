from llms import model_ollama, model_whisper

audio_file = "audio.mkv"
transcription_file = "transcription.txt"


with open(transcription_file, "a") as f:
    segments, info = model_whisper.transcribe(audio_file, beam_size=5, )
    for segment in segments:
        f.write(("%s\n" % (segment.text)))


text = ""
with open(transcription_file, "r") as f:
    text = f.read()
res = model_ollama.predict(f"explique o texto a seguir: {text}")
print(res)
