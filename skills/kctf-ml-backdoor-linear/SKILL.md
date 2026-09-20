---
name: kctf-ml-backdoor-linear
description: Solve KCTF model backdoors and small linear/ReLU crackmes from raw weights. Use when the artifact is a safetensors/torch model, token-id-as-feature network, tiny classifier, or a prompt gated by linear inequalities and argmax backdoors.
---

# Kctf Ml Backdoor Linear

## Workflow

1. Parse the raw model file first; do not trust the front-end wrapper.
2. Identify the feature path:
   - token ids used as floats
   - a small dense/ReLU bottleneck
   - a sparse `lm_head` or classifier row that dominates the output
3. Split the problem into:
   - feasibility constraints: hidden units that must be zero
   - objective constraint: the winning logit must beat the fail logit
4. Solve the linear system or linear program on the visible constraints.
5. Round only after checking the residual is effectively zero.
6. Decode the candidate with the challenge charset and verify it against the model.

## Solver pattern

Use the supplied script for small KCTF model crackmes:

```bash
python scripts/solve_backdoor.py path/to/model.safetensors
```

The script:
- reads safetensors directly
- extracts `dense.weight`, `dense.bias`, `lm_head.weight`, `lm_head.bias`
- solves the bottleneck constraints
- prints the candidate prompt
- replays the forward pass to confirm the success token wins

## When to use

- `safetensors`, `model.safetensors`, `state_dict`, `torch`
- 16/21/64-style toy models
- prompt-gated challenge binaries
- tiny classifiers with an obvious `success` / `fail` row

## Notes

- Prefer numpy/scipy over torch for analysis.
- If the solution is integer-valued, use the exact rounded vector only after residual check.
- If multiple candidates survive, verify by manual forward evaluation instead of guessing.
