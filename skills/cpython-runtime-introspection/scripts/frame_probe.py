import builtins
import dis
import json
import marshal
import os
import sys
from pathlib import Path


OUTPUT_DIR = Path(os.environ.get("CPYTHON_PROBE_DIR", "cpython_probe"))
CONTROLLED_INPUT = os.environ.get("CPYTHON_PROBE_INPUT")
ORIGINAL_INPUT = builtins.input
CAPTURE_INDEX = 0


def safe_repr(value, limit=2000):
    try:
        result = repr(value)
    except Exception as error:
        result = f"<repr failed: {error!r}>"
    return result[:limit]


def capture_frames(frame):
    global CAPTURE_INDEX
    CAPTURE_INDEX += 1
    capture_dir = OUTPUT_DIR / f"capture_{CAPTURE_INDEX:03d}"
    capture_dir.mkdir(parents=True, exist_ok=True)
    summary = []
    depth = 0
    while frame is not None:
        code = frame.f_code
        prefix = capture_dir / f"frame_{depth:02d}"
        prefix.with_suffix(".marshal").write_bytes(marshal.dumps(code))
        with prefix.with_suffix(".dis.txt").open("w", encoding="utf-8") as output:
            dis.dis(code, file=output)
        summary.append({
            "depth": depth,
            "filename": code.co_filename,
            "name": code.co_name,
            "line": frame.f_lineno,
            "names": list(code.co_names),
            "consts": [safe_repr(value) for value in code.co_consts],
            "locals": {name: safe_repr(value) for name, value in frame.f_locals.items()},
            "globals": sorted(frame.f_globals),
        })
        frame = frame.f_back
        depth += 1
    (capture_dir / "frames.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")


def probing_input(prompt=""):
    capture_frames(sys._getframe(1))
    if CONTROLLED_INPUT is not None:
        return CONTROLLED_INPUT
    return ORIGINAL_INPUT(prompt)


builtins.input = probing_input

