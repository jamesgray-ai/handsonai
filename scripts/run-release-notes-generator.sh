#!/bin/bash
# Wrapper script for release-notes-generator subagent
# Runs the subagent and logs output for troubleshooting

# Store logs in the project folder for easy access
PROJECT_DIR="/Users/jamesgray/code/handsonai"
LOG_DIR="$PROJECT_DIR/logs/scheduled"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
LOG_FILE="$LOG_DIR/release-notes-generator_$TIMESTAMP.log"

echo "=== Release Notes Generator ===" >> "$LOG_FILE"
echo "Started: $(date)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# Change to the repo directory
cd "$PROJECT_DIR"

# Run the subagent (using full path for launchd compatibility)
# --dangerously-skip-permissions allows headless operation with tool use
/Users/jamesgray/.local/bin/claude -p "Generate and publish release notes for any changes since the last release." --agent release-notes-generator --dangerously-skip-permissions >> "$LOG_FILE" 2>&1

echo "" >> "$LOG_FILE"
echo "Finished: $(date)" >> "$LOG_FILE"
