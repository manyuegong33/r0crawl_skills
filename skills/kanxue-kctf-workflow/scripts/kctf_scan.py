#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


def sha1(path: Path) -> str:
    h = hashlib.sha1()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def html_meta(path: Path) -> tuple[str, str]:
    data = path.read_text(encoding="utf-8", errors="ignore")
    title = ""
    h1 = ""
    m = re.search(r"<title>(.*?)</title>", data, re.I | re.S)
    if m:
        title = norm(re.sub(r"<.*?>", "", m.group(1)))
    m = re.search(r"<h[12][^>]*>(.*?)</h[12]>", data, re.I | re.S)
    if m:
        h1 = norm(re.sub(r"<.*?>", "", m.group(1)))
    return title, h1


def guess_kind(blob: str, names: list[str]) -> str:
    low = blob.lower()
    joined = " ".join(names).lower()
    if "antiai" in low or "antiai" in joined or "debug" in low and "integrity" in low:
        return "anti-ai / anti-analysis"
    if "verify success" in low or "enter your key" in low or "key" in low and "verify failed" in low:
        return "windows serial / key checker"
    if "elf64" in low or "pwn" in low or "canary" in low or "relro" in low or "nx" in low:
        return "linux pwn / ELF"
    if "vm" in low or "interpreter" in low or "opcode" in low:
        return "VM / interpreter"
    if any(x.endswith(".exe") for x in names):
        return "windows binary"
    return "unknown"


def list_archive(path: Path) -> str:
    seven = shutil.which("7z") or r"C:\\Program Files\\7-Zip\\7z.exe"
    if not Path(seven).exists():
        return "7z not found"
    res = subprocess.run(
        [seven, "l", str(path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return res.stdout.strip() or res.stderr.strip() or "(no output)"


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Scan a KCTF bundle and print a fast triage summary.")
    ap.add_argument("path", nargs="?", default=".", help="KCTF folder to inspect")
    ap.add_argument("--list-archives", action="store_true", help="Show 7z listing for archive files")
    args = ap.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        raise SystemExit(f"not found: {root}")

    case_dirs = [p for p in sorted(root.iterdir()) if p.is_dir() and not p.name.endswith("_files")]
    if not case_dirs:
        case_dirs = [root]

    for case in case_dirs:
        files = [p for p in sorted(case.iterdir()) if p.is_file()]
        htmls = [p for p in files if p.suffix.lower() == ".html" and p.name != "看雪CTF 攻防战.html"]
        archives = [p for p in files if p.suffix.lower() in {".rar", ".zip", ".7z"}]
        runnables = [p for p in files if p.suffix.lower() in {".exe", ".dll", ".so", ".elf", ".bin"} or p.name.lower() == "pwn"]

        print(f"## {case.name}")
        if htmls:
            for h in htmls:
                title, h1 = html_meta(h)
                blob = h.read_text(encoding="utf-8", errors="ignore")
                names = [x.name for x in files]
                kind = guess_kind(blob, names)
                print(f"- html: {h.name}")
                if title:
                    print(f"  - title: {title}")
                if h1:
                    print(f"  - h1: {h1}")
                print(f"  - guess: {kind}")
        if archives:
            for a in archives:
                print(f"- archive: {a.name} ({a.stat().st_size} bytes, sha1 {sha1(a)})")
                if args.list_archives:
                    print("  - 7z:")
                    for line in list_archive(a).splitlines()[:40]:
                        print(f"    {line}")
        if runnables:
            for r in runnables:
                print(f"- file: {r.name} ({r.stat().st_size} bytes, sha1 {sha1(r)})")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
