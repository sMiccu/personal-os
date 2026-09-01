import json
import os
import subprocess
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(
    Path.home() / ".config" / "personal-os" / "secrets.env"
)

token = os.environ["DISCORD_BOT_TOKEN"]
channel_id = os.environ["DISCORD_INBOX_CHANNEL_ID"]

prompt_path = Path(__file__).parent.parent / "prompts" / "classify.md"
prompt_template = prompt_path.read_text(encoding="utf-8")

url = f"https://discord.com/api/v10/channels/{channel_id}/messages"

response = requests.get(
    url,
    headers={"Authorization": f"Bot {token}"},
    params={"limit": 1},
    timeout=10,
)

response.raise_for_status()

messages = response.json()

if not messages:
    print("No messages.")
    raise SystemExit

message = messages[0]
content = message.get("content", "").strip()

if not content:
    print("Latest message is empty.")
    raise SystemExit

full_prompt = f"""{prompt_template}

入力:
{content}
"""

result = subprocess.run(
    ["claude", "-p", full_prompt],
    capture_output=True,
    text=True,
    check=True,
)

raw_output = result.stdout.strip()

print("=== Claude raw output ===")
print(raw_output)

# ```json ... ``` が付いて返る場合に備えて除去
if raw_output.startswith("```"):
    lines = raw_output.splitlines()
    raw_output = "\n".join(lines[1:-1])

classified = json.loads(raw_output)

print("\n=== Parsed ===")
print(f"category: {classified['category']}")
print(f"title:    {classified['title']}")
print(f"content:  {classified['content']}")