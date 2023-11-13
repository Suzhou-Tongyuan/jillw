# Change Log

## v0.3.1

1. Use `normpath()` instead of `resolve()` to decide whether a path is already in `$PATH`, which helps to reduce the latency.

## v0.3.0

1. Improving latency by lazily loading `jill`.

2. `Development.toml` is loaded only if `DEV` is set to `1`.
