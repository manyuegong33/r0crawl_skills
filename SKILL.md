---
name: r0crawl-skills
description: 面向新手的全谱系逆向工程路由器，覆盖 Web/JavaScript、Android/iOS、Frida、脱壳、反分析、原生二进制、协议、固件、恶意软件、游戏、云 API、CTF、可复现一致性测试。用于逆向、起步、脱壳、反编译、hook、Frida、绕过检测、APK/SO/DEX/JS/PCAP/WASM/PE/ELF/Mach-O 分析、签名还原，或从样本到验证结果的完整调查。
---

# r0crawl_skills

## 新手优先约定

在使用高级工具前，先解释清楚：

1. 目标是什么：网页、JavaScript、APK、DEX、原生库、二进制、协议、固件或样本。
2. 哪个动作关键：启动、登录、搜索、上传、支付、加密、校验或网络交换。
3. 已有什么材料：文件、URL、HAR、PCAP、日志、截图、转储、源码或只有一段描述。
4. 想要什么结果：解释行为、定位入口、写 hook、脱运行时产物、复现请求或写报告。

如果没有任何产物，先给一份简短的采集计划，而不是假装分析一个看不见的目标。

## 启动协议

对于 `start`、`reverse start`、`mixed start`、`full reverse`：

1. 跑 `triage-and-route`。
2. 用 `evidence-collection` 建证据与时间线。
3. 把工作拆成静态、运行时、加载/脱壳、协议、数据流五条线。
4. 只加载路由表命中的模块。
5. 用 `reconstruction-and-parity` 做最小可复现结果。
6. 每一处不一致都用 `systematic-debugging`。
7. 先给新手摘要，再给技术附录。

## 核心路由

| 信号 | 优先加载 |
|---|---|
| APK、AAB、DEX、smali、类加载器 | `android-static-analysis`、`android-unpacking-and-dumping`、`dex-memory-dump` |
| APK 保护、壳、打包器、加载器、OEP | `apk-protection-analysis`、`native-unpacking`、`packer-and-loader-analysis` |
| SO、PE、ELF、Mach-O、汇编、反编译器 | `native-binary-analysis`、`ida-ghidra-workflow`、`symbol-recovery-and-structs` |
| Frida、Java.perform、Interceptor、spawn、attach | `frida-dynamic-analysis`、`frida-stealth-hooking` |
| 反 Frida、maps、端口、线程、Gadget、Root、模拟器 | `frida-anti-detection-analysis`、`root-emulator-detection`、`anti-analysis-and-integrity` |
| JavaScript hook、fetch、XHR、WebSocket、Proxy、getter/setter | `js-hook-engineering`、`browser-runtime-tracing`、`webcrypto-hooking` |
| Worker、iframe、ServiceWorker、Blob URL、importScripts | `js-worker-hooking`、`browser-runtime-tracing` |
| 混淆、JSFuck、AAEncode、webpack、控制流平坦化 | `js-deobfuscation`、`ast-program-analysis`、`ollvm-deobfuscation` |
| JSVMP、VMP、opcode、DSL VM、虚拟机 | `jsvmp-vmp-analysis`、`virtualization-protection`、`script-vm-sandbox-analysis` |
| sign、token、cookie、header、加解密请求或响应 | `web-signature-analysis`、`crypto-dataflow-analysis`、`reconstruction-and-parity` |
| 浏览器环境、canvas、WebGL、webdriver、指纹 | `browser-env-emulation`、`browser-fingerprint-analysis` |
| 验证码、挑战、WAF、403、412、风控 | `captcha-protocol-analysis`、`anti-bot-analysis` |
| TLS 固定、TrustManager、Cronet、NSURLSession | `tls-pinning-analysis`、`android-network-stack`、`crypto-dataflow-analysis` |
| PCAP、TCP、UDP、WebSocket、gRPC、Protobuf | `protocol-reconstruction`、`websocket-grpc-analysis` |
| iOS、Objective-C、Swift、dyld、越狱、IPA | `ios-runtime-analysis`、`ios-unpacking-and-dump`、`objc-swift-hooking` |
| Unity、IL2CPP、Unreal、反作弊 | `unity-il2cpp-analysis`、`game-security-reversing`、`anti-cheat-kernel-analysis` |
| 恶意软件、C2、持久化、IOC、沙箱 | `malware-triage`、`malware-dynamic-analysis`、`detection-rule-engineering` |
| 固件、U-Boot、SquashFS、IoT、BLE、USB | `firmware-and-iot-analysis`、`ble-usb-protocol-reversing` |
| 崩溃、模糊测试、minidump、覆盖率、harness | `fuzzing-and-crash-analysis`、`crash-dump-symbolication`、`emulation-unicorn-angr` |
| OAuth、JWT、GraphQL、云、代理、工具协议 | `cloud-api-reversing`、`llm-agent-security-reversing` |
| CTF、crackme、压缩包、flag、沙箱 | `ctf-reversing`、`ctf-sandbox-orchestration` |
| PyInstaller、pyc、PYZ、pythonXY.dll、冻结 Python | `python-frozen-app-reversing`、`ctf-reverse-pivot-control` |
| CPython 帧、code object、PyEval、marshal 运行时 | `cpython-runtime-introspection` |
| CTF 密钥、序列号、已知明文、重复 XOR | `ctf-key-recovery`、`reconstruction-and-parity` |

## 厂商与场景快捷方式

| 线索 | 快捷模块 |
|---|---|
| 极验 Geetest | `vendor-geetest-captcha` |
| 腾讯 TCaptcha | `vendor-tencent-tcaptcha` |
| 网易易盾 | `vendor-netease-yidun` |
| 顶象 | `vendor-dingxiang-captcha` |
| 数美 | `vendor-shumei-captcha` |
| 阿里云 NVC、AWSC、Baxia | `vendor-aliyun-nvc-baxia` |
| 京东 jcap、H5ST | `vendor-jd-jcap-h5st` |
| 瑞数 RS、412、acw_sc | `vendor-ruishu-rs` |
| Akamai、_abck、bm_sz、sensor_data | `vendor-akamai-bm` |
| Cloudflare、Turnstile、clearance | `vendor-cloudflare-waf`、`vendor-cloudflare-turnstile` |
| AWS WAF、aws-waf-token | `vendor-aws-waf` |
| Imperva、Incapsula、Reese84 | `vendor-imperva-incapsula` |
| DataDome、PerimeterX、Kasada | `vendor-datadome`、`vendor-perimeterx`、`vendor-kasada` |
| 抖音/TikTok a_bogus、x-bogus | `web-douyin-abogus-xbogus` |
| 小红书 x-s、x-t | `web-xiaohongshu-xs-xt` |
| 淘宝/天猫 MTOP、H5ST | `web-taobao-mtop-h5st` |
| 美团 mtgsig | `web-meituan-mtgsig` |
| 知乎 zse | `web-zhihu-zse` |
| 雪球 acw、md5__1038 | `web-xueqiu-acw` |
| 微信小程序 | `wechat-miniprogram-reversing` |
| React Native、Flutter、Electron | `react-native-reversing`、`flutter-dart-reversing`、`electron-app-reversing` |

## 证据约定

使用以下案件目录结构：

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

每个结果都必须包含：大白话摘要、证据、路线、可复现检查、局限性、下一步动作。绝不能把单个静态字符串、单行日志或自动反编译结果当作已确认的调用链，必须有独立验证。

## 模块目录

专用模块在 `skills/<name>/SKILL.md` 下。只读路由表命中的模块。参见 `references/catalog.md`、`references/tool-matrix.md`、`references/evidence.md`、`docs/BEGINNER.md`。
