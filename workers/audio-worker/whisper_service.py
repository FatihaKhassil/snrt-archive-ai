import whisper


class WhisperService:

    def __init__(self):

        print(
            "⏳ Loading Whisper model...",
            flush=True
        )

        self.model = whisper.load_model("base")

        print(
            "✅ Whisper model loaded",
            flush=True
        )


    def transcribe(self, audio_path):

        result = self.model.transcribe(
            audio_path
        )

        return result["text"]