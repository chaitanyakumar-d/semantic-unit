# Production Monitoring Examples

Monitor AI systems in production using JudgeAI.

## Overview

Use JudgeAI to detect when your AI system's responses drift from expected behavior in production. Early detection prevents customer-facing issues.

## Basic Monitoring

### Simple Response Monitor

```python
from judgeai import SemanticJudge
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIMonitor:
    """Monitor AI responses for semantic drift."""

    def __init__(self, threshold: float = 0.7):
        self.judge = SemanticJudge(temperature=0.0)
        self.threshold = threshold
        self.drift_events = []

    def check_response(
        self,
        response: str,
        expected: str,
        context: dict = None
    ) -> bool:
        """
        Check if response matches expected semantically.

        Returns True if response is acceptable, False if drift detected.
        """
        result = self.judge.evaluate(response, expected)

        if result.score < self.threshold:
            event = {
                "timestamp": datetime.now().isoformat(),
                "score": result.score,
                "reasoning": result.reasoning,
                "response": response,
                "expected": expected,
                "context": context
            }
            self.drift_events.append(event)
            logger.warning(f"Drift detected! Score: {result.score}")
            return False

        return True

    def get_drift_report(self) -> dict:
        """Get summary of drift events."""
        return {
            "total_events": len(self.drift_events),
            "events": self.drift_events[-10:]  # Last 10
        }

# Usage
monitor = AIMonitor(threshold=0.75)

# Check AI responses
for response in ai_responses:
    is_ok = monitor.check_response(
        response=response,
        expected="Thank you for contacting support",
        context={"user_id": "123"}
    )
    if not is_ok:
        alert_team()
```

## Real-time Monitoring

### Streaming Monitor with Alerts

```python
from judgeai import SemanticJudge
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import deque
import statistics

@dataclass
class DriftAlert:
    timestamp: datetime
    score: float
    reasoning: str
    response: str
    severity: str  # "warning", "critical"

class RealtimeMonitor:
    """Real-time AI monitoring with alerts."""

    def __init__(
        self,
        warning_threshold: float = 0.75,
        critical_threshold: float = 0.5,
        window_size: int = 100
    ):
        self.judge = SemanticJudge(temperature=0.0)
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold
        self.recent_scores = deque(maxlen=window_size)
        self.alerts = []

    def evaluate(self, response: str, expected: str) -> DriftAlert | None:
        """Evaluate response and return alert if drift detected."""
        result = self.judge.evaluate(response, expected)
        self.recent_scores.append(result.score)

        if result.score < self.critical_threshold:
            alert = DriftAlert(
                timestamp=datetime.now(),
                score=result.score,
                reasoning=result.reasoning,
                response=response,
                severity="critical"
            )
            self.alerts.append(alert)
            return alert

        elif result.score < self.warning_threshold:
            alert = DriftAlert(
                timestamp=datetime.now(),
                score=result.score,
                reasoning=result.reasoning,
                response=response,
                severity="warning"
            )
            self.alerts.append(alert)
            return alert

        return None

    def get_health_status(self) -> dict:
        """Get current health metrics."""
        if not self.recent_scores:
            return {"status": "no_data"}

        avg_score = statistics.mean(self.recent_scores)
        min_score = min(self.recent_scores)

        if avg_score < self.critical_threshold:
            status = "critical"
        elif avg_score < self.warning_threshold:
            status = "degraded"
        else:
            status = "healthy"

        return {
            "status": status,
            "avg_score": round(avg_score, 3),
            "min_score": round(min_score, 3),
            "sample_size": len(self.recent_scores),
            "recent_alerts": len([
                a for a in self.alerts
                if a.timestamp > datetime.now() - timedelta(hours=1)
            ])
        }

# Integration with alerting system
monitor = RealtimeMonitor()

def process_ai_response(response: str, expected: str):
    alert = monitor.evaluate(response, expected)

    if alert:
        if alert.severity == "critical":
            send_pagerduty_alert(alert)
            send_slack_message(f"🚨 Critical AI drift: {alert.score}")
        else:
            send_slack_message(f"⚠️ AI drift warning: {alert.score}")

    return monitor.get_health_status()
```

## Batch Monitoring

### Scheduled Quality Check

```python
from judgeai import SemanticJudge
from datetime import datetime
import json

class BatchQualityChecker:
    """Periodic batch quality assessment."""

    def __init__(self, expected_responses: dict):
        self.judge = SemanticJudge(temperature=0.0)
        self.expected = expected_responses
        self.history = []

    def run_check(self, actual_responses: dict) -> dict:
        """
        Run quality check on batch of responses.

        Args:
            actual_responses: dict mapping query_id to response

        Returns:
            Quality report
        """
        results = []

        for query_id, actual in actual_responses.items():
            expected = self.expected.get(query_id)
            if not expected:
                continue

            result = self.judge.evaluate(actual, expected)
            results.append({
                "query_id": query_id,
                "score": result.score,
                "passed": result.score > 0.8
            })

        passed = sum(1 for r in results if r["passed"])
        total = len(results)

        report = {
            "timestamp": datetime.now().isoformat(),
            "total_checked": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": passed / total if total > 0 else 0,
            "avg_score": sum(r["score"] for r in results) / total if total else 0,
            "failures": [r for r in results if not r["passed"]]
        }

        self.history.append(report)
        return report

    def get_trend(self, days: int = 7) -> dict:
        """Get quality trend over time."""
        recent = self.history[-days:]
        if not recent:
            return {"trend": "no_data"}

        scores = [r["avg_score"] for r in recent]

        if len(scores) < 2:
            trend = "stable"
        elif scores[-1] > scores[0] + 0.05:
            trend = "improving"
        elif scores[-1] < scores[0] - 0.05:
            trend = "degrading"
        else:
            trend = "stable"

        return {
            "trend": trend,
            "current_score": scores[-1],
            "week_ago_score": scores[0],
            "samples": len(recent)
        }

# Daily cron job
checker = BatchQualityChecker(expected_responses=golden_responses)

def daily_quality_check():
    # Get today's AI responses
    responses = fetch_todays_responses()

    report = checker.run_check(responses)

    # Store report
    save_to_database(report)

    # Alert if quality dropped
    if report["pass_rate"] < 0.9:
        send_alert(f"Quality dropped to {report['pass_rate']:.1%}")

    return report
```

## A/B Testing

### Compare Model Versions

```python
from judgeai import SemanticJudge
from typing import Callable
import statistics

class ABTester:
    """A/B test different AI models."""

    def __init__(self):
        self.judge = SemanticJudge(temperature=0.0)
        self.results = {"A": [], "B": []}

    def test(
        self,
        prompts: list[str],
        model_a: Callable,
        model_b: Callable,
        expected_responses: list[str]
    ) -> dict:
        """
        Run A/B test comparing two models.

        Returns comparison report.
        """
        for prompt, expected in zip(prompts, expected_responses):
            response_a = model_a(prompt)
            response_b = model_b(prompt)

            result_a = self.judge.evaluate(response_a, expected)
            result_b = self.judge.evaluate(response_b, expected)

            self.results["A"].append(result_a.score)
            self.results["B"].append(result_b.score)

        return self._generate_report()

    def _generate_report(self) -> dict:
        """Generate comparison report."""
        avg_a = statistics.mean(self.results["A"])
        avg_b = statistics.mean(self.results["B"])

        # Simple statistical test
        diff = avg_b - avg_a

        if diff > 0.05:
            winner = "B"
            confidence = "high" if diff > 0.1 else "moderate"
        elif diff < -0.05:
            winner = "A"
            confidence = "high" if diff < -0.1 else "moderate"
        else:
            winner = "tie"
            confidence = "low"

        return {
            "model_a_avg": round(avg_a, 3),
            "model_b_avg": round(avg_b, 3),
            "difference": round(diff, 3),
            "winner": winner,
            "confidence": confidence,
            "sample_size": len(self.results["A"])
        }

# Usage
tester = ABTester()

report = tester.test(
    prompts=test_prompts,
    model_a=current_model.generate,
    model_b=new_model.generate,
    expected_responses=golden_responses
)

print(f"Winner: Model {report['winner']}")
print(f"Model A: {report['model_a_avg']:.3f}")
print(f"Model B: {report['model_b_avg']:.3f}")
```

## Integration Examples

### FastAPI Middleware

```python
from fastapi import FastAPI, Request
from judgeai import SemanticJudge
import asyncio

app = FastAPI()
monitor = RealtimeMonitor()

@app.middleware("http")
async def monitor_ai_responses(request: Request, call_next):
    response = await call_next(request)

    # Check if this was an AI endpoint
    if "/ai/" in request.url.path:
        # Get response body (simplified)
        ai_response = getattr(response, '_ai_response', None)
        expected = getattr(response, '_expected', None)

        if ai_response and expected:
            # Run monitoring asynchronously
            asyncio.create_task(
                run_monitor(ai_response, expected)
            )

    return response

async def run_monitor(response: str, expected: str):
    alert = monitor.evaluate(response, expected)
    if alert:
        await send_alert_async(alert)
```

### Prometheus Metrics

```python
from prometheus_client import Counter, Gauge, Histogram
from judgeai import SemanticJudge

# Metrics
SEMANTIC_SCORE = Histogram(
    'ai_semantic_score',
    'Semantic similarity scores',
    buckets=[0.1, 0.3, 0.5, 0.7, 0.8, 0.9, 0.95, 1.0]
)
DRIFT_EVENTS = Counter(
    'ai_drift_events_total',
    'Total drift events detected'
)
HEALTH_SCORE = Gauge(
    'ai_health_score',
    'Current AI health score (rolling average)'
)

class MetricsMonitor:
    def __init__(self):
        self.judge = SemanticJudge(temperature=0.0)

    def check(self, response: str, expected: str):
        result = self.judge.evaluate(response, expected)

        # Record metrics
        SEMANTIC_SCORE.observe(result.score)

        if result.score < 0.7:
            DRIFT_EVENTS.inc()

        # Update health gauge (simplified)
        HEALTH_SCORE.set(result.score)

        return result
```

## Best Practices

1. **Use temperature=0** for consistent monitoring
2. **Set appropriate thresholds** based on your SLOs
3. **Store drift events** for post-mortem analysis
4. **Alert on trends**, not just individual failures
5. **Include context** (user_id, session, etc.) in events
6. **Monitor the monitor** - ensure the monitoring system itself is healthy

## Next Steps

- [RAG Validation](rag.md) - Monitor RAG pipelines
- [Best Practices](../user-guide/best-practices.md) - More tips
- [API Reference](../api/semantic-judge.md) - Full API docs
