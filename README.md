# JILL Wrapper

JILL Wrapper (`jillw`) is a lightweight and cross-platform Julia version manager. This work is based on [johnnychen94/jill.py](https://github.com/johnnychen94/jill.py) and [Python venv](https://docs.python.org/3/library/venv.html).

`jillw` targets several different use cases:

1. cross-platform julia installation
2. cross-platform julia version management (create, switch, remove, etc.)
3. providing the "one Julia, one Python" installation

## Installation

```bash
pip install -U jillw
```

## Usage

### Create environments

```shell
> jillw create --help
usage: create [-h] [--name NAME] [--upstream UPSTREAM] [--version VERSION] [--confirm] [--unstable] [name] [upstream] [version]

# create a new environment using Julia 1.8
> jillw create myenv --version 1.8
```

The explanations of the arguments except `name` are referred to [johnnychen94/jill.py](https://github.com/johnnychen94/jill.py).

### Activate environments

```shell
> jillw switch <envname>

> jillw switch myenv
```

### Start `julia` under environments

```shell
> jillw switch myenv
> julia --compile=min --quiet
julia> Sys.which("julia")
"~/.jlenvs/myenv/julia/julia-1.8/bin/julia.exe"
```

### List environments

```shell
> jillw list
myenv => ~/.jlenvs/myenv
latest => ~/.jlenvs/latest
```

### Remove environments

```shell
> jillw remove latest
Environment latest removed.
```

### Run commands under environments

```shell
> jillw switch myenv
> jillw run 'echo %VIRTUAL_ENV%'
~/.jlenvs/myenv
```


### Configuring the `julia` command (Experimental)

By creating a `Development.toml` at a working directory, you can conveniently configure the `julia` command to have the following features:

- reduce the startup time by using interpreted mode
- activate a project on startup
- preload some specified files on startup
- preload some modules on startup

Use `jillw devhere` to create a template `Development.toml` at the current working directory.

The following options can be modified to fit your needs:

- `min-latency`: a boolean that tells whether to use interpreted mode. This makes Julia code slow, but much faster at Julia startup and first-time module loading.

- `no-startup-file`: a boolean that tells whether to load the `~/.julia/config/startup.jl` file.

- `project`: a string thats indicates the path to the project that is expected to be activated on startup.

- `sysimage`: a string thats indicates the path to the sysimage that is expected to be used on startup.

- `using`: a list of strings that indicates the modules that are expected to be preloaded on startup.

- `files`: a list of strings that indicates the files that are expected to be preloaded on startup.

## License

See [LICENSE.md](./LICENSE.md).
