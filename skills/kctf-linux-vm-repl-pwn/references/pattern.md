# KCTF Linux VM REPL Pwn Pattern

## Facts from KCTF 10

- Binary: `pwn`
- Linked libc: `libc-2.27.so`
- ELF64 x86-64
- Mitigations from corpus notes: PIE, canary, NX, Full RELRO
- Prompt-driven interpreter / REPL pattern

## What to do

1. Trace the input loop and command dispatch.
2. Identify the state machine or VM opcodes.
3. Recover the leak / write / pivot primitive.
4. Build a local exploit or solver with the shipped libc.
5. Replay on the raw binary.

## Signals

- C++ streams or custom interpreter
- prompt-based interaction
- no obvious direct flag print
- exploit chain depends on dispatch logic
