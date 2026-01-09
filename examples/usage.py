"""
Example usage of JudgeAI framework.

This script demonstrates how to use SemanticJudge for semantic evaluation.
"""

import os

from judgeai import SemanticJudge


def example_basic_evaluation():
    """Basic semantic evaluation example."""
    print("=" * 60)
    print("Example 1: Basic Semantic Evaluation")
    print("=" * 60)

    # Initialize the judge
    judge = SemanticJudge(model="gpt-4o-mini", temperature=0.0)

    # Evaluate semantic alignment
    result = judge.evaluate(
        actual="The machine learning model achieved 95% accuracy on the test dataset",
        expected="The ML model reached 95% test accuracy",
    )

    print(f"Alignment Score: {result.score:.3f}")
    print(f"Semantic Drift: {1 - result.score:.3f}")
    print(f"Reasoning: {result.reasoning}")
    print(f"Tokens Used: {result.metadata.get('tokens_used', 'N/A')}")
    print()


def example_different_meanings():
    """Example with semantically different texts."""
    print("=" * 60)
    print("Example 2: Different Semantic Meanings")
    print("=" * 60)

    judge = SemanticJudge()

    result = judge.evaluate(
        actual="The experiment failed with 30% accuracy",
        expected="The experiment succeeded with 95% accuracy",
    )

    print(f"Alignment Score: {result.score:.3f}")
    print(f"Reasoning: {result.reasoning}")
    print()


def example_with_metadata():
    """Example with custom metadata."""
    print("=" * 60)
    print("Example 3: Evaluation with Metadata")
    print("=" * 60)

    judge = SemanticJudge()

    custom_metadata = {
        "task_type": "classification",
        "domain": "medical",
        "experiment_id": "exp_001",
    }

    result = judge.evaluate(
        actual="Patient exhibits fever and cough",
        expected="Patient has pyrexia and coughing symptoms",
        metadata=custom_metadata,
    )

    print(f"Alignment Score: {result.score:.3f}")
    print(f"Metadata: {result.metadata}")
    print()


def example_batch_evaluation():
    """Batch evaluation example."""
    print("=" * 60)
    print("Example 4: Batch Evaluation")
    print("=" * 60)

    judge = SemanticJudge()

    test_pairs = [
        ("The system works correctly", "The system functions properly"),
        ("Error occurred during processing", "Processing completed successfully"),
        ("User authentication passed", "User login was successful"),
    ]

    results = judge.batch_evaluate(test_pairs)

    for i, result in enumerate(results, 1):
        print(f"\nPair {i}:")
        print(f"  Score: {result.score:.3f}")
        print(f"  Actual: {result.actual}")
        print(f"  Expected: {result.expected}")

    avg_score = sum(r.score for r in results) / len(results)
    print(f"\nAverage Alignment Score: {avg_score:.3f}")
    print()


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("JUDGEAI - EXAMPLE USAGE")
    print("=" * 60)
    print()

    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("JUDGEAI_API_KEY"):
        print("⚠️  WARNING: No API key found!")
        print("Set OPENAI_API_KEY or JUDGEAI_API_KEY environment variable")
        print("or create a .env file with your API key.")
        print("\nExamples will show structure but won't make actual API calls.\n")
        return

    try:
        example_basic_evaluation()
        example_different_meanings()
        example_with_metadata()
        example_batch_evaluation()

        print("=" * 60)
        print("✓ All examples completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have set your API key:")
        print("  export OPENAI_API_KEY='your-key-here'")
        print("  or")
        print("  export JUDGEAI_API_KEY='your-key-here'")


if __name__ == "__main__":
    main()
