# KCTF Algebraic Crackme Chain Pattern

## Core shape

This pattern shows up in Windows crackmes where:
- the EXE is only a loader / shell
- real logic sits in `.data` or other non-text regions
- the user-facing checker is split into multiple named stages
- the final gate is algebraic, polynomial, or row-selection based

## 4题 reconstruction notes

- Visible prompts: `Name` + `Serial`
- Static shell: 32-bit loader with a 64-bit / mixed-code stage chain
- Stage names seen in writeup / reverse notes:
  - `DayDayUp`
  - `MengXinQiuFangGuo`
  - `check2`
  - `GoodGoodStudy`
- Public sample facts:
  - name: `338F493766CFC94B`
  - serial length: `9226`
  - normalized body: `6912` bytes (`432 x 16`)
  - final math layer: `100` rows / `1000` integer roots
- The final gate works on a normalized body plus a per-name state set.
- Snapshot the live `100 x uint32` state buffer before the final polynomial pass.
- Layer sizes from the writeup:
  - `6912` input bytes -> `9216` body bytes
  - `100` row states
  - `100` polynomials, each with `11` coefficients
  - `1000` total integer roots

## Recommended reverse order

1. Confirm prompt/response behavior on the public sample and on bad input.
2. Find the real checker entry in the shell chain.
3. Dump or emulate the code region if it lives in `.data`.
4. Extract the normalized body before the last gate.
5. Recover the per-name state set.
6. Solve the algebraic gate on the recovered state set.
7. Re-run the original sample to confirm parity.

## Validation rules

- Keep raw input, normalized body, and final serial separate.
- Compare wrong input vs sample vs target.
- Record the exact branch or buffer where the first divergence appears.
