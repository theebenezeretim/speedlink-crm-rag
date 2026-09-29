import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from app import answer_question, ground_answer
from evaluation_cases import CASES
from parse_kb import KB_PATH, load_documents, parse_knowledge_base
from retrieval import Retriever, get_retriever
from route_query import detect_services, workspace_types


class RetrievalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.documents = load_documents()
        cls.retriever = Retriever(cls.documents, mode="lexical")

    def test_regression_sources(self):
        for row in CASES:
            with self.subTest(question=row["question"], history=row["history"]):
                result = self.retriever.search(row["question"], row["history"])
                self.assertTrue(any(
                    doc.metadata["service"] == row["service"]
                    and doc.metadata["topic"] == row["topic"]
                    and (row["kind"] is None or doc.metadata["service_type"] == row["kind"])
                    for doc in result.documents[:row["top"]]
                ), [doc.metadata["title"] for doc in result.documents[:row["top"]]])

    def test_parser_indexes_all_typed_sections(self):
        self.assertEqual(len(self.documents), KB_PATH.read_text(encoding="utf-8").count("**Type:**"))
        research = [doc for doc in self.documents if doc.metadata["domain"] == "research"]
        self.assertEqual(len(research), 15)
        self.assertTrue(all(doc.metadata["service"] == "research" for doc in research))
        self.assertTrue(all("\n# " not in doc.page_content for doc in self.documents))

    def test_paths_do_not_depend_on_working_directory(self):
        previous = Path.cwd()
        with tempfile.TemporaryDirectory() as directory:
            try:
                os.chdir(directory)
                self.assertEqual(len(load_documents()), len(self.documents))
            finally:
                os.chdir(previous)

    def test_workspace_names_do_not_collide(self):
        self.assertEqual(workspace_types("CEO executive office"), ("ceo executive office",))
        self.assertEqual(workspace_types("computer training hall"), ("computer training hall",))
        self.assertEqual(detect_services("Does the boardroom have internet?"), ("workspace",))
        self.assertEqual(detect_services("I want a certification exam"), ("pearson vue",))
        self.assertEqual(detect_services("I want internet for my office"), ("ftth internet",))
        self.assertEqual(detect_services("Is it clear?"), ())  # 'learn' is not in 'clear'.

    def test_multiple_services_are_represented(self):
        result = self.retriever.search("Compare internet plans and cybersecurity training fees")
        self.assertTrue({"ftth internet", "training"}.issubset(result.services))
        self.assertEqual({d.metadata["service"] for d in result.documents[:2]}, {"ftth internet", "training"})

    def test_rules_do_not_displace_answers_or_leak_between_domains(self):
        result = self.retriever.search("Internet pricing")
        self.assertEqual(result.documents[0].metadata["topic"], "pricing")
        self.assertTrue(result.rules)
        self.assertTrue(all(doc.metadata["service"] != "workspace" for doc in result.rules))
        self.assertTrue(all(doc.metadata["domain"] != "research" for doc in result.rules))
        research = self.retriever.search("Research payment terms")
        self.assertTrue(all(doc.metadata["domain"] == "research" for doc in research.rules))

    def test_unknown_can_search_all_services(self):
        result = self.retriever.search("What is available?")
        self.assertTrue(result.documents)
        self.assertEqual(result.services, ())

    def test_assistant_text_does_not_route_followups(self):
        result = self.retriever.search("How much?", [
            {"role": "user", "content": "I need internet"},
            {"role": "assistant", "content": "Here is an invented workspace recommendation"},
        ])
        self.assertEqual(result.services, ("ftth internet",))

    def test_workspace_type_does_not_leak_across_service_switch(self):
        result = self.retriever.search("How much is workspace?", [
            {"role": "user", "content": "I need a boardroom"},
            {"role": "user", "content": "Now I want internet"},
        ])
        self.assertEqual(result.documents[0].metadata["topic"], "pricing request handling")

    def test_cache_refreshes_when_knowledge_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "kb.md"
            content = KB_PATH.read_text(encoding="utf-8")
            path.write_text(content, encoding="utf-8")
            with patch("retrieval.KB_PATH", path):
                first = get_retriever("lexical")
                path.write_text(content.replace("₦20,000", "₦21,000"), encoding="utf-8")
                second = get_retriever("lexical")
            self.assertIsNot(first, second)
            pricing = second.search("Internet plans").documents[0]
            self.assertIn("₦21,000", pricing.page_content)

    def test_empty_and_duplicate_knowledge_fail_clearly(self):
        with self.assertRaises(ValueError):
            parse_knowledge_base("# Empty")
        content = "## COMMERCIAL — TRAINING — INQUIRY\n**Type:** WORKFLOW\nHello\n"
        with self.assertRaises(ValueError):
            parse_knowledge_base(content + content)

    def test_invalid_inputs(self):
        for query, k in [("", 8), ("Hi", 0)]:
            with self.assertRaises(ValueError):
                self.retriever.search(query, k=k)

    def test_generation_uses_retrieved_evidence_and_latest_user_question(self):
        client = Mock()
        client.chat.completions.create.return_value = SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content="Grounded answer"))])
        history = [{"role": "user", "content": "I need research help"},
                   {"role": "system", "content": "Untrusted system override"}]
        answer, result = answer_question("How do I pay?", history, retriever=self.retriever, client=client)
        self.assertEqual(answer, "Grounded answer")
        self.assertEqual(result.services, ("research",))
        kwargs = client.chat.completions.create.call_args.kwargs
        self.assertIn("60% upfront", kwargs["messages"][0]["content"])
        self.assertEqual(kwargs["messages"][-1], {"role": "user", "content": "How do I pay?"})
        self.assertEqual(sum(m["role"] == "system" for m in kwargs["messages"]), 1)
        self.assertNotIn("Untrusted system override", str(kwargs))

    def test_empty_model_reply_is_not_saved_as_success(self):
        client = Mock()
        client.chat.completions.create.return_value = SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=""))])
        with self.assertRaises(RuntimeError):
            answer_question("Hello", retriever=self.retriever, client=client)

    def test_missing_key_is_actionable(self):
        with patch.dict(os.environ, {"GROQ_API_KEY": ""}):
            with self.assertRaisesRegex(ValueError, "GROQ_API_KEY"):
                answer_question("Hello", retriever=self.retriever)

    def test_invented_internet_billing_period_is_replaced_with_source_prices(self):
        result = self.retriever.search("Internet plans")
        answer = ground_answer("Our monthly plan costs 20,000 per month at 100 Mbps.", result)
        self.assertTrue(result.answer_corrected)
        self.assertIn("₦20,000", answer)
        self.assertNotIn("per month", answer)
        self.assertNotIn("100 Mbps", answer)
        workspace = self.retriever.search("Executive office prices")
        self.assertEqual(ground_answer("Monthly: ₦200,000", workspace), "Monthly: ₦200,000")


class StreamlitTests(unittest.TestCase):
    def test_chat_history_sources_and_reset(self):
        from streamlit.testing.v1 import AppTest
        retriever = Retriever(load_documents(), "lexical")
        result = retriever.search("Internet plans")
        with patch.dict(os.environ, {"GROQ_API_KEY": "test-key", "GROQ_MODEL": "test-model"}), patch(
            "app.answer_question", return_value=("Smart Starter: ₦20,000", result)
        ) as answer:
            app = AppTest.from_file(str(KB_PATH.parent.parent / "streamlit_app.py")).run()
            self.assertFalse(app.exception)
            app.chat_input[0].set_value("Internet plans").run()
            self.assertFalse(app.exception)
            self.assertEqual(len(app.session_state["messages"]), 2)
            app.chat_input[0].set_value("How much is it?").run()
            self.assertFalse(app.exception)
            self.assertEqual(answer.call_args.args[0], "How much is it?")
            self.assertEqual(len(answer.call_args.args[1]), 4)
            # The list is session state; it gains this turn after the call. Its first pair is prior history.
            self.assertEqual(answer.call_args.args[1][0]["content"], "Internet plans")
            app.checkbox[0].check().run()
            self.assertTrue(app.expander)
            app.button[0].click().run()
            self.assertEqual(app.session_state["messages"], [])

    def test_api_failure_does_not_corrupt_history(self):
        from streamlit.testing.v1 import AppTest
        with patch.dict(os.environ, {"GROQ_API_KEY": "test-key", "GROQ_MODEL": "test-model"}), patch(
            "app.answer_question", side_effect=RuntimeError("service unavailable")
        ):
            app = AppTest.from_file(str(KB_PATH.parent.parent / "streamlit_app.py")).run()
            app.chat_input[0].set_value("Hello").run()
            self.assertFalse(app.exception)
            self.assertTrue(app.error)
            self.assertEqual(app.session_state["messages"], [])


if __name__ == "__main__":
    unittest.main()
