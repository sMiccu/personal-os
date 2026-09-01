import os

import requests
from dotenv import load_dotenv

load_dotenv()

token = os.environ["DISCORD_BOT_TOKEN"]
channel_id = os.environ["DISCORD_INBOX_CHANNEL_ID"]

url = f"https://discord.com/api/v10/channels/{channel_id}/messages"

response = requests.get(
    url,
    headers={
        "Authorization": f"Bot {token}",
    },
    params={
        "limit": 5,
    },
    timeout=10,
)

response.raise_for_status()

messages = response.json()

for message in reversed(messages):
    print(
        f"{message['author']['username']}: "
        f"{message.get('content', '')}"
    )