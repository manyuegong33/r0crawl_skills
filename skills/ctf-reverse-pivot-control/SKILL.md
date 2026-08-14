---
name: ctf-reverse-pivot-control
description: Evidence-driven pivot control for CTF reverse engineering. Use when analysis is stuck, the apparent entry point is a decoy, static and runtime observations disagree, a packed or embedded-language target is being treated as pure native code, or repeated experiments are not reducing uncertainty.
---

# CTF Reverse Pivot Control

## Build the substrate ladder

Classify every observation at the correct layer before following xrefs:

1. Container or packer
2. Loader or bootloader
3. Language runtime
4. Application logic
5. Verifier and success output

Do not descend into a lower layer merely because it is easy to disassemble. First prove that the layer contains the behavior under investigation.

## Maintain competing hypotheses

For each hypothesis, record:

- predicted observation
- smallest discriminating experiment
- result
- confidence
- next pivot condition

Keep at least two plausible hypotheses until one experiment distinguishes them.

## Enforce pivot gates

- If runtime stacks stay inside a language runtime, inspect frames, bytecode, modules, and embedded data before native internals.
- If an extracted entry script is inert but behavior occurs before it, inspect runtime hooks, frozen modules, modified runtime libraries, and loader patches.
- If strings are absent from the outer executable, scan every extracted binary and runtime component before assuming runtime decryption.
- If redirected input changes repetition count, test EOF and console semantics before inferring constructors, callbacks, or threads.
- If three consecutive commands only confirm the same layer, stop and run a cross-layer experiment.

## Time-box rabbit holes

After 15 minutes or five tool calls without a new address, object, constant, or falsified hypothesis:

1. State what remains unknown.
2. Identify the next higher semantic boundary.
3. Instrument that boundary.
4. Resume static work only with a runtime address or artifact.

## Quality gates

- Separate fact, inference, and speculation.
- Require two independent signals for the decisive call chain.
- Prefer one experiment that can falsify a theory over ten broad searches.
- Never call an entry point, section name, or decompiler label “core logic” without behavioral evidence.

## Routing

- Frozen Python executable: use `python-frozen-app-reversing`.
- Live CPython behavior: use `cpython-runtime-introspection`.
- Key or flag derivation: use `ctf-key-recovery`.
- Final parity check: use `reconstruction-and-parity`.

