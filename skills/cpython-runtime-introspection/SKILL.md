---
name: cpython-runtime-introspection
description: Inspect embedded or packaged CPython processes at runtime by tracing child processes, acquiring the GIL, injecting Python, replacing builtins.input, walking frame.f_back, exporting frame code objects, locals, globals, and disassembly, and hooking PyEval or marshal boundaries. Use when static extraction misses executed logic or when Python behavior is visible only in memory.
---

# CPython Runtime Introspection

## Prove the process and runtime

1. Handle one-file parent and child processes separately.
2. Record module bases and the exact Python version.
3. Capture an input or output stack and confirm it enters CPython.
4. Match injector and target architecture.

## Prefer semantic injection

Inject Python-level code instead of reverse engineering the evaluator first:

1. Acquire the GIL with `PyGILState_Ensure`.
2. Execute a small payload with `PyRun_SimpleStringFlags` or a compatible API.
3. Release the GIL.
4. Install `scripts/frame_probe.py` before the interesting `input()` or verifier executes.

See `references/injection-boundaries.md` for native API sequencing.

## Walk caller frames

At a semantic choke point such as `builtins.input`:

- start at `sys._getframe(1)`
- walk `frame.f_back`
- record `co_filename`, `co_name`, `f_lineno`, `co_names`, and `co_consts`
- safely serialize local/global values
- write `marshal.dumps(frame.f_code)` using the target runtime
- disassemble in the same Python version

Do not rely on native stacks alone; they usually stop at generic evaluator functions.

## Fallback boundaries

If Python-level injection is unavailable, instrument in this order:

1. `PyEval_EvalCode` or version-specific evaluator boundary
2. `PyMarshal_ReadObjectFromString`
3. `PyImport_ExecCodeModule*`
4. input or comparison builtins

## Quality gates

- Preserve the original input function and restore it after capture.
- Limit repr length and handle repr exceptions.
- Export code objects before modifying locals.
- Confirm dumped marshal objects load under the exact Python version.
- Validate the recovered verifier independently against live behavior.

