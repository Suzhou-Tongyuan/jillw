# Change Log

## v0.3.1

1. Force appending environment specific binary directories to `PATH`:

   - the directory of julia executable

   - the directory of Python `Scripts/` directory

## v0.3.0

1. Improving latency by lazily loading `jill`.

2. `Development.toml` is loaded only if `DEV` is set to `1`.
