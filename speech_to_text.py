from faster_whisper import WhisperModel

class STTModel:
    def __init__(self, model_size="small", device="cpu", compute_type="int8"):
        print(f"Загружаю модель faster-whisper '{model_size}'...")
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type, local_files_only=True)
        print("Модель готова.")

    def transcribe(self, audio_file):
        segments, info = self.model.transcribe(audio_file, beam_size=5, language="ru")
        full_text = " ".join([segment.text for segment in segments])
        return full_text.strip()