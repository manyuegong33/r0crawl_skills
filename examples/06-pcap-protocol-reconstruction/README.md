# Example 06: PCAP protocol reconstruction

Goal: recover message boundaries, fields, state, and serialization from a capture.

Route: `protocol-reconstruction` -> `websocket-grpc-analysis` -> `protobuf-schema-recovery` -> `reconstruction-and-parity`.

Success: a small decoder handles normal and edge messages.
