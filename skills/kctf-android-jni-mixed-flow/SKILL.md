---
name: kctf-android-jni-mixed-flow
description: Solve KCTF Android APKs with JNI bridges, native .so logic, channel splits, and mixed Java/native state machines. Use when the artifact includes classes.dex, lib/*.so, and the check is split across Java input, JNI dispatch, and native code.
---

# KCTF Android JNI Mixed Flow

## Workflow

1. Identify package, activity, JNI exports, and the native library path.
2. Separate Java-side validation from native-side validation.
3. Trace the full path:
   - Java input
   - JNI entry
   - native state transforms
   - final success string
4. Check for channel splits, hex/byte conversion, or fixed-size buffers before solving.
5. Verify on the original APK or extracted sample, not on decompiled pseudocode alone.

## Use this pattern

- `classes.dex` + `lib/*.so`
- `Java_com_*` JNI exports
- even/odd or split-channel transforms
- native anti-debug / state-machine / crypto logic

## Reference

- `references/pattern.md`
