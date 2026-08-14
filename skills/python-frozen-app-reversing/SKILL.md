---
name: python-frozen-app-reversing
description: Recover logic from PyInstaller, cx_Freeze, py2exe, Nuitka, and other frozen Python applications, including modified bootloaders, decoy entry scripts, patched frozen standard-library modules, embedded marshal code objects, and logic hidden inside pythonXY.dll or libpython. Use for packaged Python executables, MEI overlays, PYZ archives, suspicious .pyc files, or runtime behavior missing from extracted scripts.
---

# Python Frozen App Reversing

## Preserve the environment

Record hashes, architecture, packer evidence, Python version, and tool versions. Use a dedicated virtual environment for extractors; do not downgrade shared dependencies.

## Inventory every layer

1. Identify the container using imports, strings, overlay magic, and process behavior.
2. List the archive TOC before extraction.
3. Extract the archive and record every script, runtime hook, PYZ entry, native extension, and Python runtime library.
4. Disassemble entry scripts with a Python-version-compatible tool.
5. Run `scripts/scan_frozen_artifacts.py` across the entire extraction tree using runtime output and function identifiers as markers.

## Treat an inert entry script as evidence

If the extracted entry script exits or lacks observed behavior, inspect in this order:

1. PyInstaller runtime hooks and bootstrap scripts
2. Frozen modules embedded in `pythonXY.dll` or `libpython`
3. Modified standard-library modules
4. Custom bootloader calls before script execution
5. Runtime-created code objects

Do not conclude that extraction failed solely because `main.pyc` is a decoy.

## Locate modified frozen modules

- Search all extracted binaries for unique runtime text, function names, exception text, and nearby Python identifiers.
- Compare the bundled runtime library with the same upstream Python version when available.
- Inspect `_PyImport_Frozen*` tables, marshal tags, code-object names, filenames such as `<frozen os>`, and clusters of Python names/constants.
- Use the exact bundled Python version to deserialize marshal data; marshal is version-specific.

See `references/modified-runtime.md` for the decision tree.

## Cross the runtime boundary early

Prove whether output and input stacks enter `pythonXY.dll` or `libpython`. If they do, stop treating CRT or Win32 I/O as the verifier and route to `cpython-runtime-introspection`.

## Deliverables

- container and archive inventory
- real execution location: archive entry, frozen module, runtime library, or loader
- recovered code object or equivalent verifier
- offsets and hashes for every derived artifact
- live validation of the recovered answer

