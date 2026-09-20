# KCTF corpus notes

## Verified replay: KCTF 2026 第五题

- Artifact: `cm.exe`
- SHA1: `D1C8124C5964AF1531C6E311328854A05CA40BCA`
- Article condition: input `Key`, expect `verify success.`
- Known-good key:
  `323C47184B0D3C44254B445842552F365C362C1144424B0D3C4416433B0DD6B12A0D3D95FA65B5E0ADE5E11B`
- Replay:
  `echo 323C47184B0D3C44254B445842552F365C362C1144424B0D3C4416433B0DD6B12A0D3D95FA65B5E0ADE5E11B | cm.exe`
- Observed:
  `verify success.`

## Pattern: KCTF 2026 第三题

- Artifact: `AntiAi.exe`
- Article signals: Windows, AntiAI, fixed-length input, 32-byte internal state, debug / integrity checks.
- Use this as the template for integer-model or state-transition puzzles.

## Pattern: KCTF 第十题

- Artifact: `pwn`
- Article signals: ELF64 x86-64, PIE, Full RELRO, NX, canary, custom REPL interpreter, no direct value echo.
- Use this as the template for static + dynamic correlation in Linux pwn / VM tasks.
