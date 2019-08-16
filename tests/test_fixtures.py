from pathlib import Path
from pytest_wdl.fixtures import (
    ENV_WDL_CONFIG, DEFAULT_WDL_CONFIG_FILE, import_dirs, wdl_config_file
)
from pytest_wdl.utils import tempdir
import pytest
from . import setenv


def test_wdl_config_file():
    with tempdir() as d:
        config = d / "config.json"
        with setenv({ENV_WDL_CONFIG: config}):
            with pytest.raises(FileNotFoundError):
                wdl_config_file()
            with open(config, "wt") as out:
                out.write("foo")
            assert wdl_config_file() == config

    with tempdir() as d, setenv({"HOME": str(d)}):
        config = d / DEFAULT_WDL_CONFIG_FILE
        with open(config, "wt") as out:
            out.write("foo")
        assert wdl_config_file() == config


def test_fixtures(workflow_data, workflow_runner):
    inputs = {
        "in_txt": workflow_data["in_txt"],
        "in_int": 1
    }
    outputs = {
        "out_txt": workflow_data["out_txt"],
        "out_int": 1
    }
    workflow_runner("tests/test.wdl", "cat_file", inputs, outputs)


def test_import_dirs():
    with pytest.raises(FileNotFoundError):
        import_dirs(Path.cwd(), "foo")

    with tempdir() as d:
        foo = d / "foo"
        with open(foo, "wt") as out:
            out.write("bar")
        with pytest.raises(FileNotFoundError):
            import_dirs(d, foo)

    with tempdir(change_dir=True) as cwd:
        tests = cwd / "tests"
        tests.mkdir()
        assert import_dirs(None, None) == []
