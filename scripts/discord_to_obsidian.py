import json
import os
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(
    Path.home() / ".config" / "personal-os" / "secrets.env"
)

token = os.environ["DISCORD_BOT_TOKEN"]
channel_id = os.environ["DISCORD_INBOX_CHANNEL_ID"]
vault_path = Path(os.environ["OBSIDIAN_VAULT_PATH"])

state_file = Path(__file__).parent.parent / "state" / "discord.json"
state_file.parent.mkdir(parents=True, exist_ok=True)

last_message_id = None

if state_file.exists():
    with state_file.open("r", encoding="utf-8") as f:
        state = json.load(f)
        last_message_id = state.get("last_message_id")

url = f"https://discord.com/api/v10/channels/{channel_id}/messages"

params = {
    "limit": 100,
}

if last_message_id:
    params["after"] = last_message_id

response = requests.get(
    url,
    headers={"Authorization": f"Bot {token}"},
    params=params,
    timeout=10,
)

response.raise_for_status()
messages = response.json()

if not messages:
    print("No new messages.")
    raise SystemExit

messages = list(reversed(messages))

for message in messages:
    content = message.get("content", "").strip()

    if not content:
        continue

    created_at = datetime.fromisoformat(
        message["timestamp"].replace("Z", "+00:00")
    )

    # Discordの時刻はUTCなので、日本時間に直す
    created_at = created_at.astimezone()

    date_str = created_at.strftime("%Y-%m-%d")
    time_str = created_at.strftime("%H:%M")

    inbox_dir = vault_path / "00 Inbox"
    inbox_dir.mkdir(parents=True, exist_ok=True)

    output_file = inbox_dir / f"{date_str}.md"

    with output_file.open("a", encoding="utf-8") as f:
        f.write(
            f"\n## {time_str} Discord\n\n"
            f"{content}\n"
        )

    print(f"Saved: {content}")

latest_message_id = messages[-1]["id"]

with state_file.open("w", encoding="utf-8") as f:
    json.dump(
        {"last_message_id": latest_message_id},
        f,
        ensure_ascii=False,
        indent=2,
    )

print(f"Updated state: {latest_message_id}")