"""Cost tracker for validation model calls.

Logs every model call to cost_ledger.jsonl.
Monitors for runaway behavior.
"""
from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)

_COST_RATES: dict[str, dict[str, float]] = {
    "gemini": {"input": 0.00125, "output": 0.005, "search": 0.035},
    "openai": {"input": 0.005, "output": 0.015, "search": 0.03},
}

MAX_CONSECUTIVE_FAILURES = 10
MAX_PROMPT_TOKENS = 100_000


class CostTracker:
    """Tracks costs and detects runaway behavior."""

    def __init__(self, output_dir: str | Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.ledger_path = self.output_dir / "cost_ledger.jsonl"
        self.cumulative_cost_usd = 0.0
        self.total_calls = 0
        self.consecutive_failures = 0
        self.warnings: list[str] = []
        self._provider_calls: dict[str, int] = {"gemini": 0, "openai": 0}
        self._failed_calls = 0
        self._retried_calls = 0

    def estimate_cost(
        self, provider: str, input_tokens: int, output_tokens: int,
        search_used: bool = False,
    ) -> float:
        rates = _COST_RATES.get(provider, _COST_RATES["gemini"])
        cost = (input_tokens / 1000) * rates["input"]
        cost += (output_tokens / 1000) * rates["output"]
        if search_used:
            cost += rates.get("search", 0)
        return cost

    def log_planned(
        self, provider: str, model: str, group_key: str, variant_ids: list[str],
        input_tokens_estimated: int, output_tokens_estimated: int,
        search_used: bool = False,
    ) -> dict:
        estimated_cost = self.estimate_cost(
            provider, input_tokens_estimated, output_tokens_estimated, search_used
        )
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "provider": provider, "model": model,
            "group_key": group_key, "variant_ids": variant_ids,
            "planned_or_actual": "planned",
            "input_tokens_estimated": input_tokens_estimated,
            "output_tokens_estimated": output_tokens_estimated,
            "input_tokens_actual": None, "output_tokens_actual": None,
            "search_used": search_used,
            "estimated_cost_usd": round(estimated_cost, 6),
            "cumulative_estimated_cost_usd": round(
                self.cumulative_cost_usd + estimated_cost, 6
            ),
            "status": "planned",
        }
        self._write_entry(entry)
        if input_tokens_estimated > MAX_PROMPT_TOKENS:
            self.warnings.append(
                f"Large prompt: {input_tokens_estimated} tokens for {group_key}"
            )
        return entry

    def log_actual(
        self, provider: str, model: str, group_key: str, variant_ids: list[str],
        input_tokens_estimated: int, output_tokens_estimated: int,
        input_tokens_actual: int | None, output_tokens_actual: int | None,
        search_used: bool = False, status: str = "success",
    ) -> dict:
        it = input_tokens_actual if input_tokens_actual is not None else input_tokens_estimated
        ot = output_tokens_actual if output_tokens_actual is not None else output_tokens_estimated
        estimated_cost = self.estimate_cost(provider, it, ot, search_used)
        self.cumulative_cost_usd += estimated_cost
        self.total_calls += 1
        self._provider_calls[provider] = self._provider_calls.get(provider, 0) + 1
        if status == "success":
            self.consecutive_failures = 0
        else:
            self.consecutive_failures += 1
            self._failed_calls += 1
            if status == "retry":
                self._retried_calls += 1
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "provider": provider, "model": model,
            "group_key": group_key, "variant_ids": variant_ids,
            "planned_or_actual": "actual",
            "input_tokens_estimated": input_tokens_estimated,
            "output_tokens_estimated": output_tokens_estimated,
            "input_tokens_actual": input_tokens_actual,
            "output_tokens_actual": output_tokens_actual,
            "search_used": search_used,
            "estimated_cost_usd": round(estimated_cost, 6),
            "cumulative_estimated_cost_usd": round(self.cumulative_cost_usd, 6),
            "status": status,
        }
        self._write_entry(entry)
        if self.consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
            msg = f"Runaway: {self.consecutive_failures} consecutive failures"
            self.warnings.append(msg)
            logger.error(msg)
        return entry

    def check_runaway(self) -> list[str]:
        return list(self.warnings)

    def summary(self) -> dict:
        return {
            "gemini_calls": self._provider_calls.get("gemini", 0),
            "openai_calls": self._provider_calls.get("openai", 0),
            "total_model_calls": self.total_calls,
            "failed_model_calls": self._failed_calls,
            "retried_model_calls": self._retried_calls,
            "estimated_total_cost_usd": round(self.cumulative_cost_usd, 4),
            "runaway_warnings": self.warnings,
        }

    def _write_entry(self, entry: dict) -> None:
        with open(self.ledger_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
