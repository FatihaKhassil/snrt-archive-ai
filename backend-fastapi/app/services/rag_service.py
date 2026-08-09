from app.services.chroma_service import ChromaService
from app.services.llm_service import LLMService
from app.repositories.document_repository import DocumentRepository


class RagService:

    def __init__(self):
        self.chroma_service = ChromaService()
        self.llm_service = LLMService()
        self.document_repository = DocumentRepository()

    async def ask(self, question: str) -> dict:
        """
        Recherche les passages pertinents dans ChromaDB,
        construit un contexte pour le LLM,
        génère une réponse naturelle,
        puis récupère les documents sources depuis MongoDB.
        """

        print("\n========== RAG REQUEST ==========")
        print(f"Question : {question}")

        # ============================================================
        # 1. RECHERCHE SEMANTIQUE
        # ============================================================

        results = await self.chroma_service.search(
            question,
            k=5
        )

        print(
            f"Chunks retournés par Chroma : {len(results)}"
        )

        if not results:
            return {
                "answer": "لم أجد هذه المعلومة في الأرشيف.",
                "chunks": 0,
                "sources": []
            }

        # ============================================================
        # 2. SUPPRESSION DES DOUBLONS
        # ============================================================

        unique_results = []
        seen_texts = set()

        for result in results:

            if isinstance(result, dict):

                text = (
                    result.get("text")
                    or result.get("page_content")
                    or result.get("content")
                    or ""
                )

                metadata = result.get(
                    "metadata",
                    {}
                ) or {}

            else:

                text = getattr(
                    result,
                    "page_content",
                    ""
                )

                metadata = getattr(
                    result,
                    "metadata",
                    {}
                ) or {}

            text = str(text).strip()

            if not text:
                continue

            if text in seen_texts:
                continue

            seen_texts.add(text)

            unique_results.append(
                {
                    "text": text,
                    "metadata": metadata
                }
            )

            # On garde au maximum 3 passages pertinents.
            if len(unique_results) >= 3:
                break

        print(
            f"Chunks utilisés : {len(unique_results)}"
        )

        if not unique_results:
            return {
                "answer": "لم أجد هذه المعلومة في الأرشيف.",
                "chunks": 0,
                "sources": []
            }

        # ============================================================
        # 3. AFFICHER LES CHUNKS
        # ============================================================

        print(
            "\n========== CHUNKS ==========\n"
        )

        document_ids = []

        for index, item in enumerate(
            unique_results,
            start=1
        ):

            text = item["text"]
            metadata = item["metadata"]

            print(
                f"----- Chunk {index} -----"
            )

            print(
                f"Metadata: {metadata}"
            )

            print(text)
            print()

            document_id = metadata.get(
                "document_id"
            )

            if document_id:
                document_ids.append(
                    str(document_id)
                )

        # Supprimer les doublons d'IDs.
        document_ids = list(
            dict.fromkeys(
                document_ids
            )
        )

        # ============================================================
        # 4. CONSTRUIRE LE CONTEXTE
        # ============================================================

        MAX_CONTEXT = 4000

        context_parts = []
        current_length = 0

        for index, item in enumerate(
            unique_results,
            start=1
        ):

            text = item["text"]

            remaining = (
                MAX_CONTEXT
                - current_length
            )

            if remaining <= 0:
                break

            # Éviter de couper inutilement un passage.
            if len(text) > remaining:

                text = text[:remaining]

            passage = f"""
--- PASSAGE {index} ---
{text}
--- FIN PASSAGE {index} ---
"""

            context_parts.append(
                passage
            )

            current_length += len(
                passage
            )

        context = "\n".join(
            context_parts
        )

        # ============================================================
        # 5. PROMPT RAG
        # ============================================================

        prompt = f"""
أنت مساعد ذكي متخصص في البحث داخل أرشيف SNRT.

مهمتك هي الإجابة عن سؤال المستخدم اعتماداً حصراً على المعلومات الموجودة في السياق.

القواعد:

- استخدم المعلومات الموجودة في السياق فقط.
- لا تضف أي معلومة من معرفتك الخاصة.
- لا تخترع أي معلومة.
- إذا كانت المعلومات موجودة في السياق، يجب أن تستخدمها للإجابة.
- أجب بنفس لغة السؤال.
- أجب بطريقة طبيعية وواضحة ومترابطة.
- اجعل الإجابة كاملة وليست مجرد جزء من الجملة الموجودة في النص.
- أعد صياغة المعلومات بدلاً من نسخ النص حرفياً.
- حافظ على المعنى الأصلي للمعلومات.
- إذا كان السؤال عن حدث، اشرح باختصار ما حدث.
- إذا كان السؤال عن سبب، اذكر السبب بوضوح.
- إذا كان السؤال عن شخص، اذكر المعلومات المتعلقة به الموجودة في السياق فقط.
- إذا كانت الإجابة موزعة بين عدة مقاطع، اجمع المعلومات المرتبطة بالسؤال في إجابة واحدة.
- لا تكرر السؤال.
- لا تبدأ بعبارات مثل "وفقاً للنص" أو "حسب الوثيقة" إلا إذا كان ذلك ضرورياً.
- لا تستخدم كلمات أجنبية إذا لم تكن موجودة في السؤال أو السياق.
- لا تقل "لم أجد هذه المعلومة في الأرشيف" إذا كانت الإجابة موجودة في السياق.
- إذا كانت الإجابة غير موجودة فعلاً في السياق، قل فقط:
"لم أجد هذه المعلومة في الأرشيف."

السياق:

{context}

السؤال:

{question}

الإجابة:
"""

        print(
            "\n========== PROMPT ENVOYÉ À LLAMA =========="
        )

        print(prompt)

        print(
            "========== FIN PROMPT ==========\n"
        )

        # ============================================================
        # 6. APPEL DU LLM
        # ============================================================

        answer = await self.llm_service.generate(
            prompt
        )

        if answer is None:
            answer = ""

        answer = str(
            answer
        ).strip()

        print(
            "\n========== LLM ANSWER =========="
        )

        print(answer)

        # ============================================================
        # 7. RÉCUPÉRER LES DOCUMENTS SOURCES
        # ============================================================

        print(
            "\n========== SOURCE IDS =========="
        )

        print(document_ids)

        sources = []

        if document_ids:

            try:

                documents = await (
                    self.document_repository
                    .get_documents(
                        document_ids
                    )
                )

                print(
                    f"Documents MongoDB récupérés : {len(documents)}"
                )

                # Dictionnaire pour retrouver rapidement
                # un document par son ID.
                documents_by_id = {
                    str(document.get("_id")): document
                    for document in documents
                }

                for item in unique_results:

                    metadata = item["metadata"]
                    document_id = metadata.get(
                        "document_id"
                    )

                    if not document_id:
                        continue

                    document_id = str(
                        document_id
                    )

                    document = documents_by_id.get(
                        document_id
                    )

                    if not document:
                        print(
                            f"⚠️ Document MongoDB introuvable : "
                            f"{document_id}"
                        )
                        continue

                    filename = (
                        document.get(
                            "original_filename"
                        )
                        or document.get(
                            "filename"
                        )
                        or document.get(
                            "file_name"
                        )
                        or document.get(
                            "name"
                        )
                        or ""
                    )

                    title = (
                        document.get(
                            "title"
                        )
                        or filename
                        or ""
                    )

                    source = {
                        "document_id": document_id,
                        "title": title,
                        "filename": filename,
                        "file_type": (
                            document.get(
                                "file_type"
                            )
                            or ""
                        ),

                        # Passage exact utilisé par le RAG.
                        "excerpt": item["text"]
                    }

                    if document.get(
                        "mime_type"
                    ):
                        source["mime_type"] = (
                            document[
                                "mime_type"
                            ]
                        )

                    if document.get(
                        "file_size"
                    ) is not None:
                        source["file_size"] = (
                            document[
                                "file_size"
                            ]
                        )

                    if document.get(
                        "created_at"
                    ):
                        source["created_at"] = str(
                            document[
                                "created_at"
                            ]
                        )

                    sources.append(
                        source
                    )

            except Exception as e:

                print(
                    "❌ Erreur récupération "
                    "MongoDB sources:"
                )

                print(
                    f"{type(e).__name__}: {e}"
                )

        print(
            "\n========== SOURCES =========="
        )

        print(sources)

        # ============================================================
        # 8. RÉPONSE FINALE
        # ============================================================

        result = {
            "answer": answer,
            "chunks": len(
                unique_results
            ),
            "sources": sources
        }

        print(
            "\n========== RAG RESPONSE =========="
        )

        print(result)

        print(
            "==================================\n"
        )

        return result