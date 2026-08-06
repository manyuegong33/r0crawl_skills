#!/usr/bin/env python3
"""List request/response fields from a HAR file for signature investigation."""
from pathlib import Path
import argparse,json
ap=argparse.ArgumentParser(); ap.add_argument("har"); args=ap.parse_args()
har=json.loads(Path(args.har).read_text(encoding="utf-8"))
for i,e in enumerate(har.get("log",{}).get("entries",[]),1):
    req=e.get("request",{}); res=e.get("response",{})
    print(f"[{i}] {req.get('method','')} {req.get('url','')}")
    print("  headers:", ", ".join(x.get("name","") for x in req.get("headers",[])))
    print("  query:", ", ".join(x.get("name","") for x in req.get("queryString",[])))
    print("  post:", ", ".join(x.get("name","") for x in req.get("postData",{}).get("params",[])))
    print("  response:", res.get("status"), res.get("mimeType"))
