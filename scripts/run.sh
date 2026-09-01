#!/bin/zsh

set -e

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

cd "$HOME/personal-os"

source .venv/bin/activate

python scripts/process_inbox.py