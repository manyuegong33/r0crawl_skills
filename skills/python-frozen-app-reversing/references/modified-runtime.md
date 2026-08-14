# Modified Runtime Decision Tree

## Entry script does not explain behavior

1. Confirm the behavior belongs to the child process, not the one-file parent.
2. Capture one output or input stack.
3. If the stack enters Python, scan `pythonXY.dll`, `libpython`, runtime hooks, and frozen modules.
4. Search identifiers across all binaries, not only `.pyc` files.
5. Compare the bundled runtime with the matching stock build.
6. Deserialize candidate marshal blobs with the exact runtime version.

## Useful evidence

- PyInstaller cookie and TOC offsets
- extracted Python version
- marker offsets in runtime libraries
- frozen-module `co_filename` and `co_name`
- appended `co_names` and `co_consts`
- input frame locals and code object

## Failure patterns

- Searching only the outer PE misses modified runtime data.
- Trusting `main.pyc` misses pre-main frozen-module execution.
- Disassembling CPython internals before proving the runtime boundary wastes time.
- Loading marshal with the wrong Python version produces misleading errors.

