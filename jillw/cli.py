from __future__ import annotations
from jillw import Ops
from wisepy2 import wise
from pathlib import Path
import os
import contextlib
import io
import sys
import subprocess
import wisepy2
import shlex


def find_julia_binary_dir(env: Path):
    found = next(env.joinpath("julia").iterdir(), None)
    if found is None:
        raise IOError(f"No Julia installation found at {env}")
    return found.joinpath("bin")


@contextlib.contextmanager
def cmd_session():
    try:
        yield
    except IOError as e:
        print(wisepy2.Red("{}: {}".format(type(e).__name__, str(e))), file=sys.stderr)
        sys.exit(1)


@contextlib.contextmanager
def expect_no_stdout():
    sio = io.StringIO()
    try:
        with contextlib.redirect_stdout(sio):
            yield
    finally:
        msg = sio.getvalue()
        print(wisepy2.Red(msg), file=sys.stderr)


def _expand_or_resolve(p: Path | str):
    if isinstance(p, str):
        p = Path(p)
    try:
        return p.resolve()
    except:
        return p.absolute()


def append_PATH(PATH: str, *paths: Path):
    has_added = [False] * len(paths)
    PATHs = set(map(_expand_or_resolve, PATH.split(os.pathsep)))
    for i, path in enumerate(paths):
        try:
            path = path.resolve()
        except:
            continue
        if path in PATHs:
            has_added[i] = True
    return (
        os.pathsep.join(
            [str(paths[i]) for i, added in enumerate(has_added) if not added]
        )
        + os.pathsep
        + PATH
    )

def run_with_activated_env(cmd: list[str]):
    config = Ops.get_config()
    current: str | None = config["current"]

    if current is None:
        print(wisepy2.Yellow("No activated environment"), sys.stdout)
        return
    env = Path(Ops.env(current))
    jlbindir = find_julia_binary_dir(env)
    if os.name == "nt":
        envdict = os.environ.copy()
        envdict["VIRTUAL_ENV"] = str(env)
        envdict["PYTHONHOME"] = ""
        envdict['PATH'] = append_PATH(os.environ["PATH"], jlbindir, env / "Scripts")
    else:
        envdict = os.environ.copy()
        envdict["VIRTUAL_ENV"] = str(env)
        envdict["PYTHONHOME"] = ""
        envdict['PATH'] = append_PATH(os.environ["PATH"], jlbindir, env / "bin")

    subprocess.run(cmd, env=envdict, shell=True)

class Main:
    @staticmethod
    def switch(name: str):
        with cmd_session():
            env = Ops.env(name)
            config = Ops.get_config()
            config["current"] = name
            Ops.get_config(config)
            print(wisepy2.Green(f"Switched to {name} at {env}"))

    @staticmethod
    def run(cmd: str):
        run_with_activated_env(shlex.split(cmd))

    @staticmethod
    def create(
        name: str,
        upstream: str = "",
        version: str = "",
        confirm: bool = False,
        unstable: bool = False,
    ):
        with cmd_session():
            Ops.create_(name, upstream, version, confirm, unstable)

    @staticmethod
    def remove(name: str):
        with cmd_session():
            Ops.remove_(name)

    @staticmethod
    def list():
        with cmd_session():
            for each in Ops.list():
                print(wisepy2.Purple(each.name, "=>", each.as_posix(), sep=" "))

def main():
    wise(Main)()

def julia():
    run_with_activated_env(["julia", *sys.argv[1:]])
