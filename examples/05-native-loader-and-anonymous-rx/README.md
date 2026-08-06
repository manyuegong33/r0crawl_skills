# Example 05: Native loader and anonymous executable memory

Goal: correlate constructors, dynamic loading, anonymous RX mappings, and the real code path.

Route: `constructor-dlopen-tracing` -> `hidden-rx-memory-reconstruction` -> `native-unpacking` -> `packed-so-elf-rebuild`.

Success: runtime mapping and static artifact are tied to the same code region.
