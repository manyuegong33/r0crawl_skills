#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


ENCODINGS = ("utf-8", "utf-16le", "utf-16be", "gbk")
MEI_MAGIC = b"MEI\x0c\x0b\x0a\x0b\x0e"


def find_all(data, needle):
    start = 0
    while True:
        offset = data.find(needle, start)
        if offset < 0:
            return
        yield offset
        start = offset + 1


def scan_file(path, markers):
    try:
        data = path.read_bytes()
    except OSError:
        return []
    results = []
    for marker in markers:
        seen = set()
        for encoding in ENCODINGS:
            try:
                needle = marker.encode(encoding)
            except UnicodeEncodeError:
                continue
            for offset in find_all(data, needle):
                key = (offset, needle)
                if key in seen:
                    continue
                seen.add(key)
                results.append({"marker": marker, "encoding": encoding, "offset": offset})
    for offset in find_all(data, MEI_MAGIC):
        results.append({"marker": "PyInstaller MEI cookie", "encoding": "binary", "offset": offset})
    return results


def main():
    parser = argparse.ArgumentParser(description="Scan every frozen-app artifact for semantic markers.")
    parser.add_argument("root", type=Path)
    parser.add_argument("markers", nargs="+")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    output = []
    paths = [args.root] if args.root.is_file() else sorted(path for path in args.root.rglob("*") if path.is_file())
    for path in paths:
        hits = scan_file(path, args.markers)
        if hits:
            output.append({"path": str(path), "size": path.stat().st_size, "hits": hits})
    if args.json:
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return
    for item in output:
        print(item["path"])
        for hit in item["hits"]:
            print(f"  0x{hit['offset']:x} {hit['encoding']}: {hit['marker']}")


if __name__ == "__main__":
    main()

