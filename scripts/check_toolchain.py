#!/usr/bin/env python3
"""Report whether optional reverse-engineering commands are discoverable."""
import argparse,shutil
ap=argparse.ArgumentParser(); ap.add_argument("tools",nargs="*",default=["python","adb","frida","jadx","ghidraRun","ida64","rizin","gdb"]); args=ap.parse_args()
for name in args.tools: print(f"{name}: {shutil.which(name) or 'not-found'}")
