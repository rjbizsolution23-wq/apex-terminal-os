# --- apex-agent wiring (Claude-Code-Killer Agentic Loop) ---
export VENICE_MODEL="${VENICE_MODEL:-zai-org-glm-5-2}"   # or leave unset for $0 Ollama local mode
alias ax="noglob apex-agent"
axp() { apex-agent --plan "$@"; }       # plan first, execute on approval
axy() { apex-agent --trust yolo "$@"; } # hands-free zero-nag mode
