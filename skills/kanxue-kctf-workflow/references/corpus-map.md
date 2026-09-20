# KCTF corpus map

## 3题 - AntiAI / anti-analysis

- Windows executable
- fixed-length hex input
- 32-byte internal state
- debug / integrity checks
- solve style: integer model, inverse state, exact verification

## 4题 - algebraic crackme

- integer-ring factorization / root finding
- fake algorithm layer + final format gate
- solve style: factor polynomials, then rebuild the expected serial

## 5题 - Windows serial checker

- `Key`, `verify success.`
- 88 hex chars / 44 bytes
- XOR + checksum + RSA + lookup chain
- solve style: satisfy each gate, then replay the checker

## 6题 - Android / JNI mixed flow

- Java hex input -> JNI
- `vld2`, split even/odd channels
- SMC, XOF, TEA/LCG, state machine, local/global checks
- solve style: reverse the transform layers separately, then recombine

## 7题 - HexMaze transform

- deterministic byte/nibble transform
- 3-byte blocks -> 6-byte blocks
- length-dependent tail handling
- solve style: infer the block rule from samples, then invert it

## 8题 - Windows SMC crackme

- two-stage self-modifying code
- anti-debug / anti-breakpoint behavior
- Feistel / finite-field algebra
- solve style: dump/decrypt first, then do the math on the clean code

## 9题 - ML backdoor linear model

- tiny `safetensors` model
- token id cast to float
- ReLU bottleneck + sparse lm_head
- solve style: solve visible linear constraints, verify with raw weights

## 10题 - Linux VM / REPL pwn

- ELF64, PIE, canary, NX, Full RELRO
- prompt-driven interpreter
- no direct numeric echo
- solve style: recover the dispatch path, then build a reproducible exploit chain
