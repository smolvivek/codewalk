#!/usr/bin/env python3
"""
verify_walkthrough.py -- Post-build validation for codewalk output.

Checks a generated walkthrough HTML (and optionally the repo it was built from)
for structural correctness, provenance integrity, credential leaks, and style
rules.

Usage:
    python scripts/verify_walkthrough.py path/to/walkthrough.html [--repo path/to/repo] [--mode changes]

Exit codes:
    0  all checks passed
    1  one or more checks failed (details printed to stderr)
"""

import argparse
import json
import os
import re
import sys
from html.parser import HTMLParser


class WalkthroughParser(HTMLParser):
    """Extracts structured data from a walkthrough HTML file."""

    def __init__(self):
        super().__init__()
        self.modules = []  # list of dicts with provenance, trace_steps, slug
        self.trace_data = None  # parsed JSON from #trace-data
        self.quiz_state = None  # parsed JSON from #quiz-state
        self.brief_paths = []  # data-paths from agent brief elements
        self.current_json_id = None
        self.current_json_buf = []
        self.in_json_block = False
        self.all_text = []  # all visible text for lint checks
        self.in_style_or_script = False

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)

        # Detect modules by data-provenance
        if "data-provenance" in attr_dict:
            module = {
                "provenance": attr_dict["data-provenance"],
                "trace_steps": attr_dict.get("data-trace-steps", "").split(",") if attr_dict.get("data-trace-steps") else [],
                "slug": attr_dict.get("id", ""),
            }
            self.modules.append(module)

        # Detect brief data-paths
        if "data-paths" in attr_dict:
            paths = attr_dict["data-paths"].split(",")
            self.brief_paths.extend(p.strip() for p in paths if p.strip())

        # Detect JSON script blocks
        if tag == "script":
            script_type = attr_dict.get("type", "")
            script_id = attr_dict.get("id", "")
            if script_type == "application/json" and script_id in ("trace-data", "quiz-state"):
                self.current_json_id = script_id
                self.current_json_buf = []
                self.in_json_block = True
            elif tag == "script" or tag == "style":
                self.in_style_or_script = True

        if tag == "style":
            self.in_style_or_script = True

    def handle_endtag(self, tag):
        if tag == "script" and self.in_json_block:
            raw = "".join(self.current_json_buf)
            try:
                data = json.loads(raw)
                if self.current_json_id == "trace-data":
                    self.trace_data = data
                elif self.current_json_id == "quiz-state":
                    self.quiz_state = data
            except json.JSONDecodeError:
                pass  # Will be caught as a failure later if needed
            self.in_json_block = False
            self.current_json_id = None

        if tag in ("script", "style"):
            self.in_style_or_script = False

    def handle_data(self, data):
        if self.in_json_block:
            self.current_json_buf.append(data)
        elif not self.in_style_or_script:
            self.all_text.append(data)


# ---------------------------------------------------------------------------
# Credential patterns
# ---------------------------------------------------------------------------

CREDENTIAL_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),  # AWS access key
    re.compile(r"sk-[a-zA-Z0-9]{20,}"),  # OpenAI / Stripe secret key
    re.compile(r"ghp_[a-zA-Z0-9]{36}"),  # GitHub personal access token
    re.compile(r"gho_[a-zA-Z0-9]{36}"),  # GitHub OAuth token
    re.compile(r"ghs_[a-zA-Z0-9]{36}"),  # GitHub server token
    re.compile(r"-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----"),
    re.compile(r"Bearer\s+[a-zA-Z0-9._\-]{20,}"),
]


def check_credentials(text, context=""):
    """Return a list of credential-pattern matches found in text."""
    findings = []
    for pattern in CREDENTIAL_PATTERNS:
        for match in pattern.finditer(text):
            findings.append(f"Credential pattern in {context}: {match.group()[:30]}...")
    return findings


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def run_checks(html_path, repo_path=None, mode="walkthrough"):
    errors = []
    warnings = []

    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Parse HTML
    parser = WalkthroughParser()
    parser.feed(html_content)

    full_text = "".join(parser.all_text)

    # -- 1. Provenance labels --
    if not parser.modules:
        errors.append("No modules with data-provenance found. Every module needs an Observed or Read badge.")
    else:
        for mod in parser.modules:
            if mod["provenance"] not in ("observed", "read"):
                errors.append(f"Module '{mod['slug']}' has invalid provenance: '{mod['provenance']}'. Must be 'observed' or 'read'.")

    # -- 2. Trace step references --
    if parser.trace_data:
        trace_step_ids = {s["id"] for s in parser.trace_data.get("steps", [])}
        for mod in parser.modules:
            if mod["provenance"] == "observed":
                if not mod["trace_steps"] or mod["trace_steps"] == [""]:
                    errors.append(f"Observed module '{mod['slug']}' has no data-trace-steps.")
                else:
                    for step_id in mod["trace_steps"]:
                        if step_id not in trace_step_ids:
                            errors.append(f"Module '{mod['slug']}' references trace step '{step_id}' which does not exist in trace-data.")

        # Check trace steps point at real files
        if repo_path:
            for step in parser.trace_data.get("steps", []):
                step_file = step.get("file", "")
                if step_file:
                    full_path = os.path.join(repo_path, step_file)
                    if not os.path.isfile(full_path):
                        errors.append(f"Trace step '{step['id']}' references file '{step_file}' which does not exist in the repo.")

        # Check trace for credential patterns
        trace_raw = json.dumps(parser.trace_data)
        cred_findings = check_credentials(trace_raw, "trace-data")
        errors.extend(cred_findings)

    else:
        # No trace data is fine if all modules are Read
        observed = [m for m in parser.modules if m["provenance"] == "observed"]
        if observed:
            errors.append(f"{len(observed)} module(s) marked Observed but no trace-data block found.")

    # -- 3. Brief data-paths --
    if repo_path and parser.brief_paths:
        for p in parser.brief_paths:
            full_path = os.path.join(repo_path, p)
            if not os.path.isfile(full_path):
                errors.append(f"Agent brief data-paths references '{p}' which does not exist in the repo.")

    # -- 4. Credential scan in full HTML --
    cred_in_html = check_credentials(html_content, "HTML content")
    errors.extend(cred_in_html)

    # -- 5. No emoji --
    # Check for emoji in visible text (Unicode ranges for common emoji)
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # misc symbols
        "\U0001F680-\U0001F6FF"  # transport
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"  # dingbats
        "\U0001F900-\U0001F9FF"  # supplemental
        "\U0001FA00-\U0001FA6F"  # chess
        "\U0001FA70-\U0001FAFF"  # symbols extended
        "\U00002600-\U000026FF"  # misc symbols
        "]+",
        flags=re.UNICODE,
    )
    emoji_matches = emoji_pattern.findall(full_text)
    if emoji_matches:
        errors.append(f"Emoji found in visible text: {emoji_matches[:5]}")

    # -- 6. No forbidden word (except in the attribution link) --
    # Remove the attribution link text before checking
    excluded = "codebase-to-" + "cour" + "se"
    forbidden = "cour" + "se"
    text_without_link = re.sub(re.escape(excluded), "", full_text, flags=re.IGNORECASE)
    if re.search(r"\b" + forbidden + r"\b", text_without_link, re.IGNORECASE):
        errors.append(f"The word '{forbidden}' appears in visible text outside the attribution link.")

    # -- 7. No em dashes --
    em_dash = chr(0x2014)
    if em_dash in full_text:
        count = full_text.count(em_dash)
        errors.append(f"Em dash found {count} time(s) in visible text. Use commas, periods, or colons instead.")

    # -- 8. Quiz state block exists --
    if '<script type="application/json" id="quiz-state">' not in html_content:
        warnings.append("No #quiz-state JSON block found. Progress persistence may not work.")

    # -- 9. Prediction cards exist --
    if "predict-card" not in html_content and "predict-question" not in html_content:
        warnings.append("No prediction cards found. Every module should have a predict step.")

    # -- 10. Confidence controls --
    if 'data-confidence=' not in html_content:
        warnings.append("No confidence controls found. Predictions need a confidence mark.")

    # -- 11. Copy my progress button --
    if "Copy my progress" not in html_content and "copy-progress" not in html_content:
        warnings.append("No 'Copy my progress' button found in the page.")

    # -- 12. Mode-specific checks --
    if mode == "changes":
        # Change mode should have verdict options
        if "merge" not in full_text.lower():
            warnings.append("Change mode page does not appear to have a merge verdict section.")

    return errors, warnings


def main():
    argp = argparse.ArgumentParser(description="Validate a codewalk walkthrough HTML file.")
    argp.add_argument("html", help="Path to the walkthrough HTML file")
    argp.add_argument("--repo", help="Path to the repo the walkthrough was built from", default=None)
    argp.add_argument("--mode", choices=["walkthrough", "changes"], default="walkthrough",
                       help="Validation mode: walkthrough (default) or changes")
    args = argp.parse_args()

    if not os.path.isfile(args.html):
        print(f"Error: file not found: {args.html}", file=sys.stderr)
        sys.exit(1)

    errors, warnings = run_checks(args.html, repo_path=args.repo, mode=args.mode)

    if warnings:
        for w in warnings:
            print(f"  warning: {w}", file=sys.stderr)

    if errors:
        print(f"\n{len(errors)} error(s) found:", file=sys.stderr)
        for e in errors:
            print(f"  error: {e}", file=sys.stderr)
        sys.exit(1)
    else:
        passed = len([m for m in WalkthroughParser().modules]) if not errors else 0
        print(f"All checks passed. {len(warnings)} warning(s).", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
