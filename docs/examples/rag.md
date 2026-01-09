# RAG Validation Examples

Validate Retrieval-Augmented Generation (RAG) pipelines with SemanticTest.

## Overview

RAG systems combine retrieval and generation, which can introduce multiple failure modes:

1. **Retrieval failures**: Wrong documents retrieved
2. **Generation failures**: LLM misinterprets or hallucinates
3. **Integration failures**: Good retrieval but poor synthesis

SemanticTest helps catch all three.

## Basic RAG Testing

### Simple RAG Validator

```python
from semantictest import SemanticJudge
from your_rag import RAGPipeline

judge = SemanticJudge(temperature=0.0)
rag = RAGPipeline()

def validate_rag_response(query: str, expected_answer: str) -> bool:
    """Validate RAG response against expected answer."""
    response = rag.query(query)
    result = judge.evaluate(response, expected_answer)
    return result.score > 0.8

# Test cases
test_cases = [
    {
        "query": "What is the capital of France?",
        "expected": "Paris is the capital of France"
    },
    {
        "query": "When was Python created?",
        "expected": "Python was created in 1991 by Guido van Rossum"
    }
]

for case in test_cases:
    is_valid = validate_rag_response(case["query"], case["expected"])
    status = "✅" if is_valid else "❌"
    print(f"{status} {case['query'][:50]}...")
```

## Comprehensive RAG Testing

### RAG Test Suite

```python
from semantictest import SemanticJudge
from dataclasses import dataclass
from typing import Optional
import json

@dataclass
class RAGTestCase:
    query: str
    expected_answer: str
    expected_sources: Optional[list[str]] = None
    min_score: float = 0.8
    category: str = "general"

class RAGTestSuite:
    """Comprehensive RAG testing framework."""

    def __init__(self, rag_pipeline):
        self.rag = rag_pipeline
        self.judge = SemanticJudge(temperature=0.0)
        self.results = []

    def run_test(self, test: RAGTestCase) -> dict:
        """Run a single RAG test."""
        # Get RAG response
        response = self.rag.query(test.query)

        # Evaluate semantic similarity
        result = self.judge.evaluate(response.answer, test.expected_answer)

        # Check sources if specified
        source_match = True
        if test.expected_sources:
            retrieved_sources = [s.id for s in response.sources]
            source_match = any(
                s in retrieved_sources for s in test.expected_sources
            )

        test_result = {
            "query": test.query,
            "score": result.score,
            "passed": result.score >= test.min_score and source_match,
            "reasoning": result.reasoning,
            "response": response.answer,
            "expected": test.expected_answer,
            "source_match": source_match,
            "category": test.category
        }

        self.results.append(test_result)
        return test_result

    def run_all(self, tests: list[RAGTestCase]) -> dict:
        """Run all tests and return summary."""
        for test in tests:
            self.run_test(test)

        passed = sum(1 for r in self.results if r["passed"])

        # Group by category
        by_category = {}
        for r in self.results:
            cat = r["category"]
            if cat not in by_category:
                by_category[cat] = {"passed": 0, "total": 0}
            by_category[cat]["total"] += 1
            if r["passed"]:
                by_category[cat]["passed"] += 1

        return {
            "total": len(self.results),
            "passed": passed,
            "failed": len(self.results) - passed,
            "pass_rate": passed / len(self.results),
            "by_category": by_category,
            "failures": [r for r in self.results if not r["passed"]]
        }

# Usage
test_cases = [
    RAGTestCase(
        query="What is our refund policy?",
        expected_answer="We offer full refunds within 30 days of purchase",
        expected_sources=["policy_doc_v2"],
        category="policy"
    ),
    RAGTestCase(
        query="How do I reset my password?",
        expected_answer="Click 'Forgot Password' on the login page",
        category="technical"
    ),
]

suite = RAGTestSuite(rag_pipeline)
report = suite.run_all(test_cases)
print(f"Pass rate: {report['pass_rate']:.1%}")
```

## Testing Different RAG Components

### Retrieval Quality Testing

```python
from semantictest import SemanticJudge

class RetrievalTester:
    """Test retrieval quality independently."""

    def __init__(self, retriever):
        self.retriever = retriever
        self.judge = SemanticJudge(temperature=0.0)

    def test_retrieval(
        self,
        query: str,
        relevant_content: str,
        k: int = 5
    ) -> dict:
        """
        Test if retriever finds relevant documents.

        Args:
            query: The search query
            relevant_content: Content that should be found
            k: Number of documents to retrieve
        """
        docs = self.retriever.search(query, k=k)

        # Check if any retrieved doc matches expected content
        best_score = 0
        best_doc = None

        for doc in docs:
            result = self.judge.evaluate(doc.content, relevant_content)
            if result.score > best_score:
                best_score = result.score
                best_doc = doc

        return {
            "query": query,
            "found": best_score > 0.7,
            "best_score": best_score,
            "best_doc_id": best_doc.id if best_doc else None,
            "total_retrieved": len(docs)
        }

# Test retrieval
tester = RetrievalTester(rag.retriever)
result = tester.test_retrieval(
    query="password reset",
    relevant_content="To reset your password, click the forgot password link"
)
print(f"Found relevant doc: {result['found']}")
```

### Generation Quality Testing

```python
class GenerationTester:
    """Test generation quality given retrieved context."""

    def __init__(self, generator):
        self.generator = generator
        self.judge = SemanticJudge(temperature=0.0)

    def test_generation(
        self,
        query: str,
        context: str,
        expected_answer: str
    ) -> dict:
        """Test if generator produces correct answer given context."""
        # Generate with known-good context
        response = self.generator.generate(query, context)

        result = self.judge.evaluate(response, expected_answer)

        return {
            "query": query,
            "score": result.score,
            "passed": result.score > 0.8,
            "response": response,
            "expected": expected_answer,
            "reasoning": result.reasoning
        }

# Test generation independently
gen_tester = GenerationTester(rag.generator)
result = gen_tester.test_generation(
    query="What is the return policy?",
    context="Our return policy allows returns within 30 days with receipt.",
    expected_answer="You can return items within 30 days with a receipt"
)
```

## Hallucination Detection

### Grounded Response Testing

```python
from semantictest import SemanticJudge

class HallucinationDetector:
    """Detect when RAG hallucinates beyond retrieved context."""

    def __init__(self):
        self.judge = SemanticJudge(temperature=0.0)

    def check_grounding(
        self,
        response: str,
        retrieved_context: str,
        threshold: float = 0.6
    ) -> dict:
        """
        Check if response is grounded in retrieved context.

        Low score may indicate hallucination.
        """
        result = self.judge.evaluate(response, retrieved_context)

        is_grounded = result.score >= threshold

        return {
            "is_grounded": is_grounded,
            "grounding_score": result.score,
            "reasoning": result.reasoning,
            "potential_hallucination": not is_grounded
        }

    def extract_claims(self, response: str) -> list[str]:
        """Extract factual claims from response (simplified)."""
        # In practice, use NLP or another LLM
        sentences = response.split(". ")
        return [s.strip() for s in sentences if s.strip()]

    def check_each_claim(
        self,
        response: str,
        context: str
    ) -> list[dict]:
        """Check each claim in response against context."""
        claims = self.extract_claims(response)
        results = []

        for claim in claims:
            result = self.judge.evaluate(claim, context)
            results.append({
                "claim": claim,
                "grounded": result.score > 0.5,
                "score": result.score
            })

        return results

# Usage
detector = HallucinationDetector()

rag_response = rag.query("What are our business hours?")

# Check overall grounding
grounding = detector.check_grounding(
    response=rag_response.answer,
    retrieved_context=" ".join(doc.content for doc in rag_response.sources)
)

if grounding["potential_hallucination"]:
    print("⚠️ Potential hallucination detected!")
    print(f"Reasoning: {grounding['reasoning']}")
```

## pytest Integration

### RAG Test Fixtures

```python
# tests/conftest.py
import pytest
from semantictest import SemanticJudge
from your_rag import RAGPipeline

@pytest.fixture(scope="session")
def judge():
    return SemanticJudge(temperature=0.0)

@pytest.fixture(scope="session")
def rag():
    return RAGPipeline()

@pytest.fixture
def rag_assert(judge, rag):
    """Helper for RAG assertions."""
    def _assert(query: str, expected: str, threshold: float = 0.8):
        response = rag.query(query)
        result = judge.evaluate(response.answer, expected)
        assert result.score > threshold, (
            f"RAG response mismatch:\n"
            f"  Query: {query}\n"
            f"  Expected: {expected}\n"
            f"  Got: {response.answer}\n"
            f"  Score: {result.score}\n"
            f"  Reasoning: {result.reasoning}"
        )
        return result
    return _assert
```

### RAG Tests

```python
# tests/test_rag.py
import pytest

class TestRAGAccuracy:
    """Test RAG response accuracy."""

    def test_factual_query(self, rag_assert):
        rag_assert(
            query="What is Python?",
            expected="Python is a programming language"
        )

    def test_policy_query(self, rag_assert):
        rag_assert(
            query="What is the refund policy?",
            expected="Refunds are available within 30 days",
            threshold=0.85
        )

    @pytest.mark.parametrize("query,expected", [
        ("How to contact support?", "Contact support via email or phone"),
        ("What are shipping costs?", "Shipping is free for orders over $50"),
    ])
    def test_common_queries(self, rag_assert, query, expected):
        rag_assert(query, expected)

class TestRAGGrounding:
    """Test that RAG stays grounded in retrieved content."""

    def test_no_hallucination(self, judge, rag):
        response = rag.query("What products do we sell?")

        # Concatenate retrieved context
        context = " ".join(doc.content for doc in response.sources)

        # Response should be grounded in context
        result = judge.evaluate(response.answer, context)
        assert result.score > 0.5, "Response may contain hallucinations"
```

## Monitoring RAG in Production

```python
from semantictest import SemanticJudge
from datetime import datetime

class RAGMonitor:
    """Monitor RAG quality in production."""

    def __init__(self):
        self.judge = SemanticJudge(temperature=0.0)
        self.metrics = []

    def log_query(
        self,
        query: str,
        response: str,
        context: str,
        expected: str = None
    ):
        """Log and evaluate a RAG query."""

        # Check grounding
        grounding = self.judge.evaluate(response, context)

        # Check against expected if available
        accuracy = None
        if expected:
            result = self.judge.evaluate(response, expected)
            accuracy = result.score

        metric = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "grounding_score": grounding.score,
            "accuracy_score": accuracy,
            "response_length": len(response),
            "context_length": len(context)
        }

        self.metrics.append(metric)

        # Alert on low grounding
        if grounding.score < 0.5:
            self._alert_hallucination(query, response, grounding)

        return metric

    def _alert_hallucination(self, query, response, grounding):
        """Alert on potential hallucination."""
        print(f"⚠️ Low grounding score: {grounding.score}")
        # Send to alerting system

# Usage in production
monitor = RAGMonitor()

@app.post("/query")
async def handle_query(query: str):
    response = rag.query(query)

    # Log for monitoring
    monitor.log_query(
        query=query,
        response=response.answer,
        context=" ".join(doc.content for doc in response.sources)
    )

    return response
```

## Best Practices

1. **Test retrieval and generation separately** to isolate failures
2. **Use ground truth test sets** with known correct answers
3. **Check grounding scores** to catch hallucinations
4. **Monitor in production** with alerting
5. **Version your test cases** alongside your RAG configuration

## Next Steps

- [Production Monitoring](monitoring.md) - General monitoring patterns
- [Best Practices](../user-guide/best-practices.md) - Testing tips
- [API Reference](../api/semantic-judge.md) - Full API docs
