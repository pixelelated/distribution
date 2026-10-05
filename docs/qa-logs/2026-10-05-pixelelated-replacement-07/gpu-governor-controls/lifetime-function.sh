lifetime_suite() {
  local es="${ES_SRC:-$HOME/Development/emulationstation-next.worktrees/qa-integration}"
  if [ ! -f "$es/tests/cloud-oauth-lifetime.py" ]; then
    echo "no EmulationStation checkout at $es (set ES_SRC); the lifetime check did not run"; return 1
  fi
  echo "GuiMenu.cpp from $es at $(git -C "$es" rev-parse --short HEAD 2>/dev/null || echo '?')"
  python3 "$es/tests/cloud-oauth-lifetime.py" || return
  # Closing System Settings must also survive absent hardware options (#436).
  python3 "$es/tests/gpu-governor-save.py"
}
lifetime_suite
