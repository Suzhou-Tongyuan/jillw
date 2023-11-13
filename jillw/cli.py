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
        print(wisepy2.Red("{}: {}".format(type(e).__name__, str(e))))
        sys.exit(1)


@contextlib.contextmanager
def expect_no_stdout():
    sio = io.StringIO()
    try:
        with contextlib.redirect_stdout(sio):
            yield
    finally:
        msg = sio.getvalue()
        print(wisepy2.Red(msg))

def append_PATH(PATH: str, *paths: Path):
    return os.pathsep.join([
        *map(os.path.normpath, paths),
        *PATH.split(os.pathsep)
    ])

def run_with_activated_env(cmd: list[str]):
    config = Ops.get_config()
    current: str | None = config["current"]

    if current is None:
        print(wisepy2.Yellow("No activated environment"))
        return

    env = Path(Ops.env(current))
    jlbindir = find_julia_binary_dir(env)

    if cmd and cmd[0] == "julia":
        if os.name == "nt":
            cmd[0] = jlbindir.joinpath("julia.exe").as_posix()
        else:
            cmd[0] = jlbindir.joinpath("julia").as_posix()

    if os.name == "nt":
        envdict = os.environ.copy()
        envdict["VIRTUAL_ENV"] = str(env)
        try:
            del envdict["PYTHONHOME"]
        except KeyError:
            pass
        envdict['PATH'] = append_PATH(os.environ["PATH"], jlbindir, env, env / "Scripts")
    else:
        envdict = os.environ.copy()
        envdict["VIRTUAL_ENV"] = str(env)
        try:
            del envdict["PYTHONHOME"]
        except KeyError:
            pass
        envdict['PATH'] = append_PATH(os.environ["PATH"], jlbindir, env, env / "bin")

    subprocess.run(cmd, env=envdict, shell=False)

class Main:
    @staticmethod
    def switch(name: str):
        """Switch to the specified environment"""
        with cmd_session():
            env = Ops.env(name)
            config = Ops.get_config()
            config["current"] = name
            Ops.get_config(config)
            print(wisepy2.Green(f"Switched to {name} at {env}"))

    @staticmethod
    def run(cmd: str):
        """Run a command in the activated environment"""
        run_with_activated_env(shlex.split(cmd))

    @staticmethod
    def create(
        name: str,
        version: str = "",
        upstream: str = "",
        confirm: bool = False,
        unstable: bool = False,
    ):
        """Create a new Julia environment
        """
        with cmd_session():
            Ops.create_(name, upstream, version, confirm, unstable)

    @staticmethod
    def remove(name: str):
        """Remove a Julia environment
        """
        with cmd_session():
            Ops.remove_(name)

    @staticmethod
    def list():
        """List all Julia environments
        """
        with cmd_session():
            for each in Ops.list():
                print(wisepy2.Purple(each.name, "=>", each.as_posix(), sep=" "))

    @staticmethod
    def devhere():
        """Create a Development.toml at the current directory.
        """
        with cmd_session():
            from . configloader import write_empty_config_
            write_empty_config_()

def main():
    wise(Main)()

def julia():
    extra_options: list[str] = []

    if os.environ.get("DEV", "").strip():
        from jillw.configloader import get_options
        extra_options = get_options()

    run_with_activated_env(["julia", *extra_options, *sys.argv[1:]])
