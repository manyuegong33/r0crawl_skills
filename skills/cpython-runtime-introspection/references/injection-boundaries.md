# CPython Injection Boundaries

## C API sequence

Use the bundled runtime exports when possible:

1. Resolve `PyGILState_Ensure`.
2. Resolve `PyRun_SimpleStringFlags` or `PyRun_SimpleString`.
3. Resolve `PyGILState_Release`.
4. Execute `exec(open(r'payload.py', encoding='utf-8').read(), {})`.

Install the payload in the child process after `pythonXY.dll` loads and before the target input call.

## Frame probe strategy

Monkey-patch `builtins.input`. The wrapper runs in the caller's Python thread and can reach the verifier frame through `sys._getframe(1)`. Dump frames first, then call the original input or return a controlled test value.

## Version notes

- Marshal and bytecode are version-specific.
- Python 3.11+ uses adaptive bytecode and changed frame internals; prefer public Python attributes over native structure offsets.
- Exported evaluator names can differ by version and build. Python-level injection is more stable.

