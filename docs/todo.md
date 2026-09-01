# Personal OS Backlog

まだ実装すると決めていない改善案や検討事項を置く。

実装すると決めたものはGitHub Issueへ移す。

## Reliability

- [ ] `process_inbox.py` 失敗時にDiscordへエラー通知
- [ ] Claude Code失敗時のretry
- [ ] JSON Parse失敗時のfallback
- [ ] 途中失敗時の重複保存対策
- [ ] launchdログ整理
- [ ] 古いログのrotation
- [ ] Discord API rate limit対応

## Classification

- [ ] `task / learning / idea / note` の分類ルール改善
- [ ] Claude分類ミスの修正方法
- [ ] Inbox再分類機能
- [ ] Promptのversion管理
- [ ] 既存ObsidianノートをContextに使う分類

## Task Management

- [ ] ObsidianでのTask管理方法を検討
- [ ] Task期限
- [ ] Task優先度
- [ ] 完了Task管理
- [ ] 繰り返しTask
- [ ] Todoist / Things等との比較

## Daily Review

- [ ] Daily Summary生成
- [ ] 今日追加されたTaskの整理
- [ ] 今日学んだ内容の整理
- [ ] 未完了Taskの確認
- [ ] 明日やることの提案
- [ ] DiscordへDaily Summary送信

## Weekly Review

- [ ] Weekly Review生成
- [ ] 一週間の学びをまとめる
- [ ] 完了Taskの整理
- [ ] 未完了Taskの整理
- [ ] 新しいIdeaの整理
- [ ] 来週のFocusを作る

## Input

- [ ] Discordに貼ったURLの保存・整理
- [ ] Bookmark対応
- [ ] Discord添付画像対応
- [ ] PDF対応
- [ ] 音声メモ対応
- [ ] 音声文字起こし
- [ ] LINE Bot検討
- [ ] Slack連携検討
- [ ] iPhone Share Sheet検討

## Obsidian

- [ ] Folder構成の見直し
- [ ] Tag設計
- [ ] Frontmatter導入
- [ ] 関連ノート自動リンク
- [ ] Daily Notesとの統合
- [ ] Dataview等の利用検討

## Security

- [ ] 1Password導入検討
- [ ] 1Password CLI検討
- [ ] `secrets.env` 廃止検討
- [ ] Credential rotation
- [ ] Claude Code permission見直し
- [ ] Sandbox活用検討

## GitHub

- [ ] Private Repository作成
- [ ] 初回push
- [ ] GitHub Issues運用開始
- [ ] Issue Template検討
- [ ] GitHub Actions検討

## Mac Automation

- [ ] Shortcuts実行成功通知
- [ ] Shortcuts実行失敗通知
- [ ] Keyboard Shortcut設定
- [ ] Raycast検討
- [ ] Hammerspoon検討
- [ ] AeroSpace導入
- [ ] Karabiner-Elements導入
- [ ] Workspace自動起動

## Cloud / Always-On

現在はMac Local First。

必要になった場合のみ検討する。

- [ ] MacがOFFでもInbox処理
- [ ] GitHub Actions
- [ ] Cloudflare
- [ ] AWS
- [ ] Claude API利用

## Future Integrations

- [ ] Google Calendar
- [ ] GitHub Activity
- [ ] Email
- [ ] Browser Bookmark
- [ ] 学習ログ
- [ ] Project管理
- [ ] Personal Search
- [ ] Personal Dashboard
- [ ] スマホアプリ