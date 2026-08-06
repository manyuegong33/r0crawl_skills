# Example 03: Frida detection triage

Goal: distinguish a real detection signal from a startup or version problem.

Route: `frida-anti-detection-analysis` -> `syscall-filter-evidence` -> `anti-hook-artifact-analysis` -> `frida-stealth-hooking`.

Success: the suspected signal has a reproducible trigger, stack, thread, and clean-baseline comparison.
