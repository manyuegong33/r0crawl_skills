# KCTF Android JNI Mixed Flow Pattern

## Facts from KCTF 6

- APK content: `classes.dex`, `AndroidManifest.xml`, `lib/arm64-v8a/libkctf.so`
- Java package seen in the binary: `com.autorun.kctf.MainActivity`
- JNI export: `Java_com_autorun_kctf_MainActivity_nativeProcessInput`
- Success string in native strings: `Correct! Flag accepted.`

## Native shape

- ARM64 native code
- NEON `ld2` appears early, so channel splitting is likely
- The code carries a staged obfuscated constant flow and stack protector
- Treat Java and native checks as separate gates

## What to do

1. Confirm the Java entry point and input path.
2. Find the JNI bridge.
3. Disassemble the native export.
4. Recover the transform chain and channel split.
5. Verify against the success string on the original app.

## Signals

- hex or short bounded input
- JNI glue plus native checks
- split lanes / even-odd transform
- mixed Java/native state machine
