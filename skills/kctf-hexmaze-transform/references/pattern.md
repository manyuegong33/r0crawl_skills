# KCTF HexMaze Transform Pattern

## Facts from KCTF 7

- Deterministic byte/nibble transform
- 3-byte blocks expand to 6-byte blocks
- Tail handling depends on total length
- Solved from samples, then inverted

## What to do

1. Derive the block mapping.
2. Infer the tail behavior.
3. Rebuild the inverse on a per-block basis.
4. Verify on the original sample.

## Signals

- expansion ratio
- repeated local transform
- no meaningful cryptographic key schedule
