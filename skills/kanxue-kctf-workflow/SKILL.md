---
name: kanxue-kctf-workflow
description: |
  Fast triage and solving workflow for 看雪 KCTF / CTF对抗 writeups,题面, archives, and challenge binaries. Use when analyzing KCTF HTML articles, RAR/ZIP attachments, Windows key checkers, Linux pwn/ELF REPLs, or anti-analysis / VM puzzles, and when you need a reproducible local replay or solver.
---

# Kanxue Kctf Workflow

## Purpose

Use this skill as a KCTF overlay on top of generic reversing skills. The goal is to
turn a看雪题目 folder into: artifact inventory, challenge type, baseline run, verified
success condition, and a reusable replay command.

## Workflow

1. Read the article title, rule number, attachment names, hash, and success string.
2. Split artifacts into: article HTML, attachment archive, runnable binary, solver, and
   extracted support files.
3. Extract the smallest runnable sample first.
4. Run a baseline:
   - Windows checker: no args, bad input, then the writeup's known-good key.
   - Linux ELF / pwn: file, mitigation check, prompt capture, then local VM or Linux host.
   - AntiAI / VM puzzle: confirm fixed input length, state size, and the first immutable
     constants before solving.
5. Record the exact command, input, output, and file hash that prove the result.
6. Save the replay command and solver together.

## KCTF patterns

### Windows key / serial checker

- Look for `Key`, `Enter your key`, `verify success.`, `verify failed.`, or a fixed-length
  hex input.
- Treat checksum, lookup table, RSA, and big-int stages as separate gates.
- Prefer a direct replay before building a full solver.

### Linux pwn / REPL / VM

- Record architecture, mitigation, prompt, and I/O contract.
- Separate parser, dispatcher, leak, and overwrite stages.
- If the binary is ELF64 with PIE / RELRO / canary / NX, validate in Linux or VM rather than
  assuming Windows execution.

### AntiAI / anti-analysis / arithmetic VM

- Derive input length, state size, and debug / integrity checks first.
- Build an integer model from the article and confirm it on one local sample.
- Do not brute force until the fixed constraints are captured.

## Reuse

- Read `references/corpus-map.md` for routing by challenge family.
- Read `references/corpus-notes.md` for the validated replay example and local notes.
- Run `scripts/kctf_scan.py <folder>` to inventory a new KCTF bundle quickly.
