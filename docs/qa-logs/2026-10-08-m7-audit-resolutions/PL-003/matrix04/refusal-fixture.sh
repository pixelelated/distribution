#!/bin/bash
case "$1" in
 --set-syncpath|--set-saves-remote|--set-settings-remote|--set-content-remote)
  case "$(cat /storage/qa524/refusal-fixture-mode)" in
   busy) exit 75 ;;
   timeout) exit 124 ;;
   settings-write) echo "Your cloud sync settings couldn't be saved."; exit 1 ;;
   unknown) echo 'untrusted synthetic provider account value must not appear in UI'; exit 1 ;;
  esac ;;
esac
exec /storage/qa524/frozen/usr/bin/cloud_setup "$@"
