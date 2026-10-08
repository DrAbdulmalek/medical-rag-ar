# المعمارية — medical-rag-ar

> تفصيل الخطة الزمنية في `PLAN-12WEEKS.md` وتحليل القرار في `DECISION_ANALYSIS.md`.

## تدفق البيانات

```
PDF/صور طبية
   │  (1) ingestion/pdf_processor.py  ← ocr-core (Tesseract+Paddle، ميثاق 18 قاعدة)
   ▼
نص خام + metadata
   │  (2) ingestion/chunker.py        ← تقسيم بالفقرة/العنوان (لا بالحرف)
   ▼
chunks
   │  (3) ingestion/embedder.py       ← bge-m3 / AraBERT (sentence-transformers)
   ▼
vectors ──(4) ingestion/indexer.py──▶ Qdrant

سؤال عربي
   │  (5) retrieval/bm25.py  +  retrieval/dense.py (Qdrant)
   ▼  (6) retrieval/fusion.py — RRF (Reciprocal Rank Fusion)
أفضل K chunks
   │  (7) reasoning/llm.py — Qwen 2.5 7B Instruct (محلي)
   │  (8) reasoning/guardrails.py — رفض الإجابة بلا دليل + تحذير طبي
   ▼
إجابة + استشهادات (chunks المصدر)
```

## القرارات التقنية

| القرار | الاختيار | البديل المرفوض | السبب |
|---|---|---|---|
| OCR | ocr-core | إعادة بناء | موجود ومُختبَر (485 اختبارًا) |
| Fusion | RRF | weighted-sum | بلا معاملات لضبطها، قوي |
| LLM | Qwen 2.5 7B محلي | API خارجي | خصوصية + تكلفة + عربية قوية |
| Vector DB | Qdrant محلي | FAISS | Python-first + فلترة metadata |
| Guardrails | رفض بلا دليل | إجابة حرة | طبي — لا هلوسة |

## مجموعة التقييم (evaluation/)

- 500 سؤال/جواب طبي عربي **موثق المصدر** (من كتب المالك + مسارد).
- مقاييس: دقة الإجابة (LLM-as-judge + بشري على عينة)، ‏CER للاستخراج،
  زمن الاستجابة، recall@k للاسترجاع.
- مقارنة أساس: GPT-4 على نفس الأسئلة (للإبلاغ فقط — لا اعتماد).

## حدود أمانة

- لا يوجد كود تنفيذي بعد — هذه سقالة + خطة.
- guardrails الطبية **إلزامية** قبل أي عرض على مستخدم نهائي.
- Qwen/bge تُحمّل أوزانًا خارجية — راجع التراخيص قبل النشر التجاري.
