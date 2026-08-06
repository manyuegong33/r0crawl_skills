# r0crawl_skills 中文简介

[English README](../README.md)

这是一个面向 Codex 风格 Agent 的全栈逆向技能集合。默认页面是英文，点击本页即可查看中文简介。

## 适合的任务

- Web / JavaScript 逆向、JS Hook、sign、token、cookie
- Android APK/AAB/DEX 分析、脱壳、DEX dump
- Frida Hook、Frida 检测、Root / 模拟器检测
- JNI、Native、SO、ELF、PE、Mach-O
- iOS、Objective-C、Swift、dyld
- TLS Pinning、OkHttp、Cronet、WebCrypto
- PCAP、TCP、UDP、WebSocket、gRPC、Protobuf
- 固件、IoT、BLE、USB
- 恶意样本、IOC、YARA、Sigma、沙箱
- CTF、crackme、fuzz、crash、Unicorn、angr

## 厂商与场景专项

- 极验、腾讯验证码、网易易盾、顶象、数美
- 阿里 NVC/AWSC/Baxia、京东 jcap/H5ST
- 瑞数 RS、Akamai、Cloudflare、AWS WAF
- Imperva、DataDome、PerimeterX、Kasada
- 抖音 a_bogus/x-bogus、小红书 x-s/x-t
- MTOP、美团 mtgsig、知乎 zse、雪球 acw
- 微信小程序、支付宝小程序、Flutter、React Native、Electron、uni-app

## 小白启动方式

```text
Use r0crawl_skills. 按小白模式 start，帮我分析这个 APK。
```

Agent 会先确认分析对象、关键动作、现有材料和目标产物，然后再选择合适的 skill 和工具。

## 输出风格

先输出小白摘要，再输出技术附录：证据、路由、脚本、复现、限制和下一步。

## 编码说明

所有文件使用 UTF-8。默认 Markdown 为英文，中文只放在本页。
