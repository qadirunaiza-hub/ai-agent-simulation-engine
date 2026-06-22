"""
LLM Client Wrapper
Unified OpenAI format API calls
Supports Ollama num_ctx parameter to prevent prompt truncation
"""

import json
import os
import re
import time
from collections import deque
from datetime import datetime
from typing import Optional, Dict, Any, List
from openai import OpenAI

from ..config import Config

# Global in-memory ring buffer of recent LLM calls (last 200)
_global_llm_log: deque = deque(maxlen=200)

def get_global_llm_log() -> List[Dict[str, Any]]:
    """Return a snapshot of the global LLM call log (newest last)."""
    return list(_global_llm_log)

def _truncate(text: str, limit: int = 2000) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + f"… [+{len(text)-limit} chars]"


class LLMClient:
    """LLM Client"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        timeout: float = 300.0,
        call_tag: Optional[str] = None,   # e.g. "ontology", "simulation", "report"
        simulation_log_path: Optional[str] = None,  # path to simulation llm_calls.jsonl
    ):
        self.api_key = api_key or Config.LLM_API_KEY
        self.base_url = base_url or Config.get_active_base_url()
        # Runtime model override takes priority over .env default
        self.model = model or Config.get_runtime_model() or Config.LLM_MODEL_NAME
        self.call_tag = call_tag
        self.simulation_log_path = simulation_log_path

        if not self.api_key:
            raise ValueError("LLM_API_KEY not configured")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=timeout,
        )

        # Ollama context window size — prevents prompt truncation.
        # Read from env OLLAMA_NUM_CTX, default 8192 (Ollama default is only 2048).
        self._num_ctx = int(os.environ.get('OLLAMA_NUM_CTX', '8192'))

    def _is_ollama(self) -> bool:
        """Check if we're talking to an Ollama server."""
        return '11434' in (self.base_url or '')

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        response_format: Optional[Dict] = None
    ) -> str:
        """
        Send chat request

        Args:
            messages: Message list
            temperature: Temperature parameter
            max_tokens: Max token count
            response_format: Response format (e.g., JSON mode)

        Returns:
            Model response text
        """
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if response_format:
            kwargs["response_format"] = response_format

        # For Ollama: pass num_ctx via extra_body to prevent prompt truncation
        if self._is_ollama() and self._num_ctx:
            kwargs["extra_body"] = {
                "options": {"num_ctx": self._num_ctx}
            }

        t0 = time.time()
        response = self.client.chat.completions.create(**kwargs)
        elapsed_ms = int((time.time() - t0) * 1000)
        content = response.choices[0].message.content
        # Some models (like MiniMax M2.5) include <think>thinking content in response, need to remove
        content = re.sub(r'<think>[\s\S]*?</think>', '', content).strip()

        self._log_call(messages, content, elapsed_ms, kwargs.get("temperature"), kwargs.get("max_tokens"))
        return content

    @staticmethod
    def _compute_relevance(messages: list, response: str) -> dict:
        """Heuristic relevance/randomness score (0-100). Higher = more on-topic."""
        prompt_words = set()
        for m in messages:
            words = set(w.lower() for w in re.split(r'\W+', m.get('content', '') or '') if len(w) > 3)
            prompt_words.update(words)

        resp_tokens = [w.lower() for w in re.split(r'\W+', response) if len(w) > 3]
        resp_words = set(resp_tokens)

        # 1. Length score
        resp_len = len(response.strip())
        length_score = 0.1 if resp_len < 20 else (0.5 if resp_len < 80 else 1.0)

        # 2. Keyword overlap
        if prompt_words:
            overlap = len(prompt_words & resp_words)
            keyword_score = min(1.0, overlap / max(1, len(prompt_words) * 0.3))
        else:
            keyword_score = 0.7

        # 3. Repetition penalty (4-gram repeats)
        rep_score = 1.0
        flags = []
        if len(resp_tokens) >= 4:
            from collections import Counter
            grams = [' '.join(resp_tokens[i:i+4]) for i in range(len(resp_tokens) - 3)]
            max_rep = max(Counter(grams).values()) if grams else 1
            if max_rep > 3:
                rep_score = max(0.1, 1.0 - (max_rep - 3) * 0.15)
                flags.append('repetitive')

        if resp_len < 20:
            flags.append('too_short')

        score = int((length_score * 0.3 + keyword_score * 0.5 + rep_score * 0.2) * 100)
        return {'score': score, 'flags': flags}

    def _log_call(self, messages, response_text, elapsed_ms, temperature, max_tokens):
        """Append this LLM call to the global log and optionally a file."""
        relevance = self._compute_relevance(messages, response_text)
        entry = {
            "timestamp": datetime.now().isoformat(),
            "model": self.model,
            "tag": self.call_tag or "general",
            "elapsed_ms": elapsed_ms,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "relevance_score": relevance['score'],
            "relevance_flags": relevance['flags'],
            "messages": [
                {"role": m["role"], "content": _truncate(m.get("content", ""), 3000)}
                for m in messages
            ],
            "response": _truncate(response_text, 3000),
        }
        _global_llm_log.append(entry)

        if self.simulation_log_path:
            try:
                os.makedirs(os.path.dirname(self.simulation_log_path), exist_ok=True)
                with open(self.simulation_log_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            except Exception:
                pass

    def chat_json(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 4096
    ) -> Dict[str, Any]:
        """
        Send chat request and return JSON

        Args:
            messages: Message list
            temperature: Temperature parameter
            max_tokens: Max token count

        Returns:
            Parsed JSON object
        """
        response = self.chat(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"}
        )
        # Clean markdown code block markers
        cleaned_response = response.strip()
        cleaned_response = re.sub(r'^```(?:json)?\s*\n?', '', cleaned_response, flags=re.IGNORECASE)
        cleaned_response = re.sub(r'\n?```\s*$', '', cleaned_response)
        cleaned_response = cleaned_response.strip()

        try:
            return json.loads(cleaned_response)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format from LLM: {cleaned_response}")
