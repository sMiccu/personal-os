# Personal OS

自分自身の情報整理・学習・タスク管理・振り返りを効率化するための個人用プロジェクト。

## Overview

現在は以下の流れを構築している。

```text
Discord #inbox
       ↓
Python
       ↓
Claude Code
       ↓
分類
 ├─ task
 ├─ learning
 ├─ idea
 └─ note
       ↓
Obsidian Vault
       ↓
Discord #ai-output
```

## Current Features

- Discord `#inbox` からメモを取得
- Claude Codeで内容を分類
- Obsidianへ原文と分類結果を保存
- Discord `#ai-output` へ処理結果を返却
- macOS Shortcutsから手動実行
- `launchd` で毎日自動実行

## Manual Run

```bash
~/personal-os/scripts/run.sh
```

## Secrets

秘密情報はRepository内には保存しない。

保存場所:

```text
~/.config/personal-os/secrets.env
```

## Docs

- `docs/setup.md` : 新しいMacへの構築手順
- `docs/architecture.md` : 全体構成と設計方針
- `docs/todo.md` : 今後の改善候補