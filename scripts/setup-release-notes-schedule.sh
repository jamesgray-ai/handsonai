#!/bin/bash
# Install a macOS launchd plist to run the release-notes-generator
# every Sunday at 9 PM (21:00) local time.
#
# Usage: bash scripts/setup-release-notes-schedule.sh

LABEL="com.jamesgray.release-notes-generator"
PLIST_PATH="$HOME/Library/LaunchAgents/$LABEL.plist"
SCRIPT_PATH="/Users/jamesgray/code/handsonai/scripts/run-release-notes-generator.sh"

# Unload existing plist if present
if launchctl list "$LABEL" &>/dev/null; then
    echo "Unloading existing schedule..."
    launchctl unload "$PLIST_PATH" 2>/dev/null
fi

cat > "$PLIST_PATH" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.jamesgray.release-notes-generator</string>

    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/jamesgray/code/handsonai/scripts/run-release-notes-generator.sh</string>
    </array>

    <key>StartCalendarInterval</key>
    <dict>
        <!-- Sunday = 0, 9 PM -->
        <key>Weekday</key>
        <integer>0</integer>
        <key>Hour</key>
        <integer>21</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>

    <key>WorkingDirectory</key>
    <string>/Users/jamesgray/code/handsonai</string>

    <key>StandardOutPath</key>
    <string>/Users/jamesgray/code/handsonai/logs/scheduled/launchd-release-notes.out.log</string>

    <key>StandardErrorPath</key>
    <string>/Users/jamesgray/code/handsonai/logs/scheduled/launchd-release-notes.err.log</string>
</dict>
</plist>
EOF

echo "Installed plist at: $PLIST_PATH"

# Load the plist
launchctl load "$PLIST_PATH"
echo "Schedule loaded. Verify with:"
echo "  launchctl list | grep release-notes"
