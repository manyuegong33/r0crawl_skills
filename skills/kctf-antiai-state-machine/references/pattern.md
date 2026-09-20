# KCTF AntiAI State Machine Pattern

## Facts from KCTF 3

- File: `AntiAi.exe`
- PE64 x86-64
- Entry: `0x4790`
- Visible prompt: `input flag:`
- Import clue: `IsDebuggerPresent`
- A small hidden state exists in the binary (32-byte class in the corpus notes).

## What to do

1. Verify the prompt on empty and wrong input.
2. Identify the anti-debug / integrity gate.
3. Recover the state buffer and transition rule.
4. Solve the state recovery before brute forcing.
5. Replay the original binary with the recovered candidate.

## Signals

- fixed-length or bounded input
- small helper section / custom state storage
- debugger check
- yes/no style result
