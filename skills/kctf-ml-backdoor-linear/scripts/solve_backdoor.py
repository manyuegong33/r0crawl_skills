#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import struct
from pathlib import Path

import numpy as np


CHARSET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def load_safetensors(path: Path):
    raw = path.read_bytes()
    (hlen,) = struct.unpack("<Q", raw[:8])
    header = json.loads(raw[8 : 8 + hlen])
    base = 8 + hlen
    out = {}
    for name, meta in header.items():
        if name == "__metadata__":
            continue
        o0, o1 = meta["data_offsets"]
        arr = np.frombuffer(raw[base + o0 : base + o1], dtype="<f4").copy()
        out[name] = arr.reshape(meta["shape"])
    return out


def decode_x(x: np.ndarray) -> str:
    chars = []
    for v in x.astype(int).tolist():
        if not (0 <= v < len(CHARSET)):
            raise ValueError(f"token out of range: {v}")
        chars.append(CHARSET[v])
    return "".join(chars)


def forward(x: np.ndarray, dense_w, dense_b, head_w, head_b):
    h = np.maximum(dense_w @ x + dense_b, 0.0)
    return head_w @ h + head_b


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("model", help="path to model.safetensors")
    args = ap.parse_args()

    tensors = load_safetensors(Path(args.model))
    W = tensors["dense.weight"]
    b = tensors["dense.bias"]
    HW = tensors["lm_head.weight"]
    HB = tensors["lm_head.bias"]

    # KCTF-style small model: rows 1..20 are exact zeroing constraints.
    A = W[1:21]
    c = b[1:21]
    x, *_ = np.linalg.lstsq(A, -c, rcond=None)
    xr = np.rint(x).astype(int)

    if np.linalg.norm(A @ xr + c) > 1e-6:
        raise SystemExit("rounding failed: constraint residual too large")

    prompt = decode_x(xr)
    logits = forward(xr.astype(np.float32), W, b, HW, HB)
    pred = int(np.argmax(logits))

    print("prompt:", prompt)
    print("argmax:", pred)
    print("success:", pred == 62)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
