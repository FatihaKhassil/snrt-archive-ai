import json
import re

import requests

from model_factory import ModelFactory


class OllamaService:

    def __init__(self):

        self.url = "http://ollama:11434/api/generate"

        self.model = ModelFactory.get_model()


    def generate(
        self,
        prompt
    ):

        print(
            "📤 Sending HTTP request to Ollama...",
            flush=True
        )

        response = requests.post(

            self.url,

            json={

                "model": self.model,

                "format": "json",

                "prompt": prompt,

                "stream": False,

                "options": {

                    "num_predict": 250,

                    "temperature": 0.2

                }

            },

            timeout=600

        )

        print(
            "✅ HTTP response received",
            flush=True
        )

        response.raise_for_status()

        result = response.json()

        print(
            "✅ JSON response received",
            flush=True
        )

        print(
            "==========================",
            flush=True
        )

        print(
            result["response"],
            flush=True
        )

        print(
            "==========================",
            flush=True
        )

        print(
            "🔄 Extracting JSON...",
            flush=True
        )

        match = re.search(

            r"\{[\s\S]*\}",

            result["response"]

        )

        if not match:

            raise Exception(
                "No JSON object found."
            )

        parsed_result = json.loads(

            match.group()

        )

        print(
            "✅ JSON successfully parsed",
            flush=True
        )

        return parsed_result