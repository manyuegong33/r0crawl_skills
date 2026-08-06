# Contributing to r0crawl_skills

## Before opening a pull request

Run:

```powershell
python scripts/check_utf8.py .
python scripts/index_skills.py
python -m compileall scripts
```

Also run the skill validator against the root and every directory under `skills/`.

## Skill requirements

- Keep `SKILL.md` in UTF-8.
- Use lowercase hyphenated names in skill frontmatter.
- Start with a beginner explanation and a concrete success criterion.
- Separate evidence, hypothesis, conclusion, and limitation.
- Do not include credentials, private paths, personal secrets, live captures, or proprietary case material.
- Prefer generic capabilities over vendor-owned prompts or copied repository structure.
- Add a small example or fixture when a workflow is easy to misunderstand.

## Commit style

Use short imperative commits, for example:

```text
feat: add Android dump validation skill
docs: improve beginner routing
fix: normalize UTF-8 metadata
```
