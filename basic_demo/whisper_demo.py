from faster_whisper import WhisperModel

model_path = '../model/faster-whisper-v3'

model = WhisperModel(model_size_or_path=model_path, device="cuda", compute_type="float16", local_files_only = True)

segments, info = model.transcribe("temp_audio.mp3", beam_size=5)

print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))