#!/bin/bash
# Wrapper script for cookbook-question-reviewer subagent
# Reviews in-progress question drafts for quality, fixes issues, and approves/declines
# Can be scheduled via launchd for nightly review or run on-demand

PROJECT_DIR="/Users/jamesgray/code/handsonai"
LOG_DIR="$PROJECT_DIR/logs/scheduled"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
LOG_FILE="$LOG_DIR/cookbook-question-reviewer_$TIMESTAMP.log"

echo "=== Cookbook Question Reviewer ===" >> "$LOG_FILE"
echo "Started: $(date)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# Change to the repo directory
cd "$PROJECT_DIR"

# Run the subagent (using full path for launchd compatibility)
# --dangerously-skip-permissions allows headless operation with tool use
/Users/jamesgray/.local/bin/claude --agent cookbook-question-reviewer -p "Review all in-progress question drafts from the Notion Questions database" --dangerously-skip-permissions --verbose >> "$LOG_FILE" 2>&1

echo "" >> "$LOG_FILE"
echo "Finished: $(date)" >> "$LOG_FILE"
