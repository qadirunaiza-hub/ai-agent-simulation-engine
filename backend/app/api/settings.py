"""
Settings API
- List available LLM models from any Ollama server
- Get / set active model + server URL at runtime (no restart needed)
- Stream the global LLM call transparency log
"""

import requests
from flask import Blueprint, jsonify, request

from ..config import Config
from ..utils.llm_client import get_global_llm_log
from ..utils.logger import get_logger
from ..utils.auth_utils import login_required, admin_required

logger = get_logger("mirofish.api.settings")

settings_bp = Blueprint("settings", __name__)


def _fetch_ollama_models(base_url: str):
    """Query Ollama /api/tags and return model name list. Returns [] on failure."""
    try:
        # base_url may end in /v1 — strip it for the tags endpoint
        api_root = base_url.rstrip("/")
        if api_root.endswith("/v1"):
            api_root = api_root[:-3]
        resp = requests.get(f"{api_root}/api/tags", timeout=6)
        if resp.ok:
            return [m["name"] for m in resp.json().get("models", [])]
    except Exception as e:
        logger.debug(f"Could not reach Ollama at {base_url}: {e}")
    return []


@settings_bp.route("", methods=["GET"])
def get_settings():
    """Return current LLM + embedding settings."""
    active_url = Config.get_active_base_url()
    return jsonify({
        "success": True,
        "data": {
            "model": Config.get_runtime_model() or Config.LLM_MODEL_NAME,
            "base_url": active_url,
            "env_base_url": Config.LLM_BASE_URL,
            "embedding_model": Config.EMBEDDING_MODEL,
            "embedding_base_url": Config.EMBEDDING_BASE_URL,
            "default_model": Config.LLM_MODEL_NAME,
            "runtime_model_override": Config.get_runtime_model() is not None,
            "runtime_url_override": Config._runtime_base_url is not None,
        }
    })


@settings_bp.route("/models", methods=["GET"])
def list_models():
    """
    Return model list from the currently active Ollama server.
    Optional query param: ?url=http://... to query a different server without saving it.
    """
    query_url = request.args.get("url")
    target_url = query_url or Config.get_active_base_url()
    models = _fetch_ollama_models(target_url)
    return jsonify({
        "success": True,
        "data": {
            "models": models,
            "server": target_url,
            "count": len(models),
            "live": len(models) > 0,
        }
    })


@settings_bp.route("/model", methods=["POST"])
@admin_required
def set_model():
    """
    Set active LLM model at runtime.
    Body: { "model": "qwen2.5:32b" }
    """
    data = request.get_json() or {}
    model = data.get("model", "").strip()
    if not model:
        return jsonify({"success": False, "error": "model is required"}), 400
    Config.set_runtime_model(model)
    logger.info(f"Runtime model → {model}")
    return jsonify({"success": True, "data": {"model": model}})


@settings_bp.route("/model", methods=["DELETE"])
@admin_required
def reset_model():
    """Reset model override to .env default."""
    Config.set_runtime_model(None)
    return jsonify({"success": True, "data": {"model": Config.LLM_MODEL_NAME}})


@settings_bp.route("/server", methods=["POST"])
@admin_required
def set_server():
    """
    Switch the Ollama server URL at runtime.
    Body: { "url": "http://172.25.1.70:11434" }  (with or without /v1)
    """
    data = request.get_json() or {}
    url = data.get("url", "").strip().rstrip("/")
    if not url:
        return jsonify({"success": False, "error": "url is required"}), 400

    # Normalise: ensure /v1 suffix for LLM client
    base = url if url.endswith("/v1") else url + "/v1"
    Config.set_runtime_base_url(base)

    # Also update OASIS env vars used by CAMEL-AI
    import os
    os.environ["OPENAI_API_BASE_URL"] = base

    logger.info(f"Runtime Ollama server → {base}")

    # Probe the server and return available models
    models = _fetch_ollama_models(base)
    return jsonify({
        "success": True,
        "data": {
            "base_url": base,
            "models": models,
            "live": len(models) > 0,
        }
    })


@settings_bp.route("/server", methods=["DELETE"])
@admin_required
def reset_server():
    """Revert to .env server URL."""
    Config.set_runtime_base_url(None)
    return jsonify({"success": True, "data": {"base_url": Config.LLM_BASE_URL}})


@settings_bp.route("/llm-calls", methods=["GET"])
def get_llm_calls():
    """Return recent global LLM call log (newest first)."""
    limit = request.args.get("limit", 100, type=int)
    tag = request.args.get("tag")
    calls = get_global_llm_log()
    if tag:
        calls = [c for c in calls if c.get("tag") == tag]
    calls = list(reversed(calls))[:limit]
    return jsonify({"success": True, "data": {"count": len(calls), "calls": calls}})
