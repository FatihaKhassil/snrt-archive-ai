from prompt_builder import PromptBuilder
from ollama_service import OllamaService


class LLMService:

    def __init__(self):

        self.ollama = OllamaService()


    def process(
        self,
        text
    ):

        print(
            "📝 Building prompt...",
            flush=True
        )

        prompt = PromptBuilder.build(
            text
        )

        print(
            "🤖 Sending prompt to Ollama...",
            flush=True
        )

        result = self.ollama.generate(
            prompt
        )

        print(
            "✅ LLM processing completed",
            flush=True
        )

        return result