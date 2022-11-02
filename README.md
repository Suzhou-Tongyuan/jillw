# JILL Wrapper

JILL Wrapper (`jillw`) is a lightweight and cross-platform Julia version manager. This work is based on [johnnychen94/jill.py](https://github.com/johnnychen94/jill.py) and [Python venv](https://docs.python.org/3/library/venv.html).

`jillw` targets several different use cases:

1. cross-platform julia installation
2. cross-platform julia version management
3. providing the "one Julia, one Python" installation

## Installation

```bash
pip install -U jillw
```

## Usage

### Create environments

```shell
> jillw create --help
usage: create [-h] [--name NAME] [--upstream UPSTREAM] [--version VERSION] [--confirm CONFIRM] [--unstable UNSTABLE] [name] [upstream] [version] [confirm] [unstable]

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

## License

See [LICENSE.md](./LICENSE.md).
