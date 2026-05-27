#!/bin/bash
INPUT=$(cat)
echo "RAW_INPUT: $INPUT" >> /tmp/hook_debug.log
FILE=$(echo "$INPUT" | jq -r '.tool_input.path // .tool_input.file_path // empty')
echo "FILE: $FILE" >> /tmp/hook_debug.log
if [[ "$FILE" == *.py ]]; then
  echo "構文チェック開始: $FILE" >> /tmp/hook_debug.log
  echo "構文チェック: $FILE"
  python3 -m py_compile "$FILE" >> /tmp/hook_debug.log 2>&1 && echo "✅ OK" || echo "❌ SYNTAX ERROR"
  echo "構文チェック完了" >> /tmp/hook_debug.log
fi
