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

### Start from latest main

```bash
git checkout main
git pull origin main
```

### Create your task branch

```bash
git checkout -b issue-2-cyclonedx-parser
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
git push -u origin issue-2-cyclonedx-parser
```

### Keep your branch updated

If someone else merged work before your PR is merged:

```bash
git checkout main
git pull origin main
git checkout issue-2-cyclonedx-parser
git merge main
```

If conflicts appear, ask for help before changing files randomly.

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
