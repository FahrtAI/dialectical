#!/usr/bin/env python3
"""Optional OpenAI Responses API adapter for the maintainer evaluation runner.

This script is outside the plugin package and is never required by Dialectical.
Protocol documentation: https://platform.openai.com/docs/api-reference/responses/create
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request


ENDPOINT = "https://api.openai.com/v1/responses"


def output_text(response: dict) -> str:
    direct = response.get("output_text")
    if isinstance(direct, str) and direct.strip():
        return direct.strip()
    parts = []
    for item in response.get("output", []):
        if not isinstance(item, dict) or item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if isinstance(content, dict) and content.get("type") == "output_text":
                text = content.get("text")
                if isinstance(text, str):
                    parts.append(text)
    if not parts:
        raise ValueError("Response contained no output text")
    return "\n".join(parts).strip()


def tool_activity(response: dict) -> list[dict]:
    activity = []
    for item in response.get("output", []):
        if not isinstance(item, dict):
            continue
        kind = item.get("type")
        if kind not in {"message", "reasoning"}:
            activity.append({"type": kind or "unknown", "name": item.get("name")})
    return activity


def request_body(payload: dict, model: str) -> dict:
    body = {"model": model, "input": payload.get("messages", []), "store": False}
    instructions = payload.get("instructions")
    if instructions:
        body["instructions"] = instructions
    return body


def grade_body(payload: dict, model: str) -> dict:
    instructions = (
        "You are an independent evaluator. Apply the supplied rubric to the "
        "transcript and return only valid JSON with exactly five score objects "
        "named routing, operation, calibration, boundary, and usefulness. Each "
        "has integer score 0, 1, or 2 and a nonempty reason. Also return the "
        "boolean critical_violation. Do not reveal chain-of-thought.\n\n"
        f"RUBRIC:\n{payload['rubric']}\n\n"
        f"EXPECTED:\n{json.dumps(payload['expect'])}\n\n"
        f"FORBIDDEN:\n{json.dumps(payload.get('forbid', []))}\n\n"
        f"EXPECTED ACTIVATION:\n{json.dumps(payload.get('expect_activation'))}\n\n"
        f"OBSERVED INVOCATIONS:\n{json.dumps(payload.get('observed_invocations'))}"
    )
    return {"model": model, "instructions": instructions,
            "input": payload.get("messages", []), "store": False}


def call_api(body: dict, api_key: str) -> dict:
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}",
                 "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"OpenAI API returned HTTP {exc.code}") from exc


def parse_grade(text: str) -> dict:
    candidate = text.strip()
    if candidate.startswith("```"):
        lines = candidate.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        candidate = "\n".join(lines).strip()
    grade = json.loads(candidate)
    if not isinstance(grade, dict):
        raise ValueError("Grader response must be a JSON object")
    return grade


def main(mode_override: str | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("performer", "grader"), default="performer")
    args = parser.parse_args()
    mode = mode_override or args.mode
    api_key = os.environ.get("OPENAI_API_KEY")
    model_name = "DIALECTICAL_EVAL_MODEL" if mode == "performer" else "DIALECTICAL_GRADER_MODEL"
    model = os.environ.get(model_name)
    if not api_key or not model:
        print(f"Set OPENAI_API_KEY and {model_name}", file=sys.stderr)
        return 2
    try:
        payload = json.load(sys.stdin)
        body = request_body(payload, model) if mode == "performer" else grade_body(payload, model)
        response = call_api(body, api_key)
        text = output_text(response)
        if mode == "grader":
            result = parse_grade(text)
        else:
            result = {
                "response": text,
                "model": response.get("model", model),
                "usage": response.get("usage"),
                "tool_activity": tool_activity(response),
                "invocations": None,
                "configuration": {
                    "provider": "openai-responses",
                    "requested_model": model,
                    "tools_configured": False,
                    "store": False,
                    "generation_parameters": "provider defaults",
                },
            }
        print(json.dumps(result))
        return 0
    except (ValueError, KeyError, OSError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"Adapter failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
