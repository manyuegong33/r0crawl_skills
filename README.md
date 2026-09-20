# r0crawl_skills

一套面向 Codex 风格 AI 代理的、对新手友好的全谱系逆向工程技能合集。

r0crawl_skills 是一个"路由器 + 大量专用模块"的技能库。它对新手从简单入口开始，再按目标类型路由到更深的工作流：Web 逆向、Android 脱壳、Frida 追踪、原生二进制分析、协议还原、恶意软件分诊、固件分析、CTF 任务、可复现一致性测试。

## 亮点

- 196 个专用逆向工程模块
- 默认新手模式
- 全中文说明
- 证据优先的案件工作流
- UTF-8 干净 Markdown 文件
- 覆盖 Web、Android、iOS、原生、Frida、脱壳、反分析、协议、恶意软件、固件、CTF、模糊测试、云/API、游戏逆向

## 快速开始

把本目录复制到 Codex 技能目录：

```powershell
Copy-Item -Recurse .\r0crawl_skills $env:USERPROFILE\.codex\skills\r0crawl_skills
```

然后直接问：

```text
使用 r0crawl_skills。对这个目标开始一次新手友好的调查。
```

## 新手工作流

r0crawl_skills 从四个问题开始：

1. 我们要分析什么？
2. 哪个动作最关键？
3. 手上已经有什么材料？
4. 想要什么结果？

然后它给出一条路线，而不是一次性抛出所有高级术语。

## 热门路线

| 目标 | 模块 |
|---|---|
| Android 脱壳 | `apk-protection-analysis`、`android-unpacking-and-dumping`、`dex-memory-dump` |
| Frida 被检测 | `frida-anti-detection-analysis`、`frida-stealth-hooking`、`root-emulator-detection` |
| JS hook 或签名 | `js-hook-engineering`、`browser-runtime-tracing`、`webcrypto-hooking`、`web-signature-analysis` |
| 原生逆向 | `native-binary-analysis`、`ida-ghidra-workflow`、`symbol-recovery-and-structs` |
| 协议逆向 | `protocol-reconstruction`、`websocket-grpc-analysis`、`crypto-dataflow-analysis` |
| 恶意软件分诊 | `malware-triage`、`malware-dynamic-analysis`、`detection-rule-engineering` |
| 固件或 IoT | `firmware-and-iot-analysis`、`ble-usb-protocol-reversing` |


## 可运行入门套件

合集在 `scripts/` 下提供了一组依赖很轻的小工具：

| 工具 | 用途 |
|---|---|
| `init_case.py` | 创建可复现的案件目录 |
| `hash_artifact.py` | 计算样本哈希与大小 |
| `scan_strings.py` | 提取 ASCII 与 UTF-16 字符串 |
| `parse_har_fields.py` | 列出 HAR 头、查询、正文、响应字段 |
| `compare_jsonl.py` | 对比一致性夹具 |
| `redact_capture.py` | 分享抓包前脱敏常见密钥 |
| `validate_dump_manifest.py` | 校验转储清单与 SHA-256 |
| `module_router.py` | 用大白话查询推荐模块 |
| `check_toolchain.py` | 报告可发现的可选工具 |
| `generate_report.py` | 生成案件文件清单 |
| `frida_observe_template.js` | 仅观察的 Frida 起步模板 |
| `js_hook_template.js` | Fetch 观察 hook 起步模板 |
| `ida_export_template.py` | IDAPython 导出起步模板 |

示例：

```powershell
python scripts/init_case.py demo-signature
python scripts/module_router.py "Android APK Frida dump dex"
python scripts/hash_artifact.py sample.apk
```

## 示例手册

从 [examples](examples/) 下的十个脱敏手册任选一个开始：Web 一致性、DEX 转储校验、Frida 检测分诊、JS/WebCrypto hook、原生加载器追踪、PCAP 还原、恶意软件检测、固件分析、选择性仿真、新手报告。

## 厂商与场景包

针对验证码厂商、WAF 与反爬系统、常见 Web 签名家族、小程序、混合应用、Flutter、React Native、Electron、航空出行、电商风控、金融数据、物流、政务门户、直播 WebSocket 协议、Protobuf、GraphQL、WASM 签名等都有快捷模块。

## 研究提炼的能力层

目录包含从公开逆向实践中提炼的可复用能力层：早期加载器追踪、系统调用观察、匿名可执行内存、转储/修复/重建校验、硬件断点观察、OLLVM 还原、IDA/Ghidra/Rizin 自动化、eBPF 可观测、分阶段恶意软件分析、C2 流量还原、检测工程、安全实验管理、案件编排、选择性仿真、反作弊内核分析。

公开来源与"不复制"提炼策略见 [研究笔记](references/research-notes.md)。

## 仓库布局

```text
r0crawl_skills/
  SKILL.md
  README.md
  docs/
  references/
  scripts/
  skills/
```

## 模块索引

生成的索引见 [references/generated-index.md](references/generated-index.md)。
