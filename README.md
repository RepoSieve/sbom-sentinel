# SBOM Sentinel

> **Know what to fix first.**\
> Explainable prioritization for software dependency vulnerabilities.

SBOM Sentinel is a proposed security and machine-learning system for
helping engineering and security teams decide **which software
dependency vulnerabilities should be investigated first**.

Modern applications can contain a large number of third-party
dependencies and vulnerability findings. A vulnerability list alone does
not answer the operational question: **What should the team spend its
next hour investigating?**

SBOM Sentinel addresses this problem by combining Software Bill of
Materials (SBOM) information with vulnerability intelligence, dependency
context, reachability, package health, and other repository signals, and
then using a trained ranking model to produce an explainable
investigation priority.

> **Project status:** Proposed / research-oriented MVP. The
> implementation focus is SBOM upload/import → enrichment → ranking →
> dashboard. Automated repository scanning and continuous integrations
> are considered extensions.

## Current Engineering Base

The repository now starts with a lightweight Python project skeleton so
the team can work through small reviewed pull requests.

## Start Here For Team Members

If you are new to GitHub pull requests, follow this process every day.
Do not work directly on `main`.

### Feature work vs bug fix work

Use the same Git flow for both features and bugs. The difference is the
branch name, issue type, and PR explanation.

For a new feature:

```bash
git checkout main
git pull origin main
git checkout -b feature/issue-2-cyclonedx-parser
```

For a bug fix:

```bash
git checkout main
git pull origin main
git checkout -b bugfix/issue-12-osv-timeout
```

Use `feature/...` when adding new behavior. Use `bugfix/...` when fixing
something that is already supposed to work.

### 1. Get the latest project code

Run this before starting any task:

```bash
git checkout main
git pull origin main
```

This makes sure your local code has the latest work from the team.

### 2. Pick one small task

Open the GitHub issue assigned to you and choose only one checklist item.
One task should be small enough to finish in a day.

Examples:

- Create one parser function.
- Add one test fixture.
- Add one OSV API helper.
- Add one ranking rule.
- Update one documentation file.

### 3. Create a branch for that task

Create a new branch from the latest `main`:

```bash
git checkout -b feature/issue-2-cyclonedx-parser
```

Use this naming style:

```text
feature/issue-<issue-number>-short-task-name
bugfix/issue-<issue-number>-short-task-name
```

Examples:

```text
feature/issue-2-cyclonedx-parser
feature/issue-4-osv-client
feature/issue-3-ranking-score
bugfix/issue-5-demo-command
```

### 4. Make your changes

Edit only the files needed for your task. Avoid changing unrelated files.

After editing, check what changed:

```bash
git status
git diff
```

Use `git status` to see which files changed. Use `git diff` to review
the exact lines before committing.

### 5. Run the project checks

Run the current smoke test:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

Run the CLI:

```bash
PYTHONPATH=src python3 -m sbom_sentinel --help
```

If your task adds a new command, include that command in your PR.

### 6. Commit your work

Add and commit only your task files:

```bash
git add <files-you-changed>
git commit -m "Add CycloneDX parser skeleton"
```

Good commit messages are short and specific.

### 7. Push your branch

```bash
git push -u origin feature/issue-2-cyclonedx-parser
```

GitHub will show a link to create a pull request.

### 8. Create the pull request

Open a PR from your branch into `main`.

Fill the PR template fully:

- What changed
- Why
- Linked issue
- How to test
- Expected output
- Known limitations

Do not leave the template blank.

### 9. After review

If the mentor asks for changes:

```bash
git checkout feature/issue-2-cyclonedx-parser
```

Make the fix, run tests again, then:

```bash
git add <files-you-changed>
git commit -m "Address review feedback"
git push
```

The PR updates automatically.

### 10. If `main` changed while you were working

Before continuing work, update your branch with the latest `main`.

Recommended beginner-safe option: merge `main` into your branch.

```bash
git checkout main
git pull origin main
git checkout feature/issue-2-cyclonedx-parser
git merge main
```

If Git reports conflicts, stop and ask for help before guessing.

Advanced option: rebase your branch on top of latest `main`.

```bash
git checkout main
git pull origin main
git checkout feature/issue-2-cyclonedx-parser
git rebase main
```

Use rebase only if you are comfortable with Git. If conflicts happen
during rebase, ask for help. To cancel a rebase:

```bash
git rebase --abort
```

### 11. How to handle merge conflicts

A conflict means Git found two changes in the same part of a file and
needs a human decision.

Conflict markers look like this:

```text
<your branch version marker>
your branch version
<separator marker>
main branch version
<main branch version marker>
```

When this happens:

1. Read both versions carefully.
2. Keep the correct final version.
3. Delete the conflict marker lines.
4. Run tests again.
5. Commit the conflict fix.

For a merge conflict:

```bash
git status
# edit conflicted files
PYTHONPATH=src python3 -m unittest discover -s tests
git add <fixed-files>
git commit
git push
```

For a rebase conflict:

```bash
git status
# edit conflicted files
PYTHONPATH=src python3 -m unittest discover -s tests
git add <fixed-files>
git rebase --continue
git push --force-with-lease
```

Only use `--force-with-lease` after a rebase on your own branch. Never
force-push to `main`.

### 12. Useful Git commands

| Command | Usage |
| --- | --- |
| `git status` | Shows changed files and current branch. |
| `git branch` | Lists local branches. |
| `git checkout main` | Switches to `main`. |
| `git pull origin main` | Gets the latest code from GitHub. |
| `git checkout -b <branch>` | Creates and switches to a new branch. |
| `git diff` | Shows exact line changes before commit. |
| `git add <file>` | Stages selected files for commit. |
| `git commit -m "message"` | Saves staged changes locally. |
| `git push -u origin <branch>` | Uploads your branch to GitHub. |
| `git merge main` | Brings latest `main` into your branch. |
| `git rebase main` | Replays your branch on top of latest `main`. |
| `git rebase --abort` | Cancels a rebase in progress. |
| `git log --oneline --graph --decorate --all` | Shows commit history visually. |

### 13. Best practices

- Always start from latest `main`.
- Never commit directly to `main`.
- One issue checklist item should become one small PR.
- Keep feature branches and bugfix branches separate.
- Run tests before pushing.
- Read your own `git diff` before committing.
- Do not include unrelated file changes.
- Write clear PR descriptions so the mentor can review quickly.
- Ask before resolving conflicts if you are unsure.

### Daily rule

Each member should aim for:

- one small task
- one branch
- one pull request
- one issue checklist update

Small PRs are easier to review and safer to merge.

### Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

## How To Run The Current Skeleton

The current project is a skeleton. It does not yet parse SBOMs, call OSV,
or rank vulnerabilities. For now, students should verify that the base
package, CLI, test setup, and demo script run successfully.

### 1. Clone the repository

```bash
git clone https://github.com/RepoSieve/sbom-sentinel.git
cd sbom-sentinel
```

If the repository is already cloned, get the latest code:

```bash
git checkout main
git pull origin main
```

### 2. Create and activate a virtual environment

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install the project in editable mode

```bash
python -m pip install -e .
```

If `python` is not available, use:

```bash
python3 -m pip install -e .
```

### 4. Run the CLI help command

```bash
python -m sbom_sentinel --help
```

Expected output:

```text
usage: sbom_sentinel [-h] [--version]
```

### 5. Run the version command

```bash
python -m sbom_sentinel --version
```

Expected output:

```text
0.1.0
```

### 6. Run the smoke tests

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

Expected output:

```text
Ran 1 test

OK
```

On Windows PowerShell:

```powershell
$env:PYTHONPATH="src"
python -m unittest discover -s tests
```

### 7. Run the demo script

```bash
scripts/run_demo.sh
```

Expected behavior: the script prints the current CLI help text.

### Current skeleton checklist

Before starting feature work, each student should confirm:

- [ ] Repository is cloned locally.
- [ ] Latest `main` is pulled.
- [ ] Virtual environment is active.
- [ ] Project installs with `pip install -e .`.
- [ ] CLI help command runs.
- [ ] Version command prints `0.1.0`.
- [ ] Smoke test passes.
- [ ] Demo script runs.

### Run the placeholder CLI

```bash
python -m sbom_sentinel --help
python -m sbom_sentinel --version
```

### Run smoke tests

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

### Development workflow

Use the SDLC and PR guidance in:

- `CONTRIBUTING.md`
- `docs/sdlc.md`
- `docs/pr_guidelines.md`
- `.github/pull_request_template.md`

Each student should complete one small task per day and open one focused
pull request when code or documentation changes.

------------------------------------------------------------------------

## Table of Contents

-   [Problem](#problem)
-   [Project Objective](#project-objective)
-   [Project Scope](#project-scope)
-   [System Workflow](#system-workflow)
-   [Core Intelligence](#core-intelligence)
-   [Machine Learning](#machine-learning)
-   [Example](#example)
-   [Explainability](#explainability)
-   [MVP](#mvp)
-   [Product Vision](#product-vision)
-   [Research Question](#research-question)
-   [Research Foundation](#research-foundation)
-   [Project Team](#project-team)
-   [Future Extensions](#future-extensions)
-   [Disclaimer](#disclaimer)

------------------------------------------------------------------------

## Problem

A vulnerability scanner can produce a list of vulnerable dependencies,
but a vulnerability list still leaves an important decision:

> **Which finding matters here, and what should we investigate next?**

Severity alone is not always enough to determine the practical priority
of a vulnerability in a particular application.

For example, two vulnerabilities may have the same CVSS score while
differing significantly in:

-   Known exploitation
-   Application reachability
-   Dependency depth
-   Dependency relationships
-   Package maintenance activity
-   Release activity
-   Available security evidence

SBOM Sentinel therefore focuses on **vulnerability prioritization**,
rather than simply producing another vulnerability list.

------------------------------------------------------------------------

## Project Objective

The primary objective of SBOM Sentinel is to create an **ordered,
explainable investigation queue** for software dependency risks.

The system aims to:

1.  Understand the software components and dependencies in an
    application through an SBOM.
2.  Enrich dependency and vulnerability information with security
    intelligence.
3.  Analyze dependency and reachability context.
4.  Combine multiple signals using a machine-learning ranking model.
5.  Produce a priority ranking for investigation.
6.  Show the evidence and factors behind the ranking.
7.  Support human review when important context is uncertain or missing.

------------------------------------------------------------------------

## Project Scope

The proposed project-domain composition is:

  Area                            Estimated Scope
  ----------------------------- -----------------
  ML / Data Science                           35%
  Cybersecurity                               30%
  Backend / Data Engineering                  15%
  Graph / Dependency Analysis                 10%
  Frontend / Product                           5%
  DevOps / MLOps                               5%

These are project-domain estimates, not percentages of AI-tool usage.

------------------------------------------------------------------------

## System Workflow

The proposed end-to-end workflow is:

``` text
                Software Repository / Existing SBOM
                              |
                              v
                     Generate / Import SBOM
                              |
                              v
                  Detect Vulnerable Dependencies
                              |
                              v
              +-------------------------------+
              | Security & Repository Signals |
              |                               |
              | OSV • NVD • KEV • EPSS       |
              | + repository signals          |
              +-------------------------------+
                              |
                              v
                  Dependency & Reachability
                           Analysis
                              |
                              v
                     ML Ranking Model
                              |
                              v
                    Priority Ranking
                       + Explanations
                              |
                              v
                    Security Dashboard
                              |
                              v
              Downstream Integrations / Actions
              GitHub • Jira • Discord • CI/CD
```

### MVP boundary

The MVP focuses on:

``` text
SBOM Upload / Import
        ↓
Vulnerability & Security Enrichment
        ↓
Dependency / Reachability Analysis
        ↓
ML Prioritization
        ↓
Explainable Investigation Queue
        ↓
Dashboard
```

Automated repository scanning and continuous integrations can be treated
as later extensions.

------------------------------------------------------------------------

## SBOM

A Software Bill of Materials provides structured information about the
software components used by an application.

SBOM Sentinel uses the SBOM as the starting point for understanding:

-   Software components
-   Component versions
-   Dependency relationships
-   Dependency context
-   Potentially vulnerable dependencies

The proposed workflow supports generating or importing an SBOM.

------------------------------------------------------------------------

## Core Intelligence

SBOM Sentinel combines several categories of evidence rather than
relying on one security score.

### Security evidence

-   Vulnerability severity
-   Known exploitation
-   Published exploitability signals

### Package health

-   Package maintenance
-   Package activity
-   Release activity / release frequency

### Application context

-   Dependency relationships
-   Dependency depth
-   Reachability when verified
-   Explicit unknown / missing data

The system is designed to preserve an **unknown** state when information
such as reachability cannot be verified instead of treating missing
information as a definitive negative.

------------------------------------------------------------------------

## Machine Learning

The ML component learns a **multi-signal priority ranking** rather than
relying on severity alone.

Conceptually:

``` text
Security Signals
       +
Dependency Context
       +
Reachability
       +
Package Health
       +
Repository Signals
       |
       v
 ML Ranking Model
       |
       v
Priority Ranking
```

Example feature groups include:

``` text
CVSS
Known exploitation
Reachability
Dependency context
Package health
Release activity
```

The model's output is an **investigation priority ranking**, for
example:

``` text
#1  Fix Now
#2  Investigate
#3  Monitor
```

The project is therefore a ranking/prioritization system rather than
simply a binary vulnerability detector.

------------------------------------------------------------------------

## Example

Consider two vulnerabilities:

### Vulnerability A

``` text
CVSS             = 9.8
Known exploited  = Yes
Dependency depth = 2
Reachable        = Yes
Package activity = Low
Release frequency= Low
```

### Vulnerability B

``` text
CVSS             = 9.8
Known exploited  = No
Dependency depth = 8
Reachable        = No
Package activity = High
Release frequency= High
```

A severity-only approach may treat both findings similarly because both
have a CVSS score of 9.8.

SBOM Sentinel considers the additional signals and uses them to
determine a more context-aware investigation order.

The goal is to answer:

> **Which vulnerability should the security team investigate first?**

------------------------------------------------------------------------

## Explainability

A high-priority result should not be a black box.

SBOM Sentinel is designed to show the factors that contributed to a
finding's priority.

The investigation interface is intended to provide:

-   Priority
-   Security evidence
-   Exploitation evidence
-   Dependency context
-   Reachability information
-   Package context
-   Recommended next action

The project also proposes explainability for the trained ranking model
so users can understand **which factors changed the priority**.

Human review remains important when context is uncertain.

------------------------------------------------------------------------

## MVP

The proposed MVP interface centers on an **Investigation Queue**.

Conceptually, the queue contains:

  -----------------------------------------------------------------------
  Priority          Package           Evidence          Action
  ----------------- ----------------- ----------------- -----------------
  1                 High-risk         Known             Investigate now
                    dependency        exploitation +    
                                      reachable path    

  2                 High-severity     Reachability      Verify exposure
                    dependency        unknown           

  3                 Lower-priority    Limited context   Review
                    dependency                          
  -----------------------------------------------------------------------

The interface is intended to make the next security action clear rather
than simply presenting a large list of CVEs.

------------------------------------------------------------------------

## Product Vision

The product vision is:

> **A clear next action for every dependency risk decision.**

The system aims to provide:

-   An ordered queue
-   Visible evidence
-   Human review where context is uncertain

The central product idea is:

``` text
Many vulnerability findings
          ↓
Context + evidence
          ↓
Prioritized investigation queue
          ↓
Clear next action
```

------------------------------------------------------------------------

## Research Question

The central research question is:

> **Can multi-signal ML prioritization improve investigation ordering
> over severity-only or rule-based baselines?**

The project therefore evaluates the usefulness of combining multiple
signals rather than assuming that a single security metric is
sufficient.

------------------------------------------------------------------------

## Research Foundation

The SBOM Sentinel concept is founded on the paper:

**Supply Chain Risk Analysis via SBOM Data Enrichment**

**Authors:** Antoine Lemay & Neeraj Katiyar\
**Conference:** 2025 IEEE International Systems Conference (SysCon)

The reference work enriches SBOM information with repository maintenance
metadata to analyze software supply-chain risk and identify libraries
with risk factors associated with XZ-style infiltration.

### How SBOM Sentinel extends the foundation

SBOM Sentinel proposes a practical prioritization layer that combines:

-   Vulnerability information
-   Exploitability
-   Dependency information
-   Reachability
-   Package-health signals

and then:

``` text
Combine signals
      ↓
Learn a ranking
      ↓
Explain the ranking
      ↓
Produce investigation order
```

------------------------------------------------------------------------

## Project Team

**Under the guidance of:**

Dr. B. Bhaskara Rao, M.Tech., Ph.D.\
Associate Professor & HOD\
Department of CSE (Data Science)

**Prepared by:**

-   M. Uday Kumar Reddy --- 23091A32H2
-   S. Vasavi --- 23091A32H7
-   S. Vaseem Basha --- 23091A32H8

**Program:** IV B.Tech --- CSE (Data Science)\
**Academic Year:** 2026--2027

------------------------------------------------------------------------

## Future Extensions

The project presentation identifies the following as possible downstream
or extended capabilities:

-   Automated repository scanning
-   Continuous security scanning
-   GitHub integrations
-   Jira integrations
-   Discord integrations
-   CI/CD integrations
-   Additional automated security actions

These capabilities are extensions of the MVP rather than its core
implementation focus.

------------------------------------------------------------------------

## Disclaimer

SBOM Sentinel is a research and final-year project concept focused on
vulnerability prioritization.

The priority produced by the system should support security
investigation and human decision-making. It should not be treated as an
automatic replacement for security engineering judgment, especially when
dependency reachability or other application context is uncertain.

------------------------------------------------------------------------

## Project Summary

``` text
SBOM
  ↓
Security Intelligence
  ↓
Dependency & Reachability Context
  ↓
Multi-Signal ML Ranking
  ↓
Explainable Priority
  ↓
Investigation Queue
  ↓
Clear Next Action
```

**SBOM Sentinel --- Know what to fix first.**
