---
name: kctf-jni-even-odd-xof
description: Solve KCTF JNI validators that deinterleave fixed-length input into even/odd shares, combine ARX/XOF constraints, sparse Boolean gates, S-box state machines, and TEA-derived schedules.
---

# KCTF 第六题 酉时·书院迷局

## Workflow

1. Confirm Java hex input normalization (100 hex chars→50 bytes) and JNI entry; deinterleave with `vld2` into even25/odd25.
2. Recover APK `.kctfguard` key derivation (CRC + ELF section metadata), then simplify native opaque helpers (XOR/add/sub, inverse MixColumns, low-byte extraction, `mix32`).
3. Solve odd channel first: reverse four-round 64-bit ARX/XOF; use output bytes and seed branches to derive initial state words. Encode the 46-bit sparse Boolean gate as local CNF by enumerating each output bit’s 2–5 input support; split cubes and SAT-solve.
4. Apply cheap padding check by inverting XOF and requiring recovered bytes `25:32 == 5a…5a`; this isolates unique odd25 and seed.
5. Invert even channel’s byte permutation/state chain. Recover S-box seed from self-check bytes and enumerate small config fields.
6. Brute-force 32-bit TEA schedule seed (LCG `1664525*x+1013904223`, 16 rounds) using first known-answer test, then verify two additional KATs. Fold selector to derive final seed.
7. Reverse even share, verify expected 16-byte block equals odd-generated block, interleave even/odd bytes, hex-encode flag.

## Constants from writeup

Native key: `870573e5f5c63d52862dbd05ab3d9494`; hidden target first 16 bytes `9f73be24a1dd6c96b90723bba7cdfdc9`. Correct branch `seed=d7`; odd share `7ae31b94d256f80c41b7298e63a5df104bc8723d960fe458ad`. Even share `a77a78ff6a94367d1b4eb43faa8de2b30400bd533de8553443`. Final interleaved flag hex: `a77a7ae3781bff946ad2945636f87d0c1b414eb7b4293f8eaa638da5e2dfb310044b00c8bd72533d3d96e80f55e4345843ad`.

## Validation

Replay original JNI function (or a faithful Python model) and require all initial checks, S-box checks, 3 TEA KATs, sparse gate, and final block comparison to pass.
