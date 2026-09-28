#!/usr/bin/env python3
"""
scanner.py — static-analysis grader for the ISIT225 Cloud Security Fix-It Lab.

Run it yourself any time while you work:
    python3 scanner.py

It checks six configuration issues in cloud_config.tf, your risk register in
risk_register.md, and (only when running in GitHub Actions, where your
GitHub username is known) that you renamed the bucket to your own name
instead of copying someone else's fixed file.

No third-party packages, no `terraform` binary, no cloud account needed —
this only reads text files.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
TF_PATH = os.path.join(ROOT, "cloud_config.tf")
REGISTER_PATH = os.path.join(ROOT, "risk_register.md")

PLACEHOLDER_WORDS = {"", "todo", "tbd", "n/a", "na", "fill in", "fill me in", "?"}


def read(path):
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def find_field(text, resource_block, field):
    """Return the raw right-hand side of `field = ...` inside a named resource
    block, exactly as written (quotes included), or None if not found."""
    block_match = re.search(
        r'resource\s+"[^"]+"\s+"' + re.escape(resource_block) + r'"\s*\{(.*?)\n\}',
        text, re.S,
    )
    if not block_match:
        return None
    block = block_match.group(1)
    m = re.search(r'^\s*' + re.escape(field) + r'\s*=\s*(.+?)\s*(#.*)?$', block, re.M)
    return m.group(1).strip() if m else None


def unquote(raw):
    """Strip one pair of surrounding double quotes, if present."""
    if raw is not None and len(raw) >= 2 and raw.startswith('"') and raw.endswith('"'):
        return raw[1:-1]
    return raw


def normalize_owner(owner):
    """Turn a GitHub username into the token students must use in bucket_name."""
    token = re.sub(r"[^a-z0-9]+", "-", (owner or "").lower()).strip("-")
    return token


def check_config(text):
    results = []

    acl = unquote(find_field(text, "app_data", "acl"))
    results.append(("Bucket is private (not public-read)", (acl or "").lower() == "private", f'acl = "{acl}"'))

    enc = unquote(find_field(text, "app_data", "encryption"))
    results.append(("Bucket encryption is enabled", (enc or "").lower() == "enabled", f'encryption = "{enc}"'))

    log = find_field(text, "app_data", "logging_enabled")
    log_ok = (log or "").lower() == "true"
    results.append(("Bucket logging is enabled", log_ok, f"logging_enabled = {log}"))

    pw = find_field(text, "web_server", "db_password")
    # The value must reference a variable (e.g. var.db_password), never a quoted literal secret.
    pw_ok = bool(pw) and pw.startswith("var.")
    results.append(("No hardcoded secret (db_password references a variable)", pw_ok, f"db_password = {pw}"))

    cidr = find_field(text, "allow_ssh", "cidr_blocks")
    cidr_ok = cidr is not None and "0.0.0.0/0" not in cidr
    results.append(("SSH is not open to the whole internet (0.0.0.0/0)", cidr_ok, f"cidr_blocks = {cidr}"))

    actions = find_field(text, "app_service_account", "actions")
    resources = find_field(text, "app_service_account", "resources")
    iam_ok = bool(actions) and bool(resources) and '"*"' not in actions and '"*"' not in resources
    results.append(('IAM policy follows least privilege (no "*" actions/resources)', iam_ok, f"actions = {actions} / resources = {resources}"))

    bucket_name = unquote(find_field(text, "app_data", "bucket_name"))
    return results, bucket_name


def check_identity(bucket_name, owner):
    if not owner:
        return None  # only enforced in CI, where the owner is known
    expected = "app-data-" + normalize_owner(owner)
    ok = (bucket_name or "").strip() == expected
    detail = f"bucket_name should be \"{expected}\" for your repo owner ({owner}); found \"{bucket_name}\""
    return ("Bucket is renamed to your own repo (not copied from a classmate)", ok, detail)


def check_register(text):
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 4:
            continue
        first = cells[0].lower()
        if first in ("threat", "---", "") or set(first) <= {"-", " "}:
            continue
        if all(set(c) <= {"-", " "} for c in cells):
            continue
        threat, likelihood, impact, mitigation = (cells + ["", "", "", ""])[:4]
        filled = all(
            c.strip().lower() not in PLACEHOLDER_WORDS
            for c in (threat, likelihood, impact, mitigation)
        )
        if filled:
            rows.append((threat, likelihood, impact, mitigation))
    ok = len(rows) >= 5
    return ("Risk register has at least 5 complete threats (likelihood, impact, mitigation)", ok, f"{len(rows)} complete row(s) found"), rows


def main():
    ci = "--ci" in sys.argv
    owner = os.environ.get("GITHUB_REPOSITORY_OWNER", "").strip()

    tf_text = read(TF_PATH)
    if not tf_text:
        print(f"::error::Could not find {TF_PATH}")
        sys.exit(1)

    results, bucket_name = check_config(tf_text)
    identity_result = check_identity(bucket_name, owner) if ci else None
    register_text = read(REGISTER_PATH)
    register_result, _rows = check_register(register_text)

    all_results = results[:]
    if identity_result:
        all_results.append(identity_result)
    all_results.append(register_result)

    lines = ["", "ISIT225 — Cloud Security Fix-It Lab report", "=" * 44]
    passed = 0
    for name, ok, detail in all_results:
        mark = "PASS" if ok else "FAIL"
        lines.append(f"[{mark}] {name}")
        if not ok:
            lines.append(f"       {detail}")
        else:
            passed += 1
    total = len(all_results)
    lines.append("")
    lines.append(f"{passed}/{total} checks passed.")
    if not ci and not owner:
        lines.append("(Bucket-owner check only runs in GitHub Actions, where your username is known.)")
    report = "\n".join(lines)
    print(report)

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as f:
            f.write("## Cloud Security Fix-It Lab — grading report\n\n")
            for name, ok, detail in all_results:
                mark = "✅" if ok else "❌"
                f.write(f"- {mark} **{name}**" + ("" if ok else f" — `{detail}`") + "\n")
            f.write(f"\n**{passed}/{total} checks passed.**\n")

    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
