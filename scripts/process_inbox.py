import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

# ==================================================
# Settings
# ==================================================

load_dotenv(
    Path.home() / ".config" / "personal-os" / "secrets.env"
)

token = os.environ["DISCORD_BOT_TOKEN"]
inbox_channel_id = os.environ["DISCORD_INBOX_CHANNEL_ID"]
output_channel_id = os.environ["DISCORD_OUTPUT_CHANNEL_ID"]
vault_path = Path(os.environ["OBSIDIAN_VAULT_PATH"])

project_root = Path(__file__).parent.parent
state_file = project_root / "state" / "discord.json"
prompt_file = project_root / "prompts" / "classify.md"

category_dirs = {
    "task": "20 Tasks",
    "learning": "30 Learning",
    "idea": "40 Ideas",
    "note": "50 Notes",
}


# ==================================================
# Helpers
# ==================================================

def load_state():
    if not state_file.exists():
        return {}

    with state_file.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_state(last_message_id):
    state_file.parent.mkdir(parents=True, exist_ok=True)

    with state_file.open("w", encoding="utf-8") as f:
        json.dump(
            {
                "last_message_id": last_message_id,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )


def fetch_new_messages(last_message_id=None):
    url = (
        f"https://discord.com/api/v10/channels/"
        f"{inbox_channel_id}/messages"
    )

    params = {
        "limit": 100,
    }

    if last_message_id:
        params["after"] = last_message_id

    response = requests.get(
        url,
        headers={
            "Authorization": f"Bot {token}",
        },
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    messages = response.json()

    # Discord APIは基本的に新しい順なので、
    # 古い → 新しい順へ並べ直す
    return list(reversed(messages))


def classify_with_claude(content, prompt_template):
    full_prompt = f"""{prompt_template}

入力:
{content}
"""

    result = subprocess.run(
        [
            "claude",
            "-p",
            full_prompt,
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    raw_output = result.stdout.strip()

    # Claudeが ```json ... ``` で返した場合に除去
    if raw_output.startswith("```"):
        lines = raw_output.splitlines()

        if len(lines) >= 3:
            raw_output = "\n".join(lines[1:-1])

    classified = json.loads(raw_output)

    category = classified.get("category", "note")
    title = classified.get("title", "Untitled")
    organized_content = classified.get(
        "content",
        content,
    )

    if category not in category_dirs:
        category = "note"

    return {
        "category": category,
        "title": title,
        "content": organized_content,
    }


def save_raw_message(content, created_at):
    date_str = created_at.strftime("%Y-%m-%d")
    time_str = created_at.strftime("%H:%M")

    inbox_dir = vault_path / "00 Inbox"
    inbox_dir.mkdir(parents=True, exist_ok=True)

    inbox_file = inbox_dir / f"{date_str}.md"

    with inbox_file.open("a", encoding="utf-8") as f:
        f.write(
            f"\n## {time_str} Discord\n\n"
            f"{content}\n"
        )


def save_classified_message(classified, created_at):
    category = classified["category"]
    title = classified["title"]
    content = classified["content"]

    date_str = created_at.strftime("%Y-%m-%d")
    time_str = created_at.strftime("%H:%M")

    target_dir = vault_path / category_dirs[category]
    target_dir.mkdir(parents=True, exist_ok=True)

    target_file = target_dir / f"{date_str}.md"

    with target_file.open("a", encoding="utf-8") as f:
        f.write(
            f"\n## {title}\n\n"
            f"- source: Discord\n"
            f"- time: {time_str}\n"
            f"- category: {category}\n\n"
            f"{content}\n"
        )


def post_discord_summary(summary):
    total = sum(len(items) for items in summary.values())

    lines = [
        "Inboxを整理しました。",
        "",
        f"合計: {total}件",
        f"task: {len(summary['task'])}件",
        f"learning: {len(summary['learning'])}件",
        f"idea: {len(summary['idea'])}件",
        f"note: {len(summary['note'])}件",
    ]

    titles = []

    for category, items in summary.items():
        for title in items:
            titles.append(
                f"- [{category}] {title}"
            )

    if titles:
        lines.extend(
            [
                "",
                "整理した内容",
                *titles,
            ]
        )

    discord_message = "\n".join(lines)

    url = (
        f"https://discord.com/api/v10/channels/"
        f"{output_channel_id}/messages"
    )

    response = requests.post(
        url,
        headers={
            "Authorization": f"Bot {token}",
            "Content-Type": "application/json",
        },
        json={
            "content": discord_message,
        },
        timeout=10,
    )

    response.raise_for_status()


# ==================================================
# Main
# ==================================================

def main():
    state = load_state()
    last_message_id = state.get("last_message_id")

    messages = fetch_new_messages(
        last_message_id=last_message_id
    )

    if not messages:
        print("No new messages.")
        return

    prompt_template = prompt_file.read_text(
        encoding="utf-8"
    )

    summary = {
        "task": [],
        "learning": [],
        "idea": [],
        "note": [],
    }

    processed_message_ids = []

    for message in messages:
        content = message.get(
            "content",
            "",
        ).strip()

        message_id = message["id"]

        # 空メッセージは分類対象外
        if not content:
            processed_message_ids.append(
                message_id
            )
            continue

        created_at = datetime.fromisoformat(
            message["timestamp"].replace(
                "Z",
                "+00:00",
            )
        ).astimezone()

        print(
            f"Processing: {content}"
        )

        # 1. Discord原文を保存
        save_raw_message(
            content,
            created_at,
        )

        # 2. Claudeで分類
        classified = classify_with_claude(
            content,
            prompt_template,
        )

        # 3. 分類結果をObsidianへ保存
        save_classified_message(
            classified,
            created_at,
        )

        category = classified["category"]
        title = classified["title"]

        summary[category].append(title)

        processed_message_ids.append(
            message_id
        )

        print(
            f"  -> [{category}] {title}"
        )

    if not processed_message_ids:
        print("No processable messages.")
        return

    # 全件処理できてからstate更新
    latest_message_id = (
        processed_message_ids[-1]
    )

    save_state(latest_message_id)

    # Discord #ai-outputへ結果返却
    post_discord_summary(summary)

    print()
    print(
        f"Processed "
        f"{len(processed_message_ids)} message(s)."
    )
    print(
        f"Updated state: "
        f"{latest_message_id}"
    )
    print(
        "Posted summary to Discord."
    )


if __name__ == "__main__":
    main()