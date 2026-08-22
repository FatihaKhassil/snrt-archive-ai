import os
import httpx

from groq import AsyncGroq


class LLMService:

    def __init__(self):

        # ============================================================
        # PROVIDER
        # ============================================================

        self.provider = os.getenv(
            "LLM_PROVIDER",
            "ollama"
        ).lower().strip()

        # ============================================================
        # OLLAMA
        # ============================================================

        self.ollama_url = os.getenv(
            "OLLAMA_BASE_URL",
            "http://ollama:11434"
        )

        self.ollama_model = os.getenv(
            "OLLAMA_MODEL",
            "llama3.1"
        )

        # ============================================================
        # GROQ
        # ============================================================

        self.groq_api_key = os.getenv(
            "GROQ_API_KEY"
        )

        self.groq_model = os.getenv(
            "GROQ_MODEL",
            "llama-3.3-70b-versatile"
        )

        self.groq_client = None

        if self.provider == "groq":

            if not self.groq_api_key:
                raise RuntimeError(
                    "GROQ_API_KEY is not configured."
                )

            self.groq_client = AsyncGroq(
                api_key=self.groq_api_key
            )

        # ============================================================
        # VALIDATION
        # ============================================================

        if self.provider not in ("ollama", "groq"):

            raise ValueError(
                f"Unsupported LLM_PROVIDER: {self.provider}. "
                f"Use 'ollama' or 'groq'."
            )

        print(
            "\n========================================",
            flush=True
        )

        print(
            "🤖 LLM SERVICE INITIALIZED",
            flush=True
        )

        print(
            f"Provider : {self.provider}",
            flush=True
        )

        if self.provider == "ollama":

            print(
                f"Model    : {self.ollama_model}",
                flush=True
            )

            print(
                f"URL      : {self.ollama_url}",
                flush=True
            )

        else:

            print(
                f"Model    : {self.groq_model}",
                flush=True
            )

            print(
                "Provider : Groq API",
                flush=True
            )

        print(
            "========================================\n",
            flush=True
        )

    # ============================================================
    # PUBLIC METHOD
    # ============================================================

    async def generate(
        self,
        prompt: str
    ) -> str:

        if not prompt or not prompt.strip():

            print(
                "❌ LLM : prompt vide",
                flush=True
            )

            return ""

        if self.provider == "ollama":

            return await self._generate_ollama(prompt)

        elif self.provider == "groq":

            return await self._generate_groq(prompt)

        raise RuntimeError(
            f"Unsupported LLM provider: {self.provider}"
        )

    # ============================================================
    # OLLAMA
    # ============================================================

    async def _generate_ollama(
        self,
        prompt: str
    ) -> str:

        final_prompt = f"""
Tu es un assistant intelligent spécialisé dans la recherche
dans les archives audiovisuelles de la SNRT.

Tu dois répondre UNIQUEMENT à partir du contexte fourni.

================ QUESTION + CONTEXTE ================

{prompt}

================ FIN DU CONTEXTE ====================

RÈGLES IMPORTANTES :

1. Identifie d'abord la question de l'utilisateur.

2. Analyse attentivement tous les passages du contexte.

3. Cherche l'information demandée dans les passages.

4. Si un passage contient directement la réponse,
   utilise cette information.

5. Si plusieurs passages sont pertinents,
   combine uniquement les informations utiles.

6. Ignore complètement les documents qui ne répondent
   pas à la question.

7. N'invente aucune information.

8. N'utilise aucune connaissance extérieure au contexte.

9. Réponds dans la même langue que la question.

10. Si la question est en arabe, réponds en arabe.

11. Si la réponse existe dans le contexte,
    réponds directement et clairement.

12. Ne réponds jamais avec une réponse vide.

13. Si l'information demandée n'existe réellement
    dans aucun passage, réponds exactement :

لم أجد هذه المعلومة في الأرشيف.

14. Ne parle jamais de ChromaDB, embeddings, RAG,
    Ollama, Groq ou de l'architecture technique.

15. Donne directement la réponse.

================ RÉPONSE =================
"""

        print(
            "\n========== OLLAMA REQUEST ==========",
            flush=True
        )

        print(
            f"Model : {self.ollama_model}",
            flush=True
        )

        print(
            f"Prompt length : {len(final_prompt)} characters",
            flush=True
        )

        url = f"{self.ollama_url}/api/generate"

        try:

            async with httpx.AsyncClient(
                timeout=300
            ) as client:

                response = await client.post(
                    url,
                    json={
                        "model": self.ollama_model,
                        "prompt": final_prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.1,
                            "top_p": 0.9,
                            "num_predict": 300,
                            "repeat_penalty": 1.1
                        }
                    }
                )

            print(
                f"Ollama status : {response.status_code}",
                flush=True
            )

            response.raise_for_status()

            data = response.json()

            answer = (
                data.get("response")
                or ""
            ).strip()

            print(
                "\n========== OLLAMA ANSWER ==========",
                flush=True
            )

            print(
                answer,
                flush=True
            )

            print(
                "====================================\n",
                flush=True
            )

            return answer

        except Exception as e:

            print(
                f"❌ Ollama error : {str(e)}",
                flush=True
            )

            return ""

    # ============================================================
    # GROQ
    # ============================================================

    async def _generate_groq(
        self,
        prompt: str
    ) -> str:

        if self.groq_client is None:

            raise RuntimeError(
                "Groq client is not initialized."
            )

        system_prompt = """
Tu es un assistant intelligent spécialisé dans la recherche
dans les archives audiovisuelles de la SNRT.

Tu réponds uniquement à partir du contexte fourni par
l'application.

RÈGLES :

1. Analyse attentivement le contexte.

2. Identifie l'information demandée par la question.

3. Utilise uniquement les passages pertinents.

4. Ignore les passages qui ne répondent pas à la question.

5. Si un passage contient la réponse, utilise-le directement.

6. Si plusieurs passages sont pertinents, combine-les
   uniquement lorsqu'ils apportent réellement une information
   complémentaire.

7. N'invente aucune information.

8. N'utilise aucune connaissance extérieure au contexte.

9. Réponds dans la même langue que la question.

10. Si la question est en arabe, réponds en arabe.

11. Si la question est en français, réponds en français.

12. Donne une réponse naturelle et complète.

13. Pour une question simple, une à trois phrases suffisent.

14. Pour une question complexe, donne davantage de détails
    uniquement si le contexte le permet.

15. Ne réponds jamais uniquement par un nom si le contexte
    permet de donner une explication.

16. Ne répète pas la question.

17. Ne parle jamais de ChromaDB, embeddings, RAG,
    Ollama, Groq ou de l'architecture technique.

18. Si l'information demandée n'existe réellement
    dans aucun passage, réponds exactement :

لم أجد هذه المعلومة في الأرشيف.

19. Ne retourne jamais une réponse vide.
"""

        user_prompt = f"""
================ QUESTION ET CONTEXTE ================

{prompt}

================ FIN DU CONTEXTE ======================

Réponds maintenant à la question de l'utilisateur.
"""

        print(
            "\n========== GROQ REQUEST ==========",
            flush=True
        )

        print(
            f"Model : {self.groq_model}",
            flush=True
        )

        print(
            f"Prompt length : {len(user_prompt)} characters",
            flush=True
        )

        try:

            completion = await self.groq_client.chat.completions.create(

                model=self.groq_model,

                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],

                temperature=0.1,

                max_tokens=300,

                top_p=0.9,

                stream=False
            )

            answer = (
                completion
                .choices[0]
                .message
                .content
                or ""
            ).strip()

            print(
                "\n========== GROQ ANSWER ==========",
                flush=True
            )

            print(
                answer,
                flush=True
            )

            print(
                "=================================\n",
                flush=True
            )

            if not answer:

                print(
                    "⚠️ GROQ a retourné une réponse vide",
                    flush=True
                )

                return ""

            return answer

        except Exception as e:

            print(
                f"❌ Groq error : {str(e)}",
                flush=True
            )

            return ""