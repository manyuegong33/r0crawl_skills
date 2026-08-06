---
name: r0crawl-skills
description: A beginner-friendly full-spectrum reverse-engineering router for Web/JavaScript, Android/iOS, Frida, unpacking, anti-analysis, native binaries, protocols, firmware, malware, games, cloud APIs, CTFs, and reproducible parity testing. Use for reverse, start, unpack, decompile, hook, Frida, bypass detection, APK/SO/DEX/JS/PCAP/WASM/PE/ELF/Mach-O analysis, signature recovery, or a complete investigation from sample to verified result.
---

# r0crawl_skills

[Chinese guide](docs/README.zh-CN.md)

## Beginner-first contract

Before using advanced tools, explain:

1. What the target is: web page, JavaScript, APK, DEX, native library, binary, protocol, firmware, or sample.
2. What action matters: launch, login, search, upload, payment, encryption, validation, or network exchange.
3. What material exists: file, URL, HAR, PCAP, log, screenshot, dump, source, or only a description.
4. What result is wanted: explain behavior, locate an entry, write a hook, unpack a runtime artifact, reproduce a request, or write a report.

If no artifact exists, provide a short collection plan instead of pretending to analyze an invisible target.

## Start protocol

For `start`, `reverse start`, `mixed start`, or `full reverse`:

1. Run `triage-and-route`.
2. Create evidence and a timeline with `evidence-collection`.
3. Split work into static, runtime, loading/unpacking, protocol, and data-flow tracks.
4. Load only modules matched by the routing tables.
5. Use `reconstruction-and-parity` for a minimal reproducible result.
6. Use `systematic-debugging` for every mismatch.
7. Report a beginner summary first, then a technical appendix.

## Core routing

| Signal | Load first |
|---|---|
| APK, AAB, DEX, smali, class loader | `android-static-analysis`, `android-unpacking-and-dumping`, `dex-memory-dump` |
| APK protection, shell, packer, loader, OEP | `apk-protection-analysis`, `native-unpacking`, `packer-and-loader-analysis` |
| SO, PE, ELF, Mach-O, assembly, decompiler | `native-binary-analysis`, `ida-ghidra-workflow`, `symbol-recovery-and-structs` |
| Frida, Java.perform, Interceptor, spawn, attach | `frida-dynamic-analysis`, `frida-stealth-hooking` |
| anti-Frida, maps, ports, threads, Gadget, Root, emulator | `frida-anti-detection-analysis`, `root-emulator-detection`, `anti-analysis-and-integrity` |
| JavaScript hook, fetch, XHR, WebSocket, Proxy, getter/setter | `js-hook-engineering`, `browser-runtime-tracing`, `webcrypto-hooking` |
| Worker, iframe, ServiceWorker, Blob URL, importScripts | `js-worker-hooking`, `browser-runtime-tracing` |
| obfuscation, JSFuck, AAEncode, webpack, flattened control flow | `js-deobfuscation`, `ast-program-analysis`, `ollvm-deobfuscation` |
| JSVMP, VMP, opcode, DSL VM, virtual machine | `jsvmp-vmp-analysis`, `virtualization-protection`, `script-vm-sandbox-analysis` |
| sign, token, cookie, header, encrypted request or response | `web-signature-analysis`, `crypto-dataflow-analysis`, `reconstruction-and-parity` |
| browser environment, canvas, WebGL, webdriver, fingerprint | `browser-env-emulation`, `browser-fingerprint-analysis` |
| captcha, challenge, WAF, 403, 412, risk control | `captcha-protocol-analysis`, `anti-bot-analysis` |
| TLS pinning, TrustManager, Cronet, NSURLSession | `tls-pinning-analysis`, `android-network-stack`, `crypto-dataflow-analysis` |
| PCAP, TCP, UDP, WebSocket, gRPC, Protobuf | `protocol-reconstruction`, `websocket-grpc-analysis` |
| iOS, Objective-C, Swift, dyld, jailbreak, IPA | `ios-runtime-analysis`, `ios-unpacking-and-dump`, `objc-swift-hooking` |
| Unity, IL2CPP, Unreal, anti-cheat | `unity-il2cpp-analysis`, `game-security-reversing`, `anti-cheat-kernel-analysis` |
| malware, C2, persistence, IOC, sandbox | `malware-triage`, `malware-dynamic-analysis`, `detection-rule-engineering` |
| firmware, U-Boot, SquashFS, IoT, BLE, USB | `firmware-and-iot-analysis`, `ble-usb-protocol-reversing` |
| crash, fuzz, minidump, coverage, harness | `fuzzing-and-crash-analysis`, `crash-dump-symbolication`, `emulation-unicorn-angr` |
| OAuth, JWT, GraphQL, cloud, agent, tool protocol | `cloud-api-reversing`, `llm-agent-security-reversing` |
| CTF, crackme, archive, flag, sandbox | `ctf-reversing`, `ctf-sandbox-orchestration` |

## Vendor and scenario shortcuts

| Clue | Shortcut module |
|---|---|
| Geetest | `vendor-geetest-captcha` |
| Tencent TCaptcha | `vendor-tencent-tcaptcha` |
| NetEase Yidun | `vendor-netease-yidun` |
| Dingxiang | `vendor-dingxiang-captcha` |
| Shumei | `vendor-shumei-captcha` |
| Aliyun NVC, AWSC, Baxia | `vendor-aliyun-nvc-baxia` |
| JD jcap, H5ST | `vendor-jd-jcap-h5st` |
| Ruishu RS, 412, acw_sc | `vendor-ruishu-rs` |
| Akamai, _abck, bm_sz, sensor_data | `vendor-akamai-bm` |
| Cloudflare, Turnstile, clearance | `vendor-cloudflare-waf`, `vendor-cloudflare-turnstile` |
| AWS WAF, aws-waf-token | `vendor-aws-waf` |
| Imperva, Incapsula, Reese84 | `vendor-imperva-incapsula` |
| DataDome, PerimeterX, Kasada | `vendor-datadome`, `vendor-perimeterx`, `vendor-kasada` |
| Douyin/TikTok a_bogus, x-bogus | `web-douyin-abogus-xbogus` |
| Xiaohongshu x-s, x-t | `web-xiaohongshu-xs-xt` |
| Taobao/Tmall MTOP, H5ST | `web-taobao-mtop-h5st` |
| Meituan mtgsig | `web-meituan-mtgsig` |
| Zhihu zse | `web-zhihu-zse` |
| Xueqiu acw, md5__1038 | `web-xueqiu-acw` |
| WeChat Mini Program | `wechat-miniprogram-reversing` |
| React Native, Flutter, Electron | `react-native-reversing`, `flutter-dart-reversing`, `electron-app-reversing` |

## Evidence contract

Use this case layout:

```text
case/
  case.yaml
  evidence/raw/
  evidence/derived/
  notes/timeline.md
  notes/hypotheses.md
  repro/
  tests/fixtures.jsonl
  report.md
```

Every result must include a plain-English summary, evidence, route, reproducible check, limitations, and next action. Never treat a static string, one log line, or an automatic decompiler result as a confirmed call chain without independent validation.

## Module catalog

Specialized modules live under `skills/<name>/SKILL.md`. Read only the modules matched by the routing tables. See `references/catalog.md`, `references/tool-matrix.md`, `references/evidence.md`, and `docs/BEGINNER.md`.
