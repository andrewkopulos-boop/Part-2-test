"""LLM integration for enhanced legal reasoning.

Calls external LLM APIs (Groq, Google Gemini, OpenRouter) to produce
richer, more natural-language judicial opinions and legal analysis.

Gracefully falls back to None when no API key is configured, so the
rule-based engine can still operate independently.
"""

from __future__ import annotations

import json
import logging
import os
import urllib.request
import urllib.error
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Provider definitions
# ---------------------------------------------------------------------------

@dataclass
class _Provider:
    name: str
    env_key: str
    url: str
    model: str
    format: str  # "openai" or "gemini"


_PROVIDERS: list[_Provider] = [
    _Provider(
        name="Groq",
        env_key="GROQ_API_KEY",
        url="https://api.groq.com/openai/v1/chat/completions",
        model="llama-3.3-70b-versatile",
        format="openai",
    ),
    _Provider(
        name="Google Gemini",
        env_key="GEMINI_API_KEY",
        url="https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        model="gemini-2.0-flash",
        format="gemini",
    ),
    _Provider(
        name="OpenRouter",
        env_key="OPENROUTER_API_KEY",
        url="https://openrouter.ai/api/v1/chat/completions",
        model="meta-llama/llama-3.3-70b-instruct:free",
        format="openai",
    ),
    _Provider(
        name="Together AI",
        env_key="TOGETHER_API_KEY",
        url="https://api.together.xyz/v1/chat/completions",
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        format="openai",
    ),
]


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------

@dataclass
class LLMEnhancement:
    """Enhanced analysis produced by an LLM."""
    provider: str = ""
    model: str = ""
    enhanced_opinion: str = ""
    enhanced_reasoning: str = ""
    enhanced_dissent: str = ""
    key_insights: list[str] = field(default_factory=list)
    plain_english_summary: str = ""
    error: str = ""


# ---------------------------------------------------------------------------
# Core LLM client
# ---------------------------------------------------------------------------

class LLMClient:
    """Unified client for calling various LLM APIs."""

    def __init__(self) -> None:
        self._provider = self._detect_provider()

    @property
    def available(self) -> bool:
        return self._provider is not None

    @property
    def provider_name(self) -> str:
        return self._provider.name if self._provider else "none"

    @staticmethod
    def _detect_provider() -> _Provider | None:
        """Find the first provider with a configured API key."""
        for provider in _PROVIDERS:
            if os.environ.get(provider.env_key):
                logger.info("LLM provider detected: %s", provider.name)
                return provider
        return None

    def _call_openai_format(
        self, messages: list[dict], temperature: float = 0.7, max_tokens: int = 2048
    ) -> str:
        """Call an OpenAI-compatible chat completions API."""
        provider = self._provider
        if not provider:
            return ""

        api_key = os.environ.get(provider.env_key, "")
        payload = json.dumps({
            "model": provider.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }).encode("utf-8")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

        # OpenRouter wants an extra header
        if provider.name == "OpenRouter":
            headers["HTTP-Referer"] = "https://legal-judge-bot.vercel.app"

        req = urllib.request.Request(provider.url, data=payload, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
        except (urllib.error.URLError, KeyError, json.JSONDecodeError) as exc:
            logger.warning("LLM API call failed (%s): %s", provider.name, exc)
            return ""

    def _call_gemini_format(
        self, prompt: str, temperature: float = 0.7, max_tokens: int = 2048
    ) -> str:
        """Call the Google Gemini API."""
        provider = self._provider
        if not provider:
            return ""

        api_key = os.environ.get(provider.env_key, "")
        url = provider.url.replace("{model}", provider.model) + f"?key={api_key}"

        payload = json.dumps({
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
            },
        }).encode("utf-8")

        headers = {"Content-Type": "application/json"}
        req = urllib.request.Request(url, data=payload, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (urllib.error.URLError, KeyError, json.JSONDecodeError, IndexError) as exc:
            logger.warning("Gemini API call failed: %s", exc)
            return ""

    def call(self, system_prompt: str, user_prompt: str) -> str:
        """Send a prompt to the configured LLM provider."""
        if not self._provider:
            return ""

        if self._provider.format == "gemini":
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            return self._call_gemini_format(full_prompt)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self._call_openai_format(messages)


# ---------------------------------------------------------------------------
# LLM Enhancer – takes case + judgment data and produces enhanced analysis
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = """You are a distinguished legal analyst and judicial opinion writer.
You provide thorough, well-reasoned legal analysis using the IRAC framework
(Issue, Rule, Application, Conclusion). Your opinions are clear, authoritative,
and cite relevant legal principles. Write in a professional judicial tone.

IMPORTANT: Always respond in valid JSON format with these exact keys:
- "enhanced_opinion": A detailed judicial opinion (2-3 paragraphs)
- "enhanced_reasoning": Step-by-step legal reasoning explaining the analysis
- "enhanced_dissent": A counterargument or dissenting perspective (1-2 paragraphs)
- "key_insights": An array of 3-5 key legal insights as strings
- "plain_english_summary": A plain-English summary accessible to non-lawyers (2-3 sentences)
"""


class LLMEnhancer:
    """Enhances rule-based judgments with LLM-generated reasoning."""

    def __init__(self) -> None:
        self._client = LLMClient()

    @property
    def available(self) -> bool:
        return self._client.available

    @property
    def provider_name(self) -> str:
        return self._client.provider_name

    def enhance_judgment(self, case_data: dict, judgment_data: dict) -> LLMEnhancement:
        """Enhance a judgment with LLM-generated analysis."""
        if not self._client.available:
            return LLMEnhancement(error="No LLM API key configured")

        user_prompt = self._build_judgment_prompt(case_data, judgment_data)
        raw = self._client.call(_SYSTEM_PROMPT, user_prompt)

        if not raw:
            return LLMEnhancement(
                provider=self._client.provider_name,
                error="LLM returned empty response",
            )

        return self._parse_response(raw)

    def enhance_panel(self, case_data: dict, panel_data: dict) -> LLMEnhancement:
        """Enhance a panel decision with LLM-generated analysis."""
        if not self._client.available:
            return LLMEnhancement(error="No LLM API key configured")

        user_prompt = self._build_panel_prompt(case_data, panel_data)
        raw = self._client.call(_SYSTEM_PROMPT, user_prompt)

        if not raw:
            return LLMEnhancement(
                provider=self._client.provider_name,
                error="LLM returned empty response",
            )

        return self._parse_response(raw)

    def enhance_risk(self, case_data: dict, risk_data: dict) -> LLMEnhancement:
        """Enhance a risk assessment with LLM analysis."""
        if not self._client.available:
            return LLMEnhancement(error="No LLM API key configured")

        prompt = (
            f"Analyze this litigation risk assessment and provide deeper insight.\n\n"
            f"CASE: {case_data.get('title', 'Unknown')} ({case_data.get('case_type', 'civil')})\n"
            f"FACTS: {json.dumps(case_data.get('facts', []))}\n"
            f"ISSUES: {json.dumps(case_data.get('issues', []))}\n\n"
            f"RISK ASSESSMENT RESULTS:\n"
            f"Risk Level: {risk_data.get('litigation_risk_level', 'unknown')}\n"
            f"Recommendation: {risk_data.get('recommendation', '')}\n"
            f"Parties: {json.dumps(risk_data.get('parties', []))}\n\n"
            f"Provide enhanced analysis of the litigation risks, strategic recommendations "
            f"for each party, and practical advice."
        )
        raw = self._client.call(_SYSTEM_PROMPT, prompt)
        if not raw:
            return LLMEnhancement(provider=self._client.provider_name, error="LLM returned empty response")
        return self._parse_response(raw)

    def enhance_settlement(self, case_data: dict, settlement_data: dict) -> LLMEnhancement:
        """Enhance a settlement analysis with LLM reasoning."""
        if not self._client.available:
            return LLMEnhancement(error="No LLM API key configured")

        prompt = (
            f"Analyze this settlement recommendation and provide deeper insight.\n\n"
            f"CASE: {case_data.get('title', 'Unknown')} ({case_data.get('case_type', 'civil')})\n"
            f"FACTS: {json.dumps(case_data.get('facts', []))}\n\n"
            f"SETTLEMENT ANALYSIS:\n"
            f"Should Settle: {settlement_data.get('should_settle', False)}\n"
            f"Settlement Range: ${settlement_data.get('settlement_range', {}).get('low', 0):,.0f} - "
            f"${settlement_data.get('settlement_range', {}).get('high', 0):,.0f}\n"
            f"Recommended: ${settlement_data.get('settlement_range', {}).get('recommended', 0):,.0f}\n"
            f"Damages Estimate: {json.dumps(settlement_data.get('damages_estimate', {}))}\n"
            f"Recommendation: {settlement_data.get('settlement_recommendation', '')}\n\n"
            f"Provide strategic settlement advice, negotiation tactics, and explain "
            f"the financial reasoning in plain English."
        )
        raw = self._client.call(_SYSTEM_PROMPT, prompt)
        if not raw:
            return LLMEnhancement(provider=self._client.provider_name, error="LLM returned empty response")
        return self._parse_response(raw)

    # ------------------------------------------------------------------
    # Prompt builders
    # ------------------------------------------------------------------

    @staticmethod
    def _build_judgment_prompt(case_data: dict, judgment_data: dict) -> str:
        parts = [
            "Analyze this legal case and judgment, then provide enhanced reasoning.\n",
            f"CASE TITLE: {case_data.get('title', 'Unknown')}",
            f"CASE TYPE: {case_data.get('case_type', 'civil')}",
            f"JURISDICTION: {case_data.get('jurisdiction', 'General')}",
        ]

        if case_data.get("summary"):
            parts.append(f"SUMMARY: {case_data['summary']}")

        facts = case_data.get("facts", [])
        if facts:
            parts.append(f"FACTS: {json.dumps(facts)}")

        issues = case_data.get("issues", [])
        if issues:
            parts.append(f"LEGAL ISSUES: {json.dumps(issues)}")

        parties = case_data.get("parties", [])
        if parties:
            party_strs = [f"{p.get('name', '?')} ({p.get('role', '?')})" for p in parties]
            parts.append(f"PARTIES: {', '.join(party_strs)}")

        parts.append(f"\nJUDGMENT:")
        parts.append(f"DISPOSITION: {judgment_data.get('disposition', 'unknown')}")
        parts.append(f"PREVAILING PARTY: {judgment_data.get('prevailing_party', 'unknown')}")
        parts.append(f"CONFIDENCE: {judgment_data.get('confidence', 0):.0%}")
        parts.append(f"RULES APPLIED: {json.dumps(judgment_data.get('rules_applied', []))}")
        parts.append(f"HOLDING: {judgment_data.get('holding', '')}")

        parts.append(
            "\nProvide an enhanced judicial opinion with deeper legal reasoning, "
            "relevant legal principles, and a plain-English explanation."
        )
        return "\n".join(parts)

    @staticmethod
    def _build_panel_prompt(case_data: dict, panel_data: dict) -> str:
        parts = [
            "Analyze this multi-judge panel decision and provide enhanced reasoning.\n",
            f"CASE: {case_data.get('title', 'Unknown')} ({case_data.get('case_type', 'civil')})",
            f"FACTS: {json.dumps(case_data.get('facts', []))}",
            f"ISSUES: {json.dumps(case_data.get('issues', []))}",
            f"\nPANEL DECISION:",
            f"Majority Disposition: {panel_data.get('majority_disposition', 'unknown')}",
            f"Vote: {panel_data.get('majority_vote', 'unknown')}",
            f"Unanimous: {panel_data.get('is_unanimous', False)}",
            f"Majority Confidence: {panel_data.get('majority_confidence', 0):.0%}",
        ]

        opinions = panel_data.get("opinions", [])
        for op in opinions:
            parts.append(
                f"\n{op.get('judge_name', '?')} ({op.get('philosophy', '?')}): "
                f"{op.get('disposition', '?')} at {op.get('confidence', 0):.0%}"
            )

        parts.append(
            "\nExplain why the judges might have reached different conclusions, "
            "how their judicial philosophies influenced the outcome, and what "
            "this means for the parties."
        )
        return "\n".join(parts)

    # ------------------------------------------------------------------
    # Response parsing
    # ------------------------------------------------------------------

    def _parse_response(self, raw: str) -> LLMEnhancement:
        """Parse the LLM response, handling both JSON and plain text."""
        result = LLMEnhancement(
            provider=self._client.provider_name,
            model=self._client._provider.model if self._client._provider else "",
        )

        # Try to extract JSON from the response
        json_str = self._extract_json(raw)
        if json_str:
            try:
                data = json.loads(json_str)
                result.enhanced_opinion = data.get("enhanced_opinion", "")
                result.enhanced_reasoning = data.get("enhanced_reasoning", "")
                result.enhanced_dissent = data.get("enhanced_dissent", "")
                result.key_insights = data.get("key_insights", [])
                result.plain_english_summary = data.get("plain_english_summary", "")
                return result
            except json.JSONDecodeError:
                pass

        # Fallback: treat the whole response as the enhanced opinion
        result.enhanced_opinion = raw
        result.plain_english_summary = raw[:500] if len(raw) > 500 else raw
        return result

    @staticmethod
    def _extract_json(text: str) -> str:
        """Extract a JSON object from text that may contain markdown fences."""
        # Try to find JSON in code fences
        import re
        match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
        if match:
            return match.group(1)

        # Try to find raw JSON object
        start = text.find("{")
        if start == -1:
            return ""

        # Find the matching closing brace
        depth = 0
        for i in range(start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    return text[start:i + 1]

        return ""
