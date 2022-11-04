from __future__ import annotations
import tomli
import os
import pathlib
import wisepy2
import json

EMPTY_CONFIG = \
r"""
[julia]
min-latency = false
quiet-start = false
no-startup-file = false
interactive = true

# activate the specified project
project = ""

# this path specifies the path to your sysimage
sysimage = ""

# start Julia with loading these modules
using = []

# start Julia with executing these files
files = []
"""

def get_bool(conf: dict, name: str) -> bool | None:
    if conf.get(name, name):
        var = conf[name]
        if not isinstance(var, bool):
            raise ValueError("'{}' must be a boolean".format(name))
        return var

def get_int(conf: dict, name: str) -> int | None:
    if conf.get(name, name):
        var = conf[name]
        if not isinstance(var, int):
            raise ValueError("'{}' must be a int".format(name))
        return var

def get_str_list(conf: dict, name: str) -> list[str] | None:
    if conf.get(name, name):
        var = conf[name]
        if not isinstance(var, list) and not (all(isinstance(e, str) for e in var)):
            raise ValueError("'{}' must be a string list".format(name))
        return var

def get_str(conf: dict, name: str) -> str | None:
    if conf.get(name, name):
        var = conf[name]
        if not isinstance(var, str):
            raise ValueError("'{}' must be a string".format(name))
        return var

def write_empty_config_():
    cwd = pathlib.Path(os.getcwd())
    dev = cwd / "Development.toml"
    if dev.is_file():
        print(wisepy2.Yellow("Warning: Development.toml already exists"))
        return
    else:
        with dev.open("w", encoding="utf-8") as f:
            f.write(EMPTY_CONFIG)

def get_options() -> list[str]:
    cwd = pathlib.Path(os.getcwd())
    dev = cwd / "Development.toml"
    if dev.is_file():
        io = dev.open('rb')
        conf = tomli.load(io) # type: ignore
        if not isinstance(conf, dict):
            return []
        conf = conf.get("julia")
        if not isinstance(conf, dict):
            return []
    else:
        return []
    opts: list[str] = []

    if get_bool(conf, 'min-latency'):
        opts.append("--compile=min")
        opts.append("-O0")

    if project := get_str(conf, "project"):
        opts.append("--project={}".format(project))

    if get_bool(conf, "interactive"):
        opts.append("-i")

    if get_bool(conf, 'quiet-start'):
        opts.append("--quiet")

    if sysimage := get_str(conf, "sysimage"):
        opts.append("--sysimage")
        opts.append(sysimage)

    if get_bool(conf, "no-startup-file"):
        opts.append("--startup-file=no")

    if preload_modules := get_str_list(conf, 'using'):
        for each in preload_modules:
            opts.append("-e")
            opts.append("using {}".format(each))

    if preincluded_files := get_str_list(conf, 'files'):
        for file in preincluded_files:
            opts.append("-e")
            opts.append(
                'include(' +
                'raw' +json.dumps(str(cwd / file), ensure_ascii=False) +
                ')'
            )

    return opts
