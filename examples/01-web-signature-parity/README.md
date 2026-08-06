# Example 01: Web signature parity

Goal: compare browser output with a local implementation.

Inputs: HAR, request body, timestamp, headers, and at least three fixtures.

Route: `browser-runtime-tracing` -> `web-signature-analysis` -> `crypto-dataflow-analysis` -> `reconstruction-and-parity`.

Success: the local result matches every fixture, or the first mismatch is documented.
