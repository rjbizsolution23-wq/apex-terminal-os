# --- apex-agent v3.0 wiring (Claude-Code-Killer Agentic & Swarm Loop) ---
export VENICE_MODEL="${VENICE_MODEL:-zai-org-glm-5-2}"   # or leave unset for $0 Ollama local mode
alias ax="noglob apex-agent"
alias axp="noglob apex-agent --plan"                       # plan first, execute on approval
alias axy="noglob apex-agent --trust yolo"                 # hands-free zero-nag autonomous mode
alias axpar="noglob apex-agent --parallel 8"               # high-concurrency parallel tool execution
alias axswarm="noglob apex-agent --swarm"                  # parallel subagent swarm execution
alias axr="apex-remote"                                    # launch Remote Web Terminal & Cloudflare Tunnel
alias axv="apex-voice"                                     # launch Voice Intelligence Studio & voice-to-build
