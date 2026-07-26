from app.services.chroma_service import ChromaService
from app.services.llm_service import LLMService


class RagService:

    def __init__(self):

        self.chroma = ChromaService()

        self.llm = LLMService()

    async def ask(

        self,

        question

    ):

        chunks = await self.chroma.search(

            question,

            k=5

        )

        # Suppression des doublons
        unique_chunks = []
        seen = set()

        for chunk in chunks:

            text = chunk.page_content.strip()

            if text not in seen:

                seen.add(text)

                unique_chunks.append(chunk)

        chunks = unique_chunks[:3]

        print(
            "\n========== CHUNKS ==========",
            flush=True
        )

        for i, chunk in enumerate(chunks):

            print(
                f"\n----- Chunk {i + 1} -----",
                flush=True
            )

            print(
                chunk.page_content,
                flush=True
            )

        if len(chunks) == 0:

            return {

                "answer": "لم أجد هذه المعلومة في الأرشيف.",

                "chunks": 0

            }

        context = ""

        MAX_CONTEXT = 1500

        for index, chunk in enumerate(chunks):

            text = chunk.page_content.strip()

            if len(context) + len(text) > MAX_CONTEXT:

                break

            context += f"الوثيقة رقم {index + 1}\n"

            context += text

            context += "\n\n"

        prompt = f"""
أنت مساعد ذكي خاص بأرشيف SNRT.

ستجد في الأسفل مجموعة من المقاطع المستخرجة من الوثائق.

أجب اعتماداً على هذه المقاطع فقط.

التعليمات:

- أجب اعتماداً على الوثائق فقط.
- لا تنسخ النص كما هو.
- أعد صياغة المعلومات بلغة عربية سليمة.
- إذا وجدت كلمات غير مفهومة أو مكتوبة بشكل خاطئ فتجاهلها.
- لا تكتب أي كلمة أجنبية مثل Inside أو Chapter أو غيرها.
- إذا كانت هناك معلومات مكررة فاكتبها مرة واحدة فقط.
- أجب بإيجاز إذا كان السؤال بسيطاً.
- وإذا كان السؤال يحتاج شرحاً فقدم شرحاً واضحاً.
- إذا كان السؤال عن شخص فاشرح من هو ودوره.
- إذا كان السؤال عن مكان فاشرحه.
- إذا كان السؤال عن حدث فاشرح ما حدث.
- إذا كانت المعلومات موزعة على أكثر من وثيقة، اجمعها في إجابة واحدة.
- أجب بنفس لغة السؤال.
- لا تخترع أي معلومة غير موجودة في الوثائق.
- إذا لم تجد الإجابة داخل الوثائق فقل فقط:

لم أجد هذه المعلومة في الأرشيف.

=====================
الوثائق
=====================

{context}

=====================
السؤال
=====================

{question}

=====================
الإجابة
=====================
"""

        answer = await self.llm.generate(

            prompt

        )

        return {

            "answer": answer.strip(),

            "chunks": len(chunks)

        }