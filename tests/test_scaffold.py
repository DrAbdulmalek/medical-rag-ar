"""اختبار السقالة — يضمن أن الحزمة تُستورد بلا تبعيات ثقيلة."""
import importlib


def test_package_imports_lightweight():
    m = importlib.import_module("medical_rag_ar")
    assert m.__version__


def test_subpackages_importable():
    for sub in ("ingestion", "retrieval", "reasoning", "evaluation", "demo"):
        importlib.import_module(f"medical_rag_ar.{sub}")
