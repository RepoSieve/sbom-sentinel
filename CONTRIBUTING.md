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
