# Tool Matrix

| Task | First choice | Alternatives | Save as evidence |
|---|---|---|---|
| Browser network | Chrome DevTools, CDP | Playwright, mitmproxy, Burp | HAR, stack, request diff |
| JavaScript static analysis | Babel AST, source maps | esprima, recast | transformed code, node locations |
| APK/DEX | JADX, apktool, baksmali | Androguard, Ghidra | manifest, call graph, smali |
| Android runtime | Frida, adb, logcat | LLDB | hook log, stack, parameters |
| Native binaries | IDA, Ghidra, Binary Ninja | Rizin, radare2, objdump | functions, types, xrefs |
| Memory | WinDbg, gdb, lldb | Volatility | dump, modules, objects |
| Protocols | Wireshark, tshark | Scapy, Kaitai Struct | field table, state machine |
| Firmware | binwalk, 7-Zip, unsquashfs | FACT, Ghidra | image hash, filesystem |
| Fuzzing | AFL++, libFuzzer | Honggfuzz, boofuzz | seed, coverage, minimized crash |

Record tool version, command, timestamp, input hash, and environment variables. Treat automatic decompilation as a hypothesis until runtime or cross-reference evidence confirms it.
