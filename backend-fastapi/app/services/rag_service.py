from app.services.chroma_service import ChromaService
from app.services.llm_service import LLMService
from app.repositories.document_repository import DocumentRepository


class RagService:

    def __init__(self):

        self.chroma_service = ChromaService()
        self.llm_service = LLMService()
        self.document_repository = DocumentRepository()

    async def ask(self, question: str) -> dict:

        print("\n========== RAG REQUEST ==========")
        print(f"Question : {question}")

        # ============================================================
        # 1. RECHERCHE SEMANTIQUE DANS CHROMADB
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
        # 2. NETTOYAGE ET SUPPRESSION DES DOUBLONS
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

                metadata = (
                    result.get("metadata")
                    or {}
                )

            else:

                text = getattr(
                    result,
                    "page_content",
                    ""
                )

                metadata = (
                    getattr(
                        result,
                        "metadata",
                        {}
                    )
                    or {}
                )

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

            # Maximum 3 passages utilisés
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
        # 3. IDENTIFICATION DES DOCUMENTS
        # ============================================================

        document_ids = []

        for index, item in enumerate(
            unique_results,
            start=1
        ):

            text = item["text"]
            metadata = item["metadata"]

            print(
                f"\n----- Chunk {index} -----"
            )

            print(
                f"Metadata : {metadata}"
            )

            print(
                f"Text : {text}"
            )

            document_id = metadata.get(
                "document_id"
            )

            if document_id:

                document_ids.append(
                    str(document_id)
                )

        # Suppression des IDs en double
        document_ids = list(
            dict.fromkeys(
                document_ids
            )
        )

        # ============================================================
        # 4. CONSTRUCTION DU CONTEXTE
        # ============================================================

        MAX_CONTEXT = 6000

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

            if len(text) > remaining:
                text = text[:remaining]

            passage = (
                f"\n"
                f"================ PASSAGE {index} ================\n"
                f"{text}\n"
                f"============== FIN PASSAGE {index} ==============\n"
            )

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

مهمتك هي الإجابة عن سؤال المستخدم اعتماداً فقط على المعلومات
الموجودة في المقاطع التي تم استرجاعها من أرشيف SNRT.

========================
قواعد مهمة جداً
========================

1. استخدم المعلومات الموجودة في المقاطع فقط.

2. لا تضف أي معلومة من معرفتك الخاصة.

3. لا تخترع أسماء أو أحداثاً أو تفاصيل غير موجودة في المقاطع.

4. اقرأ جميع المقاطع قبل الإجابة.

5. قد تكون بعض المقاطع غير مرتبطة مباشرة بالسؤال.
   تجاهل أي مقطع لا يحتوي على معلومات تساعد في الإجابة.

6. إذا كانت المعلومة المطلوبة موجودة في أكثر من مقطع،
   اجمع المعلومات المرتبطة بها في إجابة واحدة متماسكة.

7. لا تكتفِ بكلمة واحدة إذا كان السياق يسمح بتقديم إجابة
   أكثر وضوحاً وتفيد المستخدم.

8. أجب بجملة كاملة أو عدة جمل قصيرة حسب طبيعة السؤال.

9. إذا كان السؤال عن شخص، اذكر اسمه ودوره أو علاقته بالحدث
   إذا كانت هذه المعلومات موجودة في السياق.

10. إذا كان السؤال عن حدث، اشرح الحدث باختصار وبشكل واضح.

11. إذا كان السؤال عن سبب أو نتيجة، اذكر السبب أو النتيجة
    الموجودة في السياق.

12. إذا كان السؤال يتطلب مقارنة بين أشخاص أو أحداث،
    استخدم المعلومات الموجودة في المقاطع للمقارنة.

13. لا تكرر السؤال في الإجابة.

14. لا تبدأ الإجابة بعبارات مثل:
    "وفقاً للنص"
    أو
    "حسب الوثيقة"
    إلا إذا كان ذلك ضرورياً.

15. أجب بنفس لغة السؤال.

16. إذا كان السؤال باللغة العربية، أجب باللغة العربية.

17. إذا كان السؤال باللغة الفرنسية، أجب باللغة الفرنسية.

18. إذا كانت الإجابة موجودة بوضوح في السياق،
    لا تقل إنك لا تعرف الإجابة.

19. إذا كانت المعلومات الموجودة في المقاطع لا تسمح بالإجابة
    عن السؤال، أجب فقط:

    "لم أجد هذه المعلومة في الأرشيف."

20. لا تستخدم معلومات خارج المقاطع المقدمة لك.

========================
المقاطع المسترجعة من الأرشيف
========================

{context}

========================
سؤال المستخدم
========================

{question}

========================
تعليمات الإجابة
========================

حلل السؤال أولاً، ثم ابحث عن المعلومات المتعلقة به داخل
المقاطع.

بعد ذلك قدم إجابة واضحة ومباشرة وكاملة.

لا تذكر المقاطع أو أرقامها في الإجابة.

الإجابة:
"""

        print(
            "\n========== PROMPT ENVOYÉ AU LLM ==========\n"
        )

        print(prompt)

        print(
            "\n========== FIN PROMPT ==========\n"
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
        # 7. RÉCUPÉRATION DES DOCUMENTS SOURCES
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
                    f"Documents MongoDB récupérés : "
                    f"{len(documents)}"
                )

                documents_by_id = {

                    str(document.get("_id")):
                    document

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

                    document = (
                        documents_by_id.get(
                            document_id
                        )
                    )

                    if not document:

                        print(
                            f"⚠️ Document MongoDB "
                            f"introuvable : "
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

                        "document_id":
                            document_id,

                        "title":
                            title,

                        "filename":
                            filename,

                        "file_type":
                            document.get(
                                "file_type"
                            ) or "",

                        "excerpt":
                            item["text"]
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

        # ============================================================
        # 8. RÉPONSE FINALE
        # ============================================================

        result = {

            "answer":
                answer,

            "chunks":
                len(unique_results),

            "sources":
                sources
        }

        print(
            "\n========== SOURCES =========="
        )

        print(sources)

        print(
            "\n========== RAG RESPONSE =========="
        )

        print(result)

        print(
            "==================================\n"
        )

        return result