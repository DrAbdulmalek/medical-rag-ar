# medical-rag-ar — Arabic Medical RAG

> **الحالة: مرحلة التخطيط/السقالة (planning).** هذا المستودع يوثّق التصميم
> والخطة (12 أسبوعًا) ويضع البنية الأساسية. التنفيذ الفعلي (ingestion/
> retrieval/reasoning) لم يبدأ بعد — الخطة في `docs/PLAN-12WEEKS.md`.
>
> المصدر: محادثة DeepSeek `1m3ih8eveq98lv7aqc` (رسائل 158-161).

## الفكرة

نظام **RAG طبي بالعربية** يجاوب على أسئلة طبية من مستندات عربية — يبني على
أصول المالك الفريدة:

- [`ocr-core`](https://github.com/DrAbdulmalek/ocr-core) — استخراج النص (ميثاق 18 قاعدة)
- [`arabic-medical-glossary`](https://github.com/DrAbdulmalek/arabic-medical-glossary) — ‏470K+ مصطلح
- `arabic-medical-ocr-corrections` (HF) — تصحيحات موثقة
- بيانات طبية/كتب ممسوحة

**لماذا هذا المشروع؟** (من `docs/DECISION_ANALYSIS.md): طبيب + أصول عربية
طبية نادرة + ocr-core جاهز = شيء لا تبنيه شركات أمريكية لا تفهم العربية
الطبية. الجمهور فوري (أطباء/طلاب/باحثون عرب). القياس واضح (دقة إجابة + CER).

## المعمارية

```
Ingestion ─→ Retrieval ─→ Reasoning
(PDF/صور     (BM25 +      (Qwen 2.5 7B
 → ocr-core   dense +      محلي +
 → chunking   RRF fusion   guardrails)
 → embed)     Qdrant)
        └── Evaluation (500 سؤال/جواب طبي عربي) ──┘
```

| الطبقة | الاختيار | السبب |
|---|---|---|
| OCR | `ocr-core` (Tesseract + Paddle) | موجود، يعمل |
| Embeddings | `BAAI/bge-m3` أو `aubmindlab/bert-base-arabertv2` | عربي جيد، مفتوح |
| Vector store | Qdrant (محلي) | سريع، Python-first |
| LLM | Qwen 2.5 7B Instruct (محلي) | الأفضل للعربية حاليًا |
| Fusion | RRF (Reciprocal Rank Fusion) | دمج BM25 + dense |
| الواجهة | Gradio (HF Space) ثم Next.js | سرعة إطلاق |

## البنية

```
src/medical_rag_ar/
├── ingestion/    pdf_processor · chunker · embedder · indexer
├── retrieval/    bm25 · dense · fusion (RRF)
├── reasoning/    llm · guardrails · answer
├── evaluation/   500 Q/A · metrics (دقة + CER + زمن)
└── demo/         Gradio HF Space
```

## التثبيت (سقالة)

```bash
pip install -e ".[dev]"          # أدوات التطوير فقط
pip install -e ".[ingest]"       # ocr-core + sentence-transformers + qdrant
pip install -e ".[retrieval]"    # rank_bm25 + qdrant-client
pip install -e ".[llm]"          # transformers + torch (Qwen 2.5)
pip install -e ".[all]"
```

## الوثائق

- `docs/DECISION_ANALYSIS.md` — لماذا هذا المشروع (4 سيناريوهات مُقارنة)
- `docs/PLAN-12WEEKS.md` — الخطة الأسبوعية التفصيلية (الأسبوع 1-12)
- `docs/ARCHITECTURE.md` — المعمارية والقرارات التقنية

## القاعدة الأولى (من الخطة)

> يُبنى على 4 مستودعات فقط (ocr-core + arabic-medical-glossary +
> arabic-medical-ocr-corrections + هذا). الباقي يُجمَّد 12 أسبوعًا.

## الترخيص

MIT (الكود). النماذج: Qwen 2.5 (Apache-2.0)، bge-m3 (MIT)، AraBERT (Apache-2.0).
