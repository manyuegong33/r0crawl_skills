# r0crawl_skills

[Chinese Guide](docs/README.zh-CN.md)

A beginner-friendly, full-spectrum reverse-engineering skill collection for Codex-style AI agents.

r0crawl_skills is a router plus a large catalog of specialized modules. It starts simple for beginners, then routes into deeper workflows for web reversing, Android unpacking, Frida tracing, native binary analysis, protocol reconstruction, malware triage, firmware analysis, CTF tasks, and reproducible parity testing.

## Highlights

- 196 specialized reverse-engineering modules
- Beginner mode by default
- English Markdown by default
- Chinese guide available by link
- Evidence-first case workflow
- UTF-8 clean Markdown files
- Web, Android, iOS, Native, Frida, unpacking, anti-analysis, protocols, malware, firmware, CTF, fuzzing, cloud/API and game reversing coverage

## Quick start

Copy this folder into your Codex skills directory:

```powershell
Copy-Item -Recurse .\r0crawl_skills $env:USERPROFILE\.codex\skills\r0crawl_skills
```

Then ask:

```text
Use r0crawl_skills. Start a beginner-friendly investigation for this target.
```

## Beginner workflow

r0crawl_skills starts with four questions:

1. What are we analyzing?
2. What action matters?
3. What material do we already have?
4. What result do we want?

Then it creates a route instead of dumping every advanced term at once.

## Popular routes

| Goal | Modules |
|---|---|
| Android unpacking | `apk-protection-analysis`, `android-unpacking-and-dumping`, `dex-memory-dump` |
| Frida detected | `frida-anti-detection-analysis`, `frida-stealth-hooking`, `root-emulator-detection` |
| JS hook or sign | `js-hook-engineering`, `browser-runtime-tracing`, `webcrypto-hooking`, `web-signature-analysis` |
| Native reversing | `native-binary-analysis`, `ida-ghidra-workflow`, `symbol-recovery-and-structs` |
| Protocol reversing | `protocol-reconstruction`, `websocket-grpc-analysis`, `crypto-dataflow-analysis` |
| Malware triage | `malware-triage`, `malware-dynamic-analysis`, `detection-rule-engineering` |
| Firmware or IoT | `firmware-and-iot-analysis`, `ble-usb-protocol-reversing` |


## Runnable starter kit

The collection now includes small, dependency-light helpers under `scripts/`:

| Helper | Use |
|---|---|
| `init_case.py` | Create a reproducible case directory |
| `hash_artifact.py` | Hash and size a sample |
| `scan_strings.py` | Extract ASCII and UTF-16 strings |
| `parse_har_fields.py` | List HAR headers, query, body, and response fields |
| `compare_jsonl.py` | Compare parity fixtures |
| `redact_capture.py` | Redact common secrets before sharing captures |
| `validate_dump_manifest.py` | Validate a dump manifest and SHA-256 |
| `module_router.py` | Suggest modules from a plain-English query |
| `check_toolchain.py` | Report discoverable optional tools |
| `generate_report.py` | Generate a case file inventory |
| `frida_observe_template.js` | Observation-only Frida starter |
| `js_hook_template.js` | Fetch observation hook starter |
| `ida_export_template.py` | IDAPython export starter |

Example:

```powershell
python scripts/init_case.py demo-signature
python scripts/module_router.py "Android APK Frida dump dex"
python scripts/hash_artifact.py sample.apk
```

## Example playbooks

Start with one of the ten sanitized playbooks under [examples](examples/): web parity, DEX dump validation, Frida detection triage, JS/WebCrypto hooks, native loader tracing, PCAP reconstruction, malware detection, firmware analysis, selective emulation, and beginner reporting.

## Vendor and scenario packs

Shortcut modules exist for captcha providers, WAF and anti-bot systems, popular web signing families, mini programs, hybrid apps, Flutter, React Native, Electron, airline and travel flows, e-commerce risk control, finance data, logistics, government portals, live WebSocket protocols, Protobuf, GraphQL, and WASM signatures.

## Research-derived capability layers

The catalog includes reusable layers extracted from public reverse-engineering practice: early loader tracing, syscall observation, anonymous executable memory, dump/fix/rebuild validation, hardware-breakpoint observation, OLLVM recovery, IDA/Ghidra/Rizin automation, eBPF observability, staged malware analysis, C2 traffic reconstruction, detection engineering, safe lab management, case orchestration, selective emulation, and anti-cheat kernel analysis.

See [research notes](references/research-notes.md) for public sources and the no-copy extraction policy.

## Repository layout

```text
r0crawl_skills/
  SKILL.md
  README.md
  docs/README.zh-CN.md
  docs/BEGINNER.md
  references/
  scripts/
  skills/
```

## Module index

Generated index: [references/generated-index.md](references/generated-index.md)
"# r0crawl_skills" 
