# Personal OS Architecture

## Purpose

Personal OSは、

「情報を整理するためのシステム」ではなく、
「情報整理そのものに使う時間を減らすシステム」

を目指す。

基本方針は以下。

```text
Capture
↓
Organize
↓
Think
↓
Act
↓
Review
```

入力時にはできるだけ整理せず、
あとからAIが整理する。

---

## Current Architecture

```text
Smartphone / Mac
       ↓
Discord #inbox
       ↓
Discord API
       ↓
process_inbox.py
       ↓
Claude Code
       ↓
Classification
 ├─ task
 ├─ learning
 ├─ idea
 └─ note
       ↓
Obsidian Vault
       ↓
Discord #ai-output
```

---

## Discord

### Role

情報の入力口。

主にスマホから、

- やること
- 学び
- 思いつき
- あとで調べたいこと
- 雑なメモ

などをそのまま `#inbox` に投稿する。

入力時に保存場所やカテゴリを考えなくてよい状態を目指す。

### Channels

```text
#inbox
```

情報の入力用。

```text
#ai-output
```

Personal OSの処理結果を受け取る。

---

## Obsidian

### Role

長期的に残す情報の保存先。

DiscordはInboxとして利用し、
最終的な情報の正本はObsidianとする。

現在の構成:

```text
00 Inbox
20 Tasks
30 Learning
40 Ideas
50 Notes
```

### Raw Data

Discordの原文は `00 Inbox` に保存する。

AIによる分類結果だけを残すのではなく、
元の文章も保持する。

理由:

- Claudeが分類を間違える可能性がある
- 将来分類ルールを変更できる
- 原文から再処理できる
- 情報が勝手に失われることを防ぐ

---

## Claude Code

### Role

ローカルで動くAI作業者。

現在の主な役割:

- Discord投稿の分類
- Markdown生成
- Obsidianへの整理
- Personal OS自体の開発

将来的には以下も担当させる可能性がある。

- Daily Review
- Weekly Review
- ノート間の関連付け
- タスク整理
- 過去情報の検索・要約

### Security

Claude Codeには必要以上のCredentialアクセスを与えない。

秘密情報はRepositoryとは別の場所に保存する。

```text
~/.config/personal-os/secrets.env
```

また、危険な操作はClaude CodeのPermission設定で制限する。

---

## ChatGPT

### Role

設計・壁打ち・意思決定支援。

主に以下を担当する。

- Personal OS全体の設計
- ツール選定
- 運用ルールの検討
- 改善案の整理
- 技術調査
- 実装方針の検討

基本的な役割分担:

```text
ChatGPT
→ 考える・設計する

Claude Code
→ 実装する・ファイルを操作する
```

---

## GitHub

### Role

Personal OSのコード・設定・ドキュメントの履歴管理。

保存するもの:

- Pythonコード
- Shell Script
- Claude用Prompt
- Documentation
- Project単位のClaude設定

保存しないもの:

- Discord Bot Token
- API Key
- Secret
- Runtime State
- Python仮想環境

Private Repositoryで管理する想定。

---

## State Management

Discordの同じメッセージを何度も処理しないため、
最後に処理したDiscord Message IDを保存する。

```text
state/discord.json
```

このファイルは実行時の状態なのでGit管理しない。

---

## Execution

処理本体:

```text
scripts/process_inbox.py
```

共通実行入口:

```text
scripts/run.sh
```

手動と自動の両方から同じ `run.sh` を利用する。

```text
macOS Shortcuts
       ↓
     run.sh
       ↑
       │
    launchd
```

これにより、
手動実行用と自動実行用で処理を二重管理しない。

---

## Manual Execution

macOS Shortcutsから実行する。

用途:

- 今すぐInboxを整理したい
- 日次処理を待ちたくない
- 動作確認したい

---

## Automatic Execution

macOS `launchd` で1日1回実行する。

現在:

```text
毎日 21:00
```

Personal OSでは厳密な実行時刻よりも、

「毎日ある程度自動的に整理される」

ことを重視する。

Macが停止している間も必ず処理する必要が出てきた場合は、
将来的にCloud実行を検討する。

---

## Local First

現在はMac上で完結する構成を優先する。

理由:

- 追加コストを抑えられる
- Obsidianがローカルにある
- Claude Codeをそのまま利用できる
- Secretをクラウドへ増やさずに済む
- 構成がシンプル

常時稼働が必要になった場合のみ、
GitHub ActionsやCloudサービス等を検討する。

---

## Future Direction

将来的には以下のようなPersonal OSを目指す。

```text
Capture
↓
AI Organize
↓
Task Management
↓
Daily Review
↓
Weekly Review
↓
Knowledge Base
↓
Personal Search
```

さらに必要に応じて、

- Google Calendar
- GitHub
- Email
- Browser Bookmark
- Voice Memo
- Mac Automation
- iPhone
- 1Password

などとの連携を検討する。