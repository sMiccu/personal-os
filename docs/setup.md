# Personal OS Setup Guide

新しいMacへ Personal OS を再構築するための手順。

## 1. 必要なもの

- macOS
- Git
- Python 3
- Obsidian
- Discord
- Claude Code
- GitHubアカウント

## 2. Repositoryを取得

```bash
cd ~
git clone <PRIVATE_REPOSITORY_URL> personal-os
cd personal-os
```

## 3. Python環境を作成

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install requests python-dotenv
```

確認:

```bash
which python
```

`~/personal-os/.venv/bin/python` 配下になっていればOK。

## 4. Obsidian Vaultを用意

ObsidianでPersonal OS用のVaultを用意する。

現在の例:

```text
~/Documents/miccu_vault_workspace
```

以下のフォルダは処理時に自動生成される。

```text
00 Inbox
20 Tasks
30 Learning
40 Ideas
50 Notes
```

## 5. Discord Serverを用意

自分用のDiscord Serverを作成し、最低限以下のチャンネルを作る。

```text
#inbox
#ai-output
```

用途:

- `#inbox`: スマホやMacから情報をæ Serverへ追加する。

## 7. Discord Channel IDを取得

DiscordのDeveloper Modeを有効にして、以下のIDを取得する。

- `#inbox`
- `#ai-output`

## 8. SecretsをRepository外に作成

```bash
mkdir -p ~/.config/personal-os
vi ~/.config/personal-os/secrets.env
```

内容:

```env
DISCORD_BOT_TOKEN=<BOT_TOKEN>
DISCORD_INBOX_CHANNEL_ID=<INBOX_CHANNEL_ID>
DISCORD_OUTPUT_CHANNEL_ID=<OUTPUT_CHANNEL_ID>
OBSIDIAN_VAULT_PATH=/Users/<USERNAME>/Documents/<VAULT_NAME>
```

権限を制限する。

```bash
chmod 600 ~/.config/personal-os/secrets.env
```

このファイルはGitHubへ保存しない。

## 9. Claude Codeをインストール

Homebrewを利用する場合:

```bash
brew install --cask claude-code
```

起動:

```bash
claude
```

Claudeアカウントへログインする。

## 10. Claude Codeのグローバル安全設定

以下を作成する。

```text
~/.claude/settings.json
```

秘密情報や危険なコマンドへのアクセスを制限する。

例:

```json
{
  "rf:*)",
      "Bash(sudo:*)"
    ],
    "ask": [
      "Bash(rm:*)",
      "Bash(git reset --hard:*)",
      "Bash(git clean:*)"
    ]
  }
}
```

秘密情報はPermission設定だけに依存せず、Repository外へ置く。

## 11. 動作確認

仮想環境を有効化する。

```bash
cd ~/personal-os
source .venv/bin/activate
```

Discordの `#inbox` にテストメッセージを投稿して実行する。

```bash
python scripts/process_inbox.py
```

以下が確認できればOK。

```text
Discord #inbox
↓
Claude Code
↓
Obsidian
↓
Discord #ai-output
```

## 12. 共通実行スクリプト

```text
scripts/run.sh
```

例:

```bash
#!/bin/zsh

set -e

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

cd "$HOME/personal-os"

source .venv/bin/activate

python scripts/process_inbox.py
```

実行権限を付ける。

```bash
chmod +x ~/personal-os/scripts/run.sh
```

テスト:

```bash
~/personal-os/scripts/run.sh
```

## 13. macOS Shortcuts

ショートカãaunchd

以下のLaunchAgentを作成する。

```text
~/Library/LaunchAgents/com.sora.personal-os.plist
```

現在は毎日21:00に実行する。

登録:

```bash
launchctl bootstrap \
  gui/$(id -u) \
  ~/Library/LaunchAgents/com.sora.personal-os.plist
```

確認:

```bash
launchctl print \
  gui/$(id -u)/com.sora.personal-os
```

即時テスト:

```bash
launchctl kickstart -k \
  gui/$(id -u)/com.sora.personal-os
```

ログ:

```bash
cat ~/personal-os/state/launchd.out.log
cat ~/personal-os/state/launchd.err.log
```

## 15. Security Checklist

GitHubへpushする前に確認する。

- `secrets.env` がRepository内にない
- `.env` が追跡されていない
- `.venv/` が追跡されていない
- `state/` が追跡されていない
- Discord Bot Tokenが含まれていない
- API KeyやSSH秘密鍵が含まれていない

必ず実行する。

```bash
git status
```
