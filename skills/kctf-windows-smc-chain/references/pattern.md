# KCTF Windows SMC Chain Pattern

## Facts from KCTF 8

- File: `kctf2026_CrackMe08.exe`
- PE64 x86-64
- Entry: `0x12c0`
- Sections include `.text`, `.rdata`, `.data`, and `.tgt`
- The entry code mutates the input buffer with `xor 0x5a`

## What to do

1. Find the runtime-decrypted target region.
2. Trace anti-debug / anti-breakpoint checks.
3. Dump or emulate the clean checker.
4. Solve the algebraic gate on the clean code.
5. Verify against the original sample.

## Signals

- runtime patching
- staged jump chains
- hidden target section
- arithmetic verification after decryption
