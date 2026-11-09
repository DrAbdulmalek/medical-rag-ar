# Implementation Gates and Evidence Requirements

> Current state: planning/scaffold. The README explicitly states that the
> ingestion, retrieval and reasoning implementation has not started. This
> document defines promotion gates; it does not claim those components exist.

## Non-negotiable operating constraints

- Local/offline processing is the default.
- No implicit remote provider, hosted vector store or cloud fallback.
- Use synthetic documents and synthetic questions in tests and CI.
- Do not put patient records, identifiers, scanned clinical documents or
  DICOM-derived content in public fixtures, hosted CI logs or remote services.
- Preserve source-document provenance and page/region references throughout
  ingestion, retrieval and answer generation.
- A generated answer is decision support, not a diagnosis or treatment order.
  It must expose evidence and uncertainty and require qualified human review.

## Gate 0 — repository and dependency baseline

Before implementation:
- Record the exact OCR-core release and pin a compatible version.
- Verify the license and intended use of every model, embedding model, corpus
  and dataset independently of the Python package license.
- Keep heavyweight dependencies optional and lazily imported.
- Define resource limits for CPU, RAM, disk and document/page counts.

Exit evidence: dependency/license inventory, reproducible install, lightweight
import tests, and a documented offline smoke test.

## Gate 1 — ingestion

Required behavior:
- Accept only explicitly supported input types.
- Preserve document ID, page number, OCR engine/version, confidence, bounding
  boxes and source hash where applicable.
- Store raw OCR output separately from normalized/chunked text.
- Make preprocessing and normalization steps traceable and reproducible.
- Reject or quarantine malformed/oversized inputs with a visible reason.

Tests: synthetic PDFs/images, corrupt files, empty pages, mixed Arabic/Latin,
RTL text, repeated headers, tables, page boundaries and resource-limit cases.

## Gate 2 — retrieval

Required behavior:
- Keep lexical and vector retrieval independently inspectable.
- Return source IDs and exact evidence spans for every candidate.
- Record embedding model/version and index configuration.
- Prevent cross-tenant or cross-document leakage if multi-user support is ever
  introduced.
- Treat missing indexes, embedding failures and low-confidence retrieval as
  explicit incomplete states, never as successful empty evidence.

Tests: known-answer synthetic corpus, irrelevant queries, conflicting sources,
duplicate chunks, Arabic morphology/diacritics, and retrieval failure paths.

## Gate 3 — answer generation

Required behavior:
- Answer only from retrieved evidence; otherwise abstain.
- Attach source/page/span citations to each material claim.
- Distinguish quoted evidence, inference and unknown information.
- Do not invent a citation or treat string overlap as proof of entailment.
- Preserve negation, uncertainty, laterality, values and units.
- Do not issue patient-specific treatment instructions without a validated
  clinical governance process and human review.

Tests: unsupported questions, contradictory evidence, negation flips,
unit/value changes, laterality swaps, citation mismatch and prompt injection
inside retrieved documents.

## Gate 4 — evaluation and promotion

Maintain a versioned, synthetic evaluation set with:
- retrieval recall/precision and citation-span correctness;
- answer support/abstention behavior;
- Arabic/RTL rendering and OCR error propagation;
- latency and resource use on CPU-only hardware;
- regression tests for clinically significant invariants.

A model or pipeline change must not be promoted on aggregate scores alone.
Report per-category regressions and retain a reproducible baseline.

## Promotion rule

A gate is PASS only when its implementation, tests, and evidence are present
and independently reviewable. A design document, passing scaffold test, or
successful import does not establish a working medical RAG system.
