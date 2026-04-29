"""Minimal Claude API smoke test for the Epic 3 advisor.

Run from the backend/ directory:
    python scripts/smoke_test_claude.py

Verifies that:
  1. ANTHROPIC_API_KEY is loaded from .env
  2. The configured model responds successfully
  3. Tool-use / structured-output mode works (which the real advisor relies on)
"""

import sys
from pathlib import Path

# Allow running this script directly from backend/ without installing the app
# package: scripts/ lives one level below backend/, where app/ is importable.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from anthropic import Anthropic, APIError  # noqa: E402

from app.core.config import settings  # noqa: E402


def main() -> int:
    if not settings.anthropic_api_key:
        print("FAIL: ANTHROPIC_API_KEY is empty. Check backend/.env.")
        return 1

    print(f"Model:   {settings.anthropic_model}")
    print(f"API key: {settings.anthropic_api_key[:14]}... (length={len(settings.anthropic_api_key)})")
    print()

    client = Anthropic(api_key=settings.anthropic_api_key)

    # --- Test 1: plain text response -----------------------------------------
    print("[1/2] Plain text call...")
    try:
        resp = client.messages.create(
            model=settings.anthropic_model,
            max_tokens=64,
            messages=[
                {
                    "role": "user",
                    "content": "Reply with exactly: 'WearImpact advisor online.'",
                }
            ],
        )
    except APIError as exc:
        print(f"  FAIL: {exc}")
        return 1

    text = resp.content[0].text if resp.content else ""
    print(f"  Response:   {text!r}")
    print(f"  Tokens:     in={resp.usage.input_tokens}, out={resp.usage.output_tokens}")
    print(f"  StopReason: {resp.stop_reason}")
    print()

    # --- Test 2: tool-use / structured output -------------------------------
    # The real advisor will force the model into a tool call so its output is
    # always parseable JSON. Verify that path works on this account/model.
    print("[2/2] Tool-use structured call...")
    advice_tool = {
        "name": "report_status",
        "description": "Report a one-line status string.",
        "input_schema": {
            "type": "object",
            "properties": {
                "status": {"type": "string", "maxLength": 40},
                "ok": {"type": "boolean"},
            },
            "required": ["status", "ok"],
        },
    }

    try:
        resp = client.messages.create(
            model=settings.anthropic_model,
            max_tokens=128,
            tools=[advice_tool],
            tool_choice={"type": "tool", "name": "report_status"},
            messages=[
                {
                    "role": "user",
                    "content": "Call report_status with status='advisor ready' and ok=true.",
                }
            ],
        )
    except APIError as exc:
        print(f"  FAIL: {exc}")
        return 1

    tool_block = next((b for b in resp.content if b.type == "tool_use"), None)
    if tool_block is None:
        print("  FAIL: model did not return a tool_use block.")
        print(f"  Raw content: {resp.content}")
        return 1

    print(f"  Tool name:  {tool_block.name}")
    print(f"  Tool input: {tool_block.input}")
    print(f"  Tokens:     in={resp.usage.input_tokens}, out={resp.usage.output_tokens}")
    print()

    print("PASS: Claude API is reachable and tool-use works on this account.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
