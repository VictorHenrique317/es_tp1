from faster_whisper import WhisperModel
from langchain.llms import Ollama

model_whisper = WhisperModel("large-v3", device="cpu", compute_type="int8")
model_ollama = Ollama(model="llama3.2:1b")
