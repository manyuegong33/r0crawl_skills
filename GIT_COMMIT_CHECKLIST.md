# Git Commit Checklist

- [ ] `git status` contains only intended files.
- [ ] No APK, DEX, SO, PCAP, HAR, dump, credential, or private capture is staged.
- [ ] `python scripts/check_utf8.py .` passes.
- [ ] `python scripts/index_skills.py` has been run.
- [ ] Root skill validation passes.
- [ ] Every module frontmatter validation passes.
- [ ] `python -m compileall scripts` passes.
- [ ] README links point to existing files.
- [ ] Generated indexes are up to date.
