#!/usr/bin/env python3
"""Suggest modules from a plain-English task description."""
import argparse
rules={"apk":["android-static-analysis","android-unpacking-and-dumping","dex-memory-dump"],"frida":["frida-dynamic-analysis","frida-anti-detection-analysis"],"javascript":["js-hook-engineering","js-deobfuscation","browser-runtime-tracing"],"sign":["web-signature-analysis","crypto-dataflow-analysis"],"pcap":["protocol-reconstruction","websocket-grpc-analysis"],"malware":["malware-triage","malware-dynamic-analysis"],"dump":["memdumper-artifact-validation","dump-fix-rebuild"],"syscall":["syscall-filter-evidence","direct-syscall-analysis"]}
ap=argparse.ArgumentParser(); ap.add_argument("query",nargs="+"); args=ap.parse_args(); q=" ".join(args.query).lower(); out=[]
for key,mods in rules.items():
    if key in q: out += mods
print("\n".join(dict.fromkeys(out)) or "triage-and-route\nevidence-collection")
