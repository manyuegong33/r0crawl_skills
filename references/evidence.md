# Evidence and Validation

## Case metadata

```yaml
case_id: reverse-YYYYMMDD-short-name
objective: locate-or-reproduce
platform: web|android|native|ios|protocol|firmware
artifact:
  path: null
  sha256: null
  version: null
environment:
  os: null
  runtime: null
  device: null
samples: []
constraints: []
```

## Hypothesis record

```markdown
## H-001
- Hypothesis:
- Supporting evidence:
- Falsifier:
- Smallest validation action:
- Result: pending|confirmed|rejected
```

## Parity fixtures

Include normal, edge, empty/default, encoding variation, repeated-call, and cross-version cases whenever possible. Store input, output, timestamp, random values or nonces, environment, and first-difference location.

## Confidence

- **A:** independent evidence, multiple fixtures, repeatable command.
- **B:** call chain confirmed, but one environment or algorithm detail remains unresolved.
- **C:** static clue or single observation; not a final conclusion.
