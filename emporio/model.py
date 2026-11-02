"""Ollama HTTP adapter, isolated from store orchestration."""
import json
import os
import urllib.error
import urllib.request
from urllib.parse import urlsplit

class ModelError(Exception):
    pass


class Ollama:
    def __init__(self, model=None, base_url=None):
        self.model = model or os.environ.get("OLLAMA_MODEL", "qwen3:8b")
        self.base_url = (base_url or os.environ.get("OLLAMA_HOST", "http://localhost:11434")).rstrip("/")
        if "://" not in self.base_url:
            self.base_url = "http://" + self.base_url
        parsed = urlsplit(self.base_url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password:
            raise ValueError("OLLAMA_HOST must be an http(s) URL without credentials")
        if parsed.path not in {"", "/"} or parsed.query or parsed.fragment:
            raise ValueError("OLLAMA_HOST must be an origin without a path, query or fragment")
        if parsed.port is not None and not 1 <= parsed.port <= 65535:
            raise ValueError("OLLAMA_HOST port must be between 1 and 65535")

    def chat(self, messages, tools):
        payload = {"model": self.model, "messages": messages, "tools": tools,
                   "stream": False, "think": False,
                   "options": {"temperature": 0, "num_ctx": 16384, "num_predict": 1600}}
        request = urllib.request.Request(self.base_url + "/api/chat", json.dumps(payload).encode(),
                                         {"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                result = json.load(response)
            message = result["message"]
            if not isinstance(message, dict) or not isinstance(message.get("content", ""), str):
                raise ValueError("invalid message")
            return message
        except urllib.error.HTTPError as exc:
            detail = "Model not found; run ollama pull for OLLAMA_MODEL." if exc.code == 404 else f"Ollama returned HTTP {exc.code}."
            raise ModelError(detail) from exc
        except (urllib.error.URLError, TimeoutError, ValueError, KeyError, TypeError, OSError) as exc:
            raise ModelError("Ollama is unavailable or returned an invalid response. Check ollama serve and ollama pull.") from exc

