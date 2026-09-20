---
name: kctf-windows-crackme-chain
description: Solve Windows KCTF crackmes with chained checks, RSA gates, lookup tables, SMC loaders, anti-debug, and Feistel-style math. Use when the artifact is a Windows EXE with Key/verify prompts, layered validation, or self-modifying code.
---

# Kctf Windows Crackme Chain

## Workflow

1. Classify the file: PE/EXE, packed EXE, SMC loader, or plain crackme.
2. Identify the gate chain:
   - serial / checksum / RSA / lookup
   - self-modifying stages
   - anti-debug / anti-breakpoint
   - Feistel / finite-field / polynomial gates
3. Strip the fake path first; recover the real checker or decrypted code.
4. Separate independent gates and solve the cheapest one first.
5. Verify with a replay input before trusting the algebra.
6. Keep the final key/serial reproducible as a command line, not just a pasted value.

## References

- `references/corpus-map.md` for case routing.
- Combine with `kctf-ml-backdoor-linear` when the challenge is a model/backdoor puzzle.
