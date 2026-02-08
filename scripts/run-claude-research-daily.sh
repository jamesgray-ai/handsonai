#!/bin/bash
# Wrapper script for claude-research-daily subagent
# Runs the subagent and logs output for troubleshooting

# Store logs in the project folder for easy access
PROJECT_DIR="/Users/jamesgray/code/handsonai"
LOG_DIR="$PROJECT_DIR/logs/scheduled"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
LOG_FILE="$LOG_DIR/claude-research-daily_$TIMESTAMP.log"

echo "=== Claude Research Daily ===" >> "$LOG_FILE"
echo "Started: $(date)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# Change to the repo directory
cd "$PROJECT_DIR"

# Run the subagent (using full path for launchd compatibility)
# --dangerously-skip-permissions allows headless operation with tool use
/Users/jamesgray/.local/bin/claude -p "Run my claude-research-daily subagent" --dangerously-skip-permissions >> "$LOG_FILE" 2>&1

echo "" >> "$LOG_FILE"
echo "Finished: $(date)" >> "$LOG_FILE"
