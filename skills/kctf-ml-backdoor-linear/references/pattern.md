# KCTF ML backdoor pattern

## Recognition

Typical signs:
- raw `safetensors`
- small `dense -> ReLU -> lm_head`
- token ids are cast to float directly
- one output row is normal, one row is a success backdoor, one row is fail

## Solve order

1. Parse tensors from the raw file.
2. Identify the hidden layer rows that must be zeroed by ReLU.
3. Solve the linear system from those rows.
4. Round only when the residual is zero or machine-zero.
5. Decode with the challenge charset.
6. Replay the forward pass and confirm `argmax` hits the success row.

## Validation

Do not rely on the model wrapper alone. Verify:
- the same candidate reproduces the target label in a manual forward pass
- the decoded string only uses in-vocabulary characters
- the candidate length obeys the tokenizer limit
