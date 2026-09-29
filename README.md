# Speedlink CRM RAG chatbot

The project-root app is the maintained version. It supports workspace, FTTH
internet, training, Pearson VUE and research inquiries using one shared engine.

## Run locally in VS Code

Open this repository folder, then use its Python environment:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run streamlit_app.py
```

Keep your existing `.env`. For a new setup, copy `.env.example` to `.env` and
replace the placeholder with your Groq key. Never commit the real key.

For a new Python environment, first run `python -m venv .venv`.
For terminal chat, run `.\.venv\Scripts\python.exe app.py`.

Use **streamlit_app.py in the repository root** for the browser demo.
Do not run/deploy `speedlink-rag-chatbot/app.py`: that is an earlier, separate
prototype using PDF indexes and EEJ branding.

## How retrieval now works

- `data/speedlink_crm_knowledge_base.md` is the source of truth. Its 63 typed
  sections include all the service information in the older 21-page PDF.
- One parser normalizes research and workspace metadata and preserves headings,
  section types and source lines.
- Hybrid search combines BM25 keyword scores with MiniLM semantic similarity,
  then applies service, room type and question intent. It scores all sections
  before selection, so post-filter candidate limits cannot hide relevant records.
- Previous user turns resolve follow-ups like “How much?”; an explicit new
  service takes precedence. Multiple explicit services each get evidence.
- Relevant rules are supplied separately so they do not crowd prices and facts
  out of the answer evidence.
- The app builds embeddings in memory from the current Markdown. Its cache is
  keyed by content, so knowledge edits refresh retrieval automatically. Existing
  pickled vector stores are not loaded. No manual index rebuild is required.
- The first hybrid request loads the embedding model and may be slow. A fresh
  machine needs network access to download it once. Later requests reuse it.
- If the embedding model fails, the app visibly reports keyword-only fallback.
  `RETRIEVAL_MODE=lexical` explicitly selects that mode for diagnostics.
  The hybrid evaluation fails if it unexpectedly falls back.

The optional `python build_vectorstore.py` exports normalized sections into
`generated_vectorstore/` for inspection. It does not overwrite the old indexes.

## Repeatable tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe evaluate_retrieval.py --mode lexical --output reports/retrieval_lexical.json
.\.venv\Scripts\python.exe evaluate_retrieval.py --mode hybrid --output reports/retrieval_hybrid.json
```

These do not call Groq. Hybrid mode may download MiniLM on the first run.
The regression set checks 57 questions, including all nine workspace price
categories, the other four services, objections and conversation follow-ups.
Each case records the expected section and whether it must be first or in the
top three. Passing is source-retrieval evidence, not a promise of perfect answers.

Optional live tests use your Groq quota and save actual answers for review:

```powershell
.\.venv\Scripts\python.exe evaluate_answers.py --mode hybrid
```

This runs 16 scenarios (including multi-turn chats). The checks are deliberately
simple content checks; review `reports/live_answers.json` yourself.
To repeat one case, add `--scenario unverified_payment --output reports/payment_recheck.json`.
Rate limits and network errors are reported as failures, not successful tests.

## Deploy for the reviewer on Streamlit Community Cloud

1. Commit and push the root app, source Markdown, requirements, tests and docs.
   The current untracked `speedlink-rag-chatbot/` folder and pre-existing changes
   to `vectorstore/index.pkl` are not needed for this app. Review them separately.
2. Select your GitHub repository and branch, and set the main file path to
   `streamlit_app.py`.
3. In Advanced settings, select a supported Python version. The local checks ran
   on Python 3.14.6; select Python 3.14 to match the local interpreter family.
   A Linux/Community Cloud build still needs to be verified after deployment.
4. Add these app secrets (replace the placeholder):

```toml
GROQ_API_KEY = "your-real-key"
GROQ_MODEL = "openai/gpt-oss-120b"
RETRIEVAL_MODE = "hybrid"
```

5. Deploy and test a fresh conversation for each service, then test follow-ups
   and a change of service in the same conversation. Enable **Show supporting
   information** to inspect the retrieved evidence. **Start a new conversation**
   clears that browser session's history.

Official references: [deployment](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)
and [secrets](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management).

## Known knowledge and capability limits

The supplied PDF and Markdown do not contain training fee breakdowns, internet
billing periods/speeds, a coverage map, installation fee table, Radio Broadband
prices, current exam base fees/exchange rates, or an office street address.
Get approved values from Speedlink before promising answers to those questions.

This demo does not verify payments, issue invoices, register exams, send email,
check live coverage, reserve rooms, issue LMS access or schedule follow-ups.
The old templates were clarified to prevent the demo from claiming those actions.
Research support must remain guidance that respects academic integrity.

Chat history is held in the Streamlit browser session. It is not a CRM database.
The website and WhatsApp can later call the shared `answer_question` function,
but those channel integrations, identity/session storage and real CRM operations
are separate work after reviewer acceptance.

See `CHANGES.md` for the diagnosis and exact file changes.
