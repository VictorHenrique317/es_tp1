from faster_whisper import WhisperModel

WhisperModel("large-v3", device="cpu", compute_type="int8")
