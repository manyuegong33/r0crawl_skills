#!/usr/bin/env python3
import argparse
from pathlib import Path


def parse_bytes(value, is_file, encoding):
    if is_file:
        return Path(value).read_bytes()
    if value.startswith("hex:"):
        return bytes.fromhex(value[4:])
    return value.encode(encoding)


def recover(cipher, plain, period):
    if len(cipher) != len(plain):
        raise ValueError("ciphertext and plaintext lengths differ")
    slots = [None] * period
    for index, (cipher_byte, plain_byte) in enumerate(zip(cipher, plain)):
        value = cipher_byte ^ plain_byte
        slot = index % period
        if slots[slot] is not None and slots[slot] != value:
            raise ValueError(f"inconsistent key byte at slot {slot}")
        slots[slot] = value
    if any(value is None for value in slots):
        raise ValueError("known plaintext does not cover every key position")
    return bytes(slots)


def main():
    parser = argparse.ArgumentParser(description="Recover a repeating-XOR key from known plaintext.")
    parser.add_argument("cipher")
    parser.add_argument("plain")
    parser.add_argument("period", type=int)
    parser.add_argument("--cipher-file", action="store_true")
    parser.add_argument("--plain-file", action="store_true")
    parser.add_argument("--encoding", default="utf-8")
    args = parser.parse_args()
    cipher = parse_bytes(args.cipher, args.cipher_file, args.encoding)
    plain = parse_bytes(args.plain, args.plain_file, args.encoding)
    key = recover(cipher, plain, args.period)
    print("hex:", key.hex())
    try:
        print("text:", key.decode(args.encoding))
    except UnicodeDecodeError:
        pass


if __name__ == "__main__":
    main()

