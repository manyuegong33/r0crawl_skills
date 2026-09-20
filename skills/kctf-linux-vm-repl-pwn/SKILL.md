---
name: kctf-linux-vm-repl-pwn
description: Solve KCTF Linux ELF64 REPL and VM pwn chains with PIE, canary, NX, and Full RELRO. Use when the challenge is a prompt-driven interpreter or custom VM with a linked libc.
---

# KCTF Linux VM REPL Pwn

## Workflow

1. Record ELF type, mitigations, linked libc, and the prompt/command contract.
2. Recover the dispatch path before attempting an exploit.
3. Separate parser, interpreter, and state machine logic.
4. Build a reproducible local run with the shipped libc.
5. Verify the same input on the raw binary and the rebuilt exploit chain.

## Use this pattern

- ELF64 with PIE, canary, NX, Full RELRO
- prompt-driven interpreter or VM
- no direct numeric echo
- libc-linked challenge binary

## Reference

- `references/pattern.md`
