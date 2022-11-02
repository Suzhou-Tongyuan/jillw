from __future__ import annotations
import venv
import wisepy2
import shutil
import json
import sys
from pathlib import Path
from jill.install import install_julia


root = Path("~/.jlenvs").expanduser()


class Ops:
    @staticmethod
    def get_config(new_conf: "dict | None" = None) -> dict:
        config_file = root.joinpath("config.json")
        if config_file.exists():
            if new_conf is None:
                return json.load(config_file.open("r", encoding="utf-8"))
            json.dump(new_conf, config_file.open("w", encoding="utf-8"), indent=4)
            return new_conf

        config = new_conf or {"current": None}
        with config_file.open("w", encoding="utf-8") as f:
            json.dump({"current": None}, f)
        return config

    @staticmethod
    def create_(
        name: str,
        upstream: str = "",
        version: str = "",
        confirm: bool = False,
        unstable: bool = False,
    ):
        envdir = root.joinpath(name)
        Ops.get_config()
        if envdir.exists():
            raise IOError(f"{envdir} already exists")
        venv.create(envdir.as_posix(), with_pip=True)
        root.mkdir(mode=0o755, parents=True, exist_ok=True)
        install_julia(
            version=version or name,
            install_dir=envdir.joinpath("julia").as_posix(),
            confirm=confirm,
            upstream=upstream,
            unstable=unstable,
            skip_symlinks=True,
            reinstall=True
        )
        print(wisepy2.Green(f"Environment {name} created at {envdir.as_posix()}."))

    @staticmethod
    def env(name: str):
        Ops.get_config()
        envdir = root.joinpath(name)
        if not envdir.exists():
            raise IOError(f"{envdir} does not exist")
        return envdir.as_posix()

    @staticmethod
    def list():
        Ops.get_config()
        for each in root.iterdir():
            if each.is_dir():
                yield each

    @staticmethod
    def remove_(name: str):
        config = Ops.get_config()
        envdir = root.joinpath(name)
        if not envdir.exists():
            raise IOError(f"{envdir} does not exist")
        shutil.rmtree(envdir.as_posix())
        if config.get("current") == name:
            config["current"] = None
            Ops.get_config(config)
        print(wisepy2.Green(f"Environment {name} removed."))
