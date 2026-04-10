"""Generate a printable setup checklist PDF for the Agentic AI for Leaders course."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import os

OUTPUT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "docs", "assets", "pdfs",
    "leaders-setup-checklist.pdf"
)

# Colors
DARK_BG = HexColor("#1a1a2e")
ACCENT = HexColor("#6c63ff")
LIGHT_ACCENT = HexColor("#e8e6ff")
TEXT_DARK = HexColor("#222222")
TEXT_MID = HexColor("#555555")
WHITE = HexColor("#ffffff")
LIGHT_GRAY = HexColor("#f5f5f5")
BORDER_GRAY = HexColor("#dddddd")


def get_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        "DocTitle", parent=styles["Title"],
        fontSize=22, leading=26, textColor=TEXT_DARK,
        spaceAfter=4, alignment=TA_LEFT
    ))
    styles.add(ParagraphStyle(
        "DocSubtitle", parent=styles["Normal"],
        fontSize=11, leading=14, textColor=TEXT_MID,
        spaceAfter=16
    ))
    styles.add(ParagraphStyle(
        "SectionHead", parent=styles["Heading1"],
        fontSize=16, leading=20, textColor=ACCENT,
        spaceBefore=18, spaceAfter=8
    ))
    styles.add(ParagraphStyle(
        "StepHead", parent=styles["Heading2"],
        fontSize=12, leading=15, textColor=TEXT_DARK,
        spaceBefore=10, spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        "Body9", parent=styles["Normal"],
        fontSize=9.5, leading=13, textColor=TEXT_DARK,
        spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        "CheckItem", parent=styles["Normal"],
        fontSize=9.5, leading=13, textColor=TEXT_DARK,
        leftIndent=14, spaceAfter=2
    ))
    styles.add(ParagraphStyle(
        "CodeText", parent=styles["Normal"],
        fontSize=9, leading=12, textColor=TEXT_DARK,
        fontName="Courier", leftIndent=14, spaceAfter=2
    ))
    styles.add(ParagraphStyle(
        "SmallNote", parent=styles["Normal"],
        fontSize=8, leading=10, textColor=TEXT_MID, spaceAfter=2
    ))
    styles.add(ParagraphStyle(
        "TableCell", parent=styles["Normal"],
        fontSize=8.5, leading=11, textColor=TEXT_DARK
    ))
    styles.add(ParagraphStyle(
        "TableHeader", parent=styles["Normal"],
        fontSize=8.5, leading=11, textColor=WHITE, fontName="Helvetica-Bold"
    ))
    styles.add(ParagraphStyle(
        "PromptText", parent=styles["Normal"],
        fontSize=8.5, leading=11, textColor=TEXT_MID,
        fontName="Courier", leftIndent=14, spaceAfter=6,
        borderColor=BORDER_GRAY, borderWidth=0.5, borderPadding=4
    ))
    return styles


def build_overview_table(styles):
    header = [
        Paragraph("<b>Step</b>", styles["TableHeader"]),
        Paragraph("<b>What</b>", styles["TableHeader"]),
        Paragraph("<b>Time</b>", styles["TableHeader"]),
        Paragraph("<b>Status</b>", styles["TableHeader"]),
        Paragraph("<b>Done</b>", styles["TableHeader"]),
    ]

    rows = [
        ["", Paragraph("<b>Part 1 — Builder Stack</b>", styles["TableCell"]), "", "", ""],
        ["1", "Terminal Basics", "~15 min", "Required", "[ ]"],
        ["2", "Code Editor + Extensions", "~15 min", "Required", "[ ]"],
        ["3", "Git", "~10 min", "Required", "[ ]"],
        ["4", "GitHub", "~15 min", "Required", "[ ]"],
        ["5", "AI Coding CLIs", "~15 min", "Required", "[ ]"],
        ["6", "AI Registry + Plugins", "~20 min", "Optional", "[ ]"],
        ["7", "Voice to Text", "~10 min", "Optional", "[ ]"],
        ["", Paragraph("<b>Part 2 — AI Platform Setup</b>", styles["TableCell"]), "", "", ""],
        ["8", "AI Platform Accounts", "~10 min", "Required", "[ ]"],
        ["9", "Personalization", "~15 min", "Recommended", "[ ]"],
        ["10", "Memory Systems", "~10 min", "Recommended", "[ ]"],
        ["11", "MCP Connections", "~15 min", "Optional", "[ ]"],
    ]

    data = [header] + rows
    col_widths = [0.4 * inch, 2.5 * inch, 0.8 * inch, 1.0 * inch, 0.5 * inch]

    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        # Header
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8.5),
        # Section headers (rows 1 and 9)
        ("BACKGROUND", (0, 1), (-1, 1), LIGHT_ACCENT),
        ("BACKGROUND", (0, 9), (-1, 9), LIGHT_ACCENT),
        ("SPAN", (1, 1), (3, 1)),
        ("SPAN", (1, 9), (3, 9)),
        # Body
        ("FONTSIZE", (0, 1), (-1, -1), 8.5),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("ALIGN", (3, 0), (3, -1), "CENTER"),
        ("ALIGN", (4, 0), (4, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        # Alternating rows
        ("BACKGROUND", (0, 2), (-1, 2), LIGHT_GRAY),
        ("BACKGROUND", (0, 4), (-1, 4), LIGHT_GRAY),
        ("BACKGROUND", (0, 6), (-1, 6), LIGHT_GRAY),
        ("BACKGROUND", (0, 8), (-1, 8), LIGHT_GRAY),
        ("BACKGROUND", (0, 10), (-1, 10), LIGHT_GRAY),
        ("BACKGROUND", (0, 12), (-1, 12), LIGHT_GRAY),
        # Grid
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_GRAY),
        ("ROWHEIGHTS", (0, 0), (-1, -1), 18),
    ]))
    return table


def build_step(story, styles, num, title, instructions, verification, ask_ai=None):
    story.append(Paragraph(f"<b>Step {num}: {title}</b>", styles["StepHead"]))
    for line in instructions:
        story.append(Paragraph(line, styles["Body9"]))
    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>You know it worked when:</b>", styles["Body9"]))
    for v in verification:
        story.append(Paragraph(f"[ ]  {v}", styles["CheckItem"]))
    if ask_ai:
        story.append(Spacer(1, 3))
        story.append(Paragraph("<i>Ask AI for help:</i>", styles["SmallNote"]))
        story.append(Paragraph(ask_ai, styles["PromptText"]))
    story.append(Spacer(1, 6))


def build_pdf():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    doc = SimpleDocTemplate(
        OUTPUT_PATH, pagesize=letter,
        topMargin=0.6 * inch, bottomMargin=0.6 * inch,
        leftMargin=0.75 * inch, rightMargin=0.75 * inch
    )
    styles = get_styles()
    story = []

    # --- Page 1: Title + Overview Table ---
    story.append(Paragraph("Agentic AI for Leaders", styles["DocTitle"]))
    story.append(Paragraph("Setup Checklist — Complete before Session 1", styles["DocSubtitle"]))
    story.append(Paragraph(
        "Work through these 11 steps in order. Budget 2–3 hours total. "
        "Check off each step as you complete it.",
        styles["Body9"]
    ))
    story.append(Spacer(1, 8))
    story.append(build_overview_table(styles))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "Full instructions with screenshots: <b>handsonai.info/courses/tools-setup-checklist/</b>",
        styles["Body9"]
    ))

    # --- Page 2-3: Builder Stack ---
    story.append(PageBreak())
    story.append(Paragraph("Part 1 — Builder Stack", styles["SectionHead"]))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT))
    story.append(Spacer(1, 6))

    build_step(story, styles, 1, "Terminal Basics",
        [
            "Open your terminal: <b>Mac</b> — Cmd+Space, type Terminal. "
            "<b>Windows</b> — Start → PowerShell.",
            "Practice: <font face='Courier' size='9'>pwd</font> (Mac) or "
            "<font face='Courier' size='9'>Get-Location</font> (Windows) to see your current directory.",
        ],
        [
            "Terminal opens and shows a prompt ($ or % or >)",
            "pwd / Get-Location prints a directory path",
        ],
        "I'm learning to use the terminal on [Mac / Windows] and ran into this issue: "
        "[describe what happened]. What should I try?"
    )

    build_step(story, styles, 2, "Code Editor + Extensions",
        [
            "Install <b>Cursor</b> (cursor.com) or <b>VS Code</b> (code.visualstudio.com).",
            "Open Extensions (Cmd/Ctrl+Shift+X) → search and install an AI extension (Claude Code, Codex, or Gemini Code Assist).",
        ],
        [
            "Editor opens and File → Open Folder shows files in the sidebar",
            "At least one AI extension installed (Claude Code, Codex, or Gemini Code Assist)",
        ],
        "I'm setting up [Cursor / VS Code] on [Mac / Windows] and running into: "
        "[describe issue]. What should I try?"
    )

    build_step(story, styles, 3, "Git",
        [
            "<b>Mac:</b> Run <font face='Courier' size='9'>xcode-select --install</font> in Terminal.",
            "<b>Windows:</b> Download from git-scm.com and run installer (use defaults).",
        ],
        [
            "git --version prints a version number",
        ],
        "I'm trying to install Git on [Mac / Windows] and getting: [paste error]. What should I try?"
    )

    build_step(story, styles, 4, "GitHub",
        [
            "Create account at github.com. Clone a repo: Cmd/Ctrl+Shift+P → Git: Clone → paste URL.",
        ],
        [
            "GitHub account created",
            "Cloned repo files appear in editor sidebar",
            "git status shows 'On branch main'",
        ],
        "I'm trying to clone a GitHub repo in [Cursor / VS Code] and getting: [paste error]. What should I try?"
    )

    build_step(story, styles, 5, "AI Coding CLIs (Claude Code)",
        [
            "<b>Mac/Linux:</b> <font face='Courier' size='9'>"
            "curl -fsSL https://claude.ai/install.sh | bash</font>",
            "<b>Windows:</b> <font face='Courier' size='9'>"
            "irm https://claude.ai/install.ps1 | iex</font>",
            "Then run <font face='Courier' size='9'>claude</font> and follow sign-in prompts.",
        ],
        [
            "claude --version prints a version number",
            "claude starts a conversation in the terminal",
        ],
        "I'm trying to install Claude Code on [Mac / Windows] and getting: [paste error]. What should I try?"
    )

    build_step(story, styles, 6, "AI Registry + Plugins (Optional)",
        [
            "Open the Notion AI Registry template (link on setup checklist page) → click Duplicate.",
            "In Claude Code: <font face='Courier' size='9'>/plugin marketplace add jamesgray-ai/handsonai-plugins</font>",
            "Then: <font face='Courier' size='9'>/plugin install business-first-ai@handsonai</font>",
        ],
        [
            "Four databases visible in Notion workspace",
            "Plugin commands run without errors in Claude Code",
        ]
    )

    build_step(story, styles, 7, "Voice to Text (Optional)",
        [
            "Install <b>Wispr Flow</b> (wisprflow.ai) or enable <b>Claude Desktop Quick Entry</b>.",
            "Grant microphone permissions when prompted.",
        ],
        [
            "Voice dictation works in any text field",
        ]
    )

    # --- Page 3-4: AI Platform Setup ---
    story.append(PageBreak())
    story.append(Paragraph("Part 2 — AI Platform Setup", styles["SectionHead"]))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "You only need <b>one</b> platform set up. Use whichever you prefer.",
        styles["Body9"]
    ))
    story.append(Spacer(1, 4))

    build_step(story, styles, 8, "AI Platform Accounts",
        [
            "<b>ChatGPT:</b> chat.openai.com → Sign up → Upgrade to Plus ($20/mo)",
            "<b>Claude:</b> claude.ai → Sign up → Upgrade to Pro ($20/mo)",
            "<b>Gemini:</b> gemini.google.com → Sign in → Upgrade to Advanced ($20/mo)",
        ],
        [
            "Paid account active on at least one platform",
            "Can start a conversation and get a response",
        ]
    )

    build_step(story, styles, 9, "Personalization / Custom Instructions",
        [
            "<b>ChatGPT:</b> Profile picture → Customize ChatGPT → fill both sections",
            "<b>Claude:</b> Initials → Settings → Profile preferences",
            "<b>Gemini:</b> Profile → Settings → Personalization",
            "<b>Starter template:</b> \"I'm a [role] in [industry]. I'm learning to build AI-powered "
            "workflows and agents. I prefer concise answers with practical examples.\"",
        ],
        [
            "Custom instructions / preferences saved",
        ],
        "I'm trying to set up custom instructions in [ChatGPT / Claude / Gemini] "
        "and can't find the setting. Where do I go?"
    )

    build_step(story, styles, 10, "Memory Systems",
        [
            "<b>ChatGPT:</b> Profile → Settings → Personalization → toggle Memory on",
            "<b>Claude:</b> Initials → Settings → toggle Memory on",
            "<b>Gemini (personal):</b> Settings → Saved Info — memory builds automatically",
            "<b>Gemini (Workspace):</b> Automated memory may not be available — check with your admin",
        ],
        [
            "Memory toggle is on",
        ],
        "I'm trying to enable memory in [ChatGPT / Claude / Gemini] but can't find the toggle. "
        "I'm on [web / desktop] with a [Free / Plus / Pro] plan. Where do I look?"
    )

    build_step(story, styles, 11, "MCP Connections (Optional)",
        [
            "<b>Claude (web):</b> Settings → Connectors → browse directory or add custom MCP server URL",
            "<b>Claude Desktop:</b> Connectors + local MCP servers "
            "(see handsonai.info/mcp-server/)",
            "<b>Claude Cowork:</b> Inherits your connectors and MCP servers automatically",
            "<b>ChatGPT:</b> Profile → Settings → Connected Apps → connect integrations",
            "<b>Gemini:</b> Settings → Extensions → enable Google Workspace, etc.",
        ],
        [
            "At least one external tool or MCP server connected",
        ]
    )

    # --- Page 5: Quick Reference ---
    story.append(PageBreak())
    story.append(Paragraph("Quick Reference Card", styles["SectionHead"]))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Verification Commands</b>", styles["StepHead"]))
    cmds = [
        ["Terminal", "pwd  (Mac)  /  Get-Location  (Windows)"],
        ["Git", "git --version"],
        ["GitHub", "git status  (inside cloned repo)"],
        ["Claude Code", "claude --version"],
    ]
    cmd_table = Table(
        [[Paragraph(f"<b>{r[0]}</b>", styles["TableCell"]),
          Paragraph(f"<font face='Courier'>{r[1]}</font>", styles["TableCell"])]
         for r in cmds],
        colWidths=[1.5 * inch, 4.5 * inch]
    )
    cmd_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), LIGHT_GRAY),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_GRAY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWHEIGHTS", (0, 0), (-1, -1), 20),
    ]))
    story.append(cmd_table)
    story.append(Spacer(1, 14))

    story.append(Paragraph("<b>Platform Settings Paths</b>", styles["StepHead"]))
    plat_data = [
        [Paragraph("<b>Platform</b>", styles["TableHeader"]),
         Paragraph("<b>Personalization</b>", styles["TableHeader"]),
         Paragraph("<b>Memory</b>", styles["TableHeader"])],
        ["ChatGPT", "Profile pic → Customize ChatGPT", "Settings → Personalization → Memory"],
        ["Claude", "Initials → Settings → Preferences", "Initials → Settings → Memory"],
        ["Gemini", "Profile → Settings", "Settings → Saved Info (personal only)"],
    ]
    plat_table = Table(plat_data, colWidths=[1.0 * inch, 2.5 * inch, 2.5 * inch])
    plat_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("BACKGROUND", (0, 2), (-1, 2), LIGHT_GRAY),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_GRAY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWHEIGHTS", (0, 0), (-1, -1), 20),
    ]))
    story.append(plat_table)
    story.append(Spacer(1, 14))

    story.append(Paragraph("<b>\"Ask AI for Help\" Template</b>", styles["StepHead"]))
    story.append(Paragraph(
        "Copy and paste this into any AI chat when you get stuck:",
        styles["Body9"]
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "I'm following the Agentic AI for Leaders setup checklist and I'm stuck on "
        "Step [number]: [step name]. I'm on [Mac / Windows] and here's what happened: "
        "[describe the issue or paste the error message]. What should I try next?",
        styles["PromptText"]
    ))
    story.append(Spacer(1, 14))

    story.append(Paragraph(
        "<b>Full interactive checklist:</b> handsonai.info/courses/tools-setup-checklist/",
        styles["Body9"]
    ))
    story.append(Paragraph(
        "<b>Course page:</b> handsonai.info/courses/leaders/",
        styles["Body9"]
    ))

    # Build
    doc.build(story)
    print(f"PDF generated: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_pdf()
