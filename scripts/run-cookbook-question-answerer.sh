#!/bin/bash
# Wrapper script for cookbook-question-answerer subagent
# Processes new questions from Notion and drafts answer pages
# Can be scheduled via launchd for periodic processing

PROJECT_DIR="/Users/jamesgray/code/handsonai"
LOG_DIR="$PROJECT_DIR/logs/scheduled"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
LOG_FILE="$LOG_DIR/cookbook-question-answerer_$TIMESTAMP.log"

echo "=== Cookbook Question Answerer ===" >> "$LOG_FILE"
echo "Started: $(date)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# Change to the repo directory
cd "$PROJECT_DIR"

# Run the subagent (using full path for launchd compatibility)
# --dangerously-skip-permissions allows headless operation with tool use
/Users/jamesgray/.local/bin/claude --agent cookbook-question-answerer -p "Process all new questions from the Notion Questions database" --dangerously-skip-permissions --verbose >> "$LOG_FILE" 2>&1

echo "" >> "$LOG_FILE"
echo "Finished: $(date)" >> "$LOG_FILE"
