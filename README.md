# ISIT225 — Week 6 Cloud Security Fix-It Lab (git version)

**This is the optional git/GitHub version of the exercise.** Most students
should use the in-browser version linked from the course site instead — it
needs no GitHub account and tracks your progress automatically. Use this
version only if you already know git and want the practice.

**Topic:** Cloud Security and Privacy · **Time budget:** 30–40 minutes ·
**Auto-graded:** yes, by GitHub Actions on every push · **Cost:** none — no
payment method, no billing, no sign-up beyond a free GitHub account.

## Scenario

A contractor set up a small cloud deployment for "Northgate Retail" and left
before finishing the security review. Six things are wrong in
[`cloud_config.tf`](cloud_config.tf). Find and fix all six, then document the
risk in [`risk_register.md`](risk_register.md).

This is a **static-analysis exercise** — `cloud_config.tf` is teaching-only
HCL. Nothing is deployed, no cloud account or credit card is needed, and no
`terraform` binary is required. A Python script reads the file as text.

## 1. Get your own copy

Click **Use this template** → **Create a new repository** at the top of this
page, and create it under **your own GitHub account** (not this org). This
gives you your own copy with a clean commit history.

If Actions don't run automatically on your first push, open the **Actions**
tab in your new repo and click **"I understand my workflows, go ahead and
enable them."**

## 2. Edit it — free, in your browser, no container

Press **`.`** on your repo's GitHub page (or change `github.com` to
`github.dev` in the URL). This opens a full VS Code editor in your browser —
nothing to install, nothing to start, no payment method ever asked for. Edit
the two files, commit with the Source Control panel on the left, and push.

If you have Python installed locally and would rather work that way, that
works too — clone the repo and run `python3 scanner.py` from a terminal.

## 3. Fix the six issues

Open `cloud_config.tf`. Each vulnerable line has a `# FIX N:` comment telling
you what's wrong. Fix them **one at a time and commit after each fix** —
your instructor looks at the commit history, not just the final state.

If you have Python locally, check your progress any time with:

```bash
python3 scanner.py
```

## 4. Rename the bucket to your own name

One of the fixes is renaming the storage bucket from `app-data-public` to
`app-data-<your-github-username>` (lowercase, hyphens instead of anything
else). **This is checked automatically against the repo owner** — copying a
classmate's already-fixed file will fail this specific check on your repo,
because it still has their username in it, not yours.

## 5. Fill in the risk register

Open `risk_register.md` and replace at least 5 of the `TODO` rows with real
threats: a description, likelihood (1–5), impact (1–5), and a mitigation.
Base these on the six fixes and this week's lecture (CIA model, threats and
attack surfaces, IAM, encryption, monitoring).

## 6. Push and check your grade

```bash
git push
```

Open the **Actions** tab in your repo (or look for the ✅ / ❌ next to your
latest commit) — the workflow runs `scanner.py` and posts a pass/fail report
for all 8 checks as a job summary. GitHub Actions is free on a public repo
like this one, no matter how many times you push.

## 7. Submit

This repo does **not** mark anything done automatically on the course site —
that only happens through the in-browser version. Paste the link to **your
own repo** (with the green ✅) into this week's DevSecOps evidence box on the
course platform, along with a one-sentence summary of your fixes.

A Kubernetes/Linux-flavored backup scenario for Killercoda is also included
in [`killercoda/`](killercoda/), for your instructor to import if this
version is ever needed as a fallback.

## Spot check (for your instructor)

This is a lightweight, ungraded integrity check: pick a couple of students at
random and ask them to explain one fix out loud for two minutes. A student
who worked through it can always do this; a copy-paste cannot.
