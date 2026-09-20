---
name: kctf-antiai-state-machine
description: Solve KCTF AntiAI and anti-analysis crackmes with fixed-length inputs, hidden state buffers, debugger checks, and staged integer recovery. Use for Windows executables that gate on a small state machine, checksum, or integrity path rather than a flat serial.
---

# KCTF AntiAI State Machine

## Workflow

1. Record file type, bitness, entrypoint, imports, and the exact prompt/output strings.
2. Check whether the binary hides validation in a state buffer, a helper section, or a debugger gate.
3. Validate on:
   - empty input
   - wrong-length input
   - one representative sample
4. Recover the state transition before attempting brute force.
5. Keep the raw input, state dump, and recovered output separate.

## Use this pattern

- fixed-length input
- `IsDebuggerPresent` / integrity / anti-analysis checks
- small hidden state vector
- final `yes/no` or `success/fail` gate

## Reference

- `references/pattern.md`
