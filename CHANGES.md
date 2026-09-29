# Retrieval and Streamlit fixes

## Root cause

The old root app loaded a pickled FAISS index and filtered it with a service
detector. Research sections were indexed as `general`, so a `research` filter
returned no results. Unknown queries were filtered as `unknown`, which also
returned no results. FAISS metadata filtering happened after a small candidate
search, so relevant sections could be discarded before ranking. The separate
`speedlink-rag-chatbot/` prototype used another index and another app prompt.

## What changed

- `parse_kb.py` is now the single parser. It normalizes research, workspace
  room types, general sections and document types, validates duplicate or
  malformed sections, and resolves paths from the repository location.
- `route_query.py` recognizes all services, room names, common wording and
  multi-service questions. It resolves short follow-ups from prior user turns
  only; assistant text cannot change the active service.
- `retrieval.py` is the shared hybrid retriever. It reads current Markdown,
  combines BM25-style keyword scoring with MiniLM similarity, applies intent
  and room-type scoring, gives multi-service questions evidence for each
  service, and keeps business rules separate from answer evidence.
- `app.py` is now a reusable answer API and terminal client. It uses one system
  prompt, sends only trusted user history, prevents conditional templates from
  becoming claims about payments, bookings, coverage, invoices, emails or
  access, and applies a targeted FTTH grounding guard for invented billing
  periods or speeds.
- `streamlit_app.py` is the maintained browser UI. It uses the same `app.py`
  engine, supports multi-turn history, reset, source inspection and a clear
  missing-key state. The old `speedlink-rag-chatbot/app.py` is not the deploy
  entry point.
- `data/speedlink_crm_knowledge_base.md` now clarifies that the demo cannot
  verify coverage, payments or registrations and that unsupported values must
  be confirmed by staff. Research is included in the service list.
- `evaluate_retrieval.py`, `evaluation_cases.py`, `evaluate_answers.py` and
  `tests/test_rag.py` provide regression, unit, Streamlit and optional live
  answer checks. `README.md` contains local and Streamlit instructions.

## Validation

- 18 automated unit and Streamlit tests pass.
- 59/59 source-retrieval cases pass in lexical mode.
- 59/59 source-retrieval cases pass in hybrid mode, with the embedding model
  available and no fallback warning.
- 6/6 focused live Groq checks pass after the final prompt and knowledge-base
  hardening.
- The local Streamlit page loaded successfully and showed no browser console
  errors.

These results establish complete coverage for the supplied regression set. They
do not prove universal correctness for every future wording or replace review
of the actual business facts. The supplied PDF and Markdown do not contain
training fees, FTTH coverage data, installation amounts, internet speeds or
billing periods, Radio Broadband prices, current exam base fees or exchange
rates, or an office street address.
