---
name: kctf-algebraic-crackme-chain
description: Solve KCTF Windows crackmes with layered codecs, 32/64-bit shell thunks, .data-resident code, and final algebraic or polynomial checks. Use when a PE/EXE has name+serial prompts, huge staged serials, lookup-table mixers, or root-finding gates.
---

# Kctf Algebraic Crackme Chain

## Use this skill

Use this for KCTF-style Windows crackmes where the visible checker is only a shell and the real logic is split across:
- a 32/64-bit loader or thunk
- codec / normalization layers
- lookup-table or mixer layers
- a final algebraic gate

## Workflow

1. Inventory the PE, entrypoint, sections, imports, prompt strings, and output strings.
2. Separate shell code from real logic. If code lives in `.data`, treat it as executable.
3. Identify each layer:
   - input normalization / expansion
   - mixer / lookup / rotate / XOR layer
   - algebraic or polynomial gate
   - final success branch
4. Validate each layer on:
   - the public sample
   - an obviously wrong input
   - the target name
5. Keep three artifacts distinct:
   - raw text input
   - normalized numeric body
   - final row/roots/state data
6. Save the replay command plus the smallest dump needed to reproduce the result.

## KCTF 4-style pattern

- `DayDayUp`: first codec / normalizer.
- `MengXin`: mixer / inverse stage.
- `check2`: format gate.
- `GoodGoodStudy`: final algebraic gate over the selected row/state set.

## Practical checks

- Do not trust the readme alone; confirm actual runtime length and branch behavior.
- Do not assume a sample serial is “simple” just because it is public; it may only validate after the hidden layers finish.
- Snapshot the state buffer before the final algebraic gate.
- If the checker is slow, attach and dump the live state instead of waiting for the final UI.

## References

- `references/pattern.md`
