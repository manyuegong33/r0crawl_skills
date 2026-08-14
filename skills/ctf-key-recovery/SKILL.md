---
name: ctf-key-recovery
description: Reconstruct CTF key, serial, and flag verifiers using known plaintext, repeating XOR, encoded constants, bytecode replacement, hash constraints, SMT, and bounded brute force. Use when a reverse challenge requests a key or serial and the verifier or encrypted target bytes can be recovered statically or dynamically.
---

# CTF Key Recovery

## Reconstruct the exact verifier

Write down input normalization, encoding, required length, transforms, comparison bytes, success condition, and retry behavior. Separate presentation decoding from authentication logic; similar XOR loops may use different keys.

## Use the cheapest invertible relation

For repeating XOR with period `p`:

```text
cipher[i] = plain[i] XOR key[i mod p]
key[i mod p] = cipher[i] XOR plain[i]
```

Recover every key position from known plaintext and reject inconsistent positions. Run `scripts/recover_repeating_xor.py` for a reproducible derivation.

Escalate only as needed:

1. algebraic inversion
2. known-plaintext constraints
3. printable/format constraints
4. SMT solver
5. bounded brute force

See `references/verifier-checklist.md` before declaring success.

## Validate twice

1. Re-encrypt or replay the recovered key against the reconstructed verifier.
2. Run the original challenge through its real input path and observe the success branch.

Record the raw key separately from any platform wrapper such as `flag{...}`.

## Quality gates

- Do not treat a plaintext-looking substring as the answer without verifier parity.
- Do not mix display constants with comparison constants.
- Preserve byte order, signedness, encoding, and terminators.
- Test wrong length, one-byte mutation, and the recovered key.

