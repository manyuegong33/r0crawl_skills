# Beginner Guide

This guide explains how to use r0crawl_skills without already knowing reverse-engineering terminology.

## Step 1: Describe the target

Use one sentence:

```text
I have an APK and I want to understand how login encryption works.
```

or:

```text
I have a website request and I want to reproduce the sign parameter.
```

## Step 2: Provide evidence

Useful evidence includes:

- file path
- URL
- HAR file
- PCAP file
- screenshot
- logcat output
- Frida log
- stack trace
- request and response sample
- expected input and output pair

## Step 3: Choose the result

Common results:

- locate the function
- explain the behavior
- dump the real DEX
- write a Frida observation hook
- recover request signing logic
- reproduce a request locally
- produce a report

## Step 4: Keep a case folder

r0crawl_skills prefers this layout:

```text
case/
  evidence/raw/
  notes/timeline.md
  notes/hypotheses.md
  repro/
  tests/fixtures.jsonl
  report.md
```

## Step 5: Validate before claiming success

A result is strong only when it has:

- the original sample
- observed runtime behavior
- a repeatable command or script
- more than one test case
- a written limitation section
