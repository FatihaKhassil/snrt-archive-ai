import os
import httpx

from groq import AsyncGroq


class LLMService:

    def __init__(self):

        # ============================================================
        # LLM PROVIDER
        # ============================================================

        self.provider = os.getenv(
            "LLM_PROVIDER",
            "ollama"
        ).lower().strip()

        # ============================================================
        # OLLAMA CONFIGURATION
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
        # GROQ CONFIGURATION
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

        if self.provider not in (
            "ollama",
            "groq"
        ):

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

    # ================================================================
    # PUBLIC METHOD
    # ================================================================

    async def generate(
        self,
        prompt: str
    ) -> str:

        if self.provider == "ollama":

            return await self._generate_ollama(
                prompt
            )

        if self.provider == "groq":

            return await self._generate_groq(
                prompt
            )

        raise RuntimeError(
            f"Unsupported LLM provider: {self.provider}"
        )

    # ================================================================
    # OLLAMA
    # ================================================================

    async def _generate_ollama(
        self,
        prompt: str
    ) -> str:

        final_prompt = f"""
{prompt}

========================
IMPORTANT
========================

La réponse ne doit jamais être uniquement un nom,
un mot ou une courte expression lorsque le contexte
permet de donner plus d'informations.

Donne une réponse complète et naturelle.

Pour une question simple concernant une personne,
un rôle ou un événement, donne au minimum 1 à 3 phrases
qui expliquent clairement la réponse à partir du contexte.

Exemple :

Question :
من كان قائد فريق ترس في اللعبة؟

Réponse insuffisante :
فور.

Réponse attendue :
كان فور قائد الفريق الذي كانت ترس ضمنه في اللعبة.
أما الفريق المنافس فكان بقيادة إريك.

Ne copie pas cet exemple.
Utilise uniquement les informations présentes
dans le contexte fourni.

Réponds maintenant à la question de l'utilisateur.
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

        url = (
            f"{self.ollama_url}/api/generate"
        )

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

                        "temperature": 0.2,

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

    # ================================================================
    # GROQ
    # ================================================================

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

Tu dois répondre uniquement à partir du contexte fourni
par l'application.

Règles :

1. Utilise uniquement les informations présentes dans le contexte.

2. N'invente aucune information.

3. Lis tous les passages avant de répondre.

4. Ignore les passages qui ne sont pas pertinents pour la question.

5. Si plusieurs passages contiennent des informations utiles,
   combine-les dans une réponse cohérente.

6. Donne une réponse complète et naturelle.

7. Ne réponds pas uniquement avec un nom ou un seul mot
   lorsque le contexte permet d'expliquer davantage.

8. Pour une question simple, réponds généralement avec
   une à trois phrases.

9. Pour une question complexe, donne une réponse plus détaillée
   lorsque cela est nécessaire.

10. Réponds dans la même langue que la question.

11. Si la question est en arabe, réponds en arabe.

12. Si la question est en français, réponds en français.

13. N'utilise aucune connaissance extérieure au contexte.

14. Si l'information demandée n'existe pas dans le contexte,
    réponds exactement :

    لم أجد هذه المعلومة في الأرشيف.

15. Ne parle pas de ChromaDB, embeddings, RAG, Ollama,
    Groq ou de l'architecture technique.

16. Ne répète pas la question.

17. Donne directement la réponse.
"""

        user_prompt = f"""
Voici le contexte extrait des archives SNRT :

================ CONTEXTE ================

{prompt}

============== FIN CONTEXTE ==============

Réponds maintenant à la question de l'utilisateur
en respectant toutes les règles.
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

            temperature=0.2,

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

        return answer