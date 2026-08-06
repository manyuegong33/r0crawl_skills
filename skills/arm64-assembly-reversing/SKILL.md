---
name: arm64-assembly-reversing
description: |
  Beginner-friendly workflow for AArch64 calling conventions, prologues, PAC, BTI, registers, literals, and compiler idioms. Extracts general methods and evidence practices without depending on any author, private repository, personal path, secret, or branded prompt. Use when a reverse-engineering task needs reliable observation, loader analysis, runtime evidence, dump validation, crash attribution, tool setup, or reproducible reporting.
---

# AArch64 calling conventions, prologues, PAC, BTI, registers, literals, and compiler idioms

## Beginner mode

Explain the object, the observation question, the required evidence, the first tool, and the success criterion before using advanced terminology.

## Workflow

1. Record sample hash, version, architecture, environment, entry action, and objective.
2. Preserve raw artifacts before modifying, decoding, dumping, or patching anything.
3. Perform the smallest observation that can distinguish competing hypotheses.
4. Correlate static references with runtime stacks, registers, mappings, files, traffic, and outputs.
5. Record commands, tool versions, paths, offsets, timestamps, and first-difference locations.
6. Validate the result with a clean baseline, repeat run, edge case, and consumer tool or independent observation.

## Quality gates

- A string or one log line is not a call chain.
- A dump is not valid until its structure, mappings, imports/relocations, and consumer-tool behavior agree.
- A patch or observation hook is not stable until cold start, warm start, repeated calls, and clean baseline are compared.
- If a prerequisite is missing, report the smallest next artifact instead of changing the environment blindly.

## Deliverables

- Beginner summary.
- Evidence table and confidence level.
- Technical chain and unresolved hypotheses.
- Reproducible command, script, fixture, dump validation, or report.
- Limitations, rollback notes, and next action.
