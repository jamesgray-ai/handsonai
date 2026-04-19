#!/usr/bin/env python3
"""Grade editing-hbr-articles outputs against assertions."""
import json
import re
import sys
from pathlib import Path

WORKSPACE = Path(__file__).parent.parent

BANNED_JARGON = [
    "leveraging", "leverage", "utilize", "utilization", "utilized",
    "synergies", "best-in-class", "in order to", "at the end of the day",
    "moving forward",
]

HEDGE_WORDS = ["perhaps", "it seems", "it seems that"]

SUPERLATIVES = [
    "revolutionary", "game-changing", "unprecedented", "groundbreaking",
    "nothing short of", "absolutely transformative", "truly unprecedented",
    "incredible",
]

PROMOTIONAL_PHRASES = [
    "don't be left behind", "left behind in the dust",
    "the future belongs to", "insurmountable competitive advantage",
    "make no mistake",
]

PASSIVE_PATTERNS = [
    r"\b(?:is|are|was|were|been|being)\s+(?:being\s+)?(?:\w+ed|transformed|adopted|achieved|utilized|recognized|reported|encountered|driven|accelerated|embedded|built|generated|created|made|delivered|rewarded)\b",
]


def count_words(text: str) -> int:
    return len(text.split())


def find_matches(text: str, terms: list[str]) -> list[str]:
    text_lower = text.lower()
    return [t for t in terms if t.lower() in text_lower]


def count_passive(text: str) -> int:
    count = 0
    for pattern in PASSIVE_PATTERNS:
        count += len(re.findall(pattern, text, re.IGNORECASE))
    return count


def has_throat_clearing(text: str) -> bool:
    first_para = text.split("\n\n")[0] if "\n\n" in text else text[:500]
    lines = [l for l in first_para.split("\n") if l.strip() and not l.startswith("#")]
    if not lines:
        return False
    first_text = lines[0].lower()
    openers = [
        "in today's", "in an era", "in the modern", "it's important to note",
        "the world is changing", "as we all know",
    ]
    return any(o in first_text for o in openers)


def grade_run(run_dir: Path, test_name: str) -> dict:
    """Grade a single run directory."""
    article_path = run_dir / "outputs" / "edited-article.md"
    summary_path = run_dir / "outputs" / "editorial-summary.md"

    if not article_path.exists():
        return {"error": f"No edited article found at {article_path}"}

    article = article_path.read_text()
    summary = summary_path.read_text() if summary_path.exists() else ""
    combined = article + "\n" + summary

    results = {"word_count": count_words(article)}
    assertions = []

    if "jargon-heavy" in test_name:
        tc = has_throat_clearing(article)
        assertions.append({
            "text": "No throat-clearing opener",
            "passed": not tc,
            "evidence": "First paragraph starts with throat-clearing" if tc else "Clean opening"
        })

        found = find_matches(article, BANNED_JARGON)
        assertions.append({
            "text": "Banned jargon terms eliminated",
            "passed": len(found) == 0,
            "evidence": f"Found: {found}" if found else "No banned jargon found"
        })

        found = find_matches(article, HEDGE_WORDS)
        assertions.append({
            "text": "Hedge words removed",
            "passed": len(found) == 0,
            "evidence": f"Found: {found}" if found else "No hedge words found"
        })

        vague = find_matches(article, ["a major retailer", "significant savings", "several leading companies", "a healthcare company", "a manufacturer"])
        assertions.append({
            "text": "Vague evidence replaced or flagged",
            "passed": len(vague) == 0,
            "evidence": f"Vague phrases remain: {vague}" if vague else "No vague evidence phrases found"
        })

        has_summary = bool(re.search(r"(?:editorial summary|major changes|word count)", combined, re.IGNORECASE))
        assertions.append({
            "text": "Editorial summary provided",
            "passed": has_summary,
            "evidence": "Summary section found" if has_summary else "No editorial summary detected"
        })

        passive_count = count_passive(article)
        assertions.append({
            "text": "Active voice dominant (<=2 passive)",
            "passed": passive_count <= 2,
            "evidence": f"Found {passive_count} passive constructions"
        })

    elif "weak-evidence" in test_name:
        found = find_matches(article, SUPERLATIVES)
        assertions.append({
            "text": "Superlatives eliminated",
            "passed": len(found) == 0,
            "evidence": f"Found: {found}" if found else "No superlatives found"
        })

        specific_evidence = re.findall(r"(?:[$%]\d|\d+%|\$\d|\d+ (?:percent|million|billion))", article)
        editor_flags = re.findall(r"\[(?:EDITOR|NOTE|TODO|INSERT)[^\]]*\]", article, re.IGNORECASE)
        total_evidence = len(specific_evidence) + len(editor_flags)
        assertions.append({
            "text": "At least 3 specific evidence points or editor flags",
            "passed": total_evidence >= 3,
            "evidence": f"Found {len(specific_evidence)} data points and {len(editor_flags)} editor flags"
        })

        risk_terms = ["risk", "challenge", "limitation", "failure", "downside", "concern", "caution", "drawback"]
        found_risk = find_matches(article, risk_terms)
        assertions.append({
            "text": "Balance: risks/limitations discussed",
            "passed": len(found_risk) >= 2,
            "evidence": f"Risk-related terms found: {found_risk}" if found_risk else "No risk discussion detected"
        })

        found = find_matches(article, PROMOTIONAL_PHRASES)
        assertions.append({
            "text": "Promotional/fear-based CTAs removed",
            "passed": len(found) == 0,
            "evidence": f"Found: {found}" if found else "No promotional phrases found"
        })

        has_summary = bool(re.search(r"(?:editorial summary|major changes)", combined, re.IGNORECASE))
        assertions.append({
            "text": "Editorial summary provided",
            "passed": has_summary,
            "evidence": "Summary section found" if has_summary else "No editorial summary detected"
        })

    elif "bloated-redundant" in test_name:
        original_path = WORKSPACE / "test-article-3-bloated-redundant.md"
        original_wc = count_words(original_path.read_text()) if original_path.exists() else 2400
        edited_wc = count_words(article)
        reduction = (original_wc - edited_wc) / original_wc * 100

        assertions.append({
            "text": "Word count reduced at least 25%",
            "passed": reduction >= 25,
            "evidence": f"Original: {original_wc}, Edited: {edited_wc}, Reduction: {reduction:.1f}%"
        })

        democratiz_count = len(re.findall(r"democratiz(?:ation|ed|ing|e)", article, re.IGNORECASE))
        assertions.append({
            "text": "Democratization concept not over-repeated (<=3 mentions)",
            "passed": democratiz_count <= 3,
            "evidence": f"'Democratiz*' appears {democratiz_count} times"
        })

        passive_count = count_passive(article)
        assertions.append({
            "text": "Passive voice reduced (<=5 instances)",
            "passed": passive_count <= 5,
            "evidence": f"Found {passive_count} passive constructions"
        })

        sections = re.split(r"\n##\s+", article)
        conclusion = sections[-1] if len(sections) > 1 else article[-500:]
        rehash = find_matches(conclusion, ["three fundamental ways", "as we have discussed", "as we've discussed"])
        assertions.append({
            "text": "Conclusion doesn't rehash intro",
            "passed": len(rehash) == 0,
            "evidence": f"Rehash phrases found: {rehash}" if rehash else "No rehash detected"
        })

        has_wc = bool(re.search(r"(?:word count|words?.*→|words?.*->|\d+\s*→\s*\d+|\d+%\s*reduction)", combined, re.IGNORECASE))
        assertions.append({
            "text": "Editorial summary includes word count comparison",
            "passed": has_wc,
            "evidence": "Word count comparison found in summary" if has_wc else "No word count comparison in summary"
        })

    results["expectations"] = assertions
    results["pass_rate"] = sum(1 for a in assertions if a["passed"]) / len(assertions) if assertions else 0
    return results


def main():
    iteration_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else WORKSPACE / "iteration-1"

    for test_dir in sorted(iteration_dir.iterdir()):
        if not test_dir.is_dir() or not test_dir.name.startswith("e"):
            continue

        print(f"\n{'='*60}")
        print(f"  {test_dir.name}")
        print(f"{'='*60}")

        for config in ["with_skill", "without_skill"]:
            config_dir = test_dir / config
            if not config_dir.exists():
                continue

            print(f"\n  [{config}]")
            results = grade_run(config_dir, test_dir.name)

            if "error" in results:
                print(f"    ERROR: {results['error']}")
                continue

            print(f"    Word count: {results['word_count']}")

            for a in results.get("expectations", []):
                status = "PASS" if a["passed"] else "FAIL"
                print(f"    [{status}] {a['text']}")
                print(f"           {a['evidence']}")

            print(f"    Pass rate: {results['pass_rate']:.0%}")

            grading_path = config_dir / "grading.json"
            grading_path.write_text(json.dumps(results, indent=2))
            print(f"    Saved: {grading_path}")


if __name__ == "__main__":
    main()
