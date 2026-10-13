# Contributing

SBOM Sentinel uses a small-task, review-first workflow. Every team member should work in short branches, open focused pull requests, and keep the linked issue updated.

## Daily Work Rule

Each member should complete one small task per day and open one focused pull request when code or documentation changes.

Good daily tasks include:

- Add a parser skeleton.
- Add one test fixture.
- Implement one OSV client method.
- Add one ranking factor.
- Update one documentation page.

Avoid large unreviewed code drops.

## Beginner Git Workflow

Use this exact flow when starting work.

## Feature Branches And Bugfix Branches

Use a feature branch when adding new behavior:

```bash
git checkout main
git pull origin main
git checkout -b feature/issue-2-cyclonedx-parser
```

Use a bugfix branch when fixing broken behavior:

```bash
git checkout main
git pull origin main
git checkout -b bugfix/issue-12-osv-timeout
```

Do not mix feature work and bug fixes in the same branch unless the
issue explicitly asks for both.

### Start from latest main

```bash
git checkout main
git pull origin main
```

### Create your task branch

```bash
git checkout -b feature/issue-2-cyclonedx-parser
```

Replace the branch name with your issue number and task name.

### Check your changes before commit

```bash
git status
git diff
```

### Run checks

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
PYTHONPATH=src python3 -m sbom_sentinel --help
```

### Commit and push

```bash
git add <files-you-changed>
git commit -m "Short description of your task"
git push -u origin feature/issue-2-cyclonedx-parser
```

### Keep your branch updated

If someone else merged work before your PR is merged:

```bash
git checkout main
git pull origin main
git checkout feature/issue-2-cyclonedx-parser
git merge main
```

If conflicts appear, ask for help before changing files randomly.

### Merge vs rebase

For beginners, prefer merging latest `main` into your branch:

```bash
git checkout main
git pull origin main
git checkout feature/issue-2-cyclonedx-parser
git merge main
```

Rebase is cleaner but easier to misuse:

```bash
git checkout main
git pull origin main
git checkout feature/issue-2-cyclonedx-parser
git rebase main
```

Use rebase only on your own branch. If a rebase conflict becomes
confusing, cancel it:

```bash
git rebase --abort
```

After a successful rebase, update your GitHub branch with:

```bash
git push --force-with-lease
```

Never force-push to `main`.

### Conflict resolution basics

Conflict markers look like this:

```text
<your branch version marker>
your branch version
<separator marker>
main branch version
<main branch version marker>
```

Resolve conflicts by keeping the correct final code and deleting the
marker lines.

For merge conflicts:

```bash
git status
# edit conflicted files
PYTHONPATH=src python3 -m unittest discover -s tests
git add <fixed-files>
git commit
git push
```

For rebase conflicts:

```bash
git status
# edit conflicted files
PYTHONPATH=src python3 -m unittest discover -s tests
git add <fixed-files>
git rebase --continue
git push --force-with-lease
```

If you are unsure which version is correct, stop and ask for review.

## Command Cheat Sheet

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

## Branch Naming

Use the issue number and a short task name:

```text
issue-6-project-skeleton
issue-2-cyclonedx-parser
issue-4-osv-cache
issue-3-baseline-ranking
issue-5-demo-command
```

## Pull Request Rules

Every PR must include:

- What changed.
- Why the change matters.
- How to test it.
- Expected output.
- Known limitations.
- Linked issue.

## Review Process

1. Pick one issue subtask.
2. Create a branch from `main`.
3. Implement only that subtask.
4. Add or update tests.
5. Run the test or demo command locally.
6. Open a PR using the template.
7. Request review.
8. Fix review comments.
9. Merge only after review approval.

## Code Quality Expectations

- Keep module boundaries clear.
- Preserve unknown evidence instead of treating missing data as safe.
- Prefer readable code over clever code.
- Keep sample outputs reproducible.
- Do not include unrelated formatting changes.
