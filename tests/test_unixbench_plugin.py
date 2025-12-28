from pathlib import Path

import pytest

from lb_unixbench_plugin.plugin import (
    PLUGIN,
    UnixBenchConfig,
    UnixBenchGenerator,
    WorkloadIntensity,
)


def test_preset_configs(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("os.cpu_count", lambda: 8)

    low = PLUGIN.get_preset_config(WorkloadIntensity.LOW)
    med = PLUGIN.get_preset_config(WorkloadIntensity.MEDIUM)
    high = PLUGIN.get_preset_config(WorkloadIntensity.HIGH)

    assert low and (low.threads, low.iterations) == (1, 1)
    assert med and (med.threads, med.iterations) == (4, 1)
    assert high and (high.threads, high.iterations) == (8, 2)


def test_build_command_includes_tests_and_args() -> None:
    cfg = UnixBenchConfig(
        threads=2,
        iterations=3,
        tests=["dhry2reg", "whetstone-double"],
        extra_args=["--foo"],
        debug=True,
    )
    cmd = UnixBenchGenerator(cfg)._build_command()
    assert cmd == [
        "./Run",
        "-c",
        "2",
        "-i",
        "3",
        "dhry2reg",
        "whetstone-double",
        "--verbose",
        "--foo",
    ]


def test_validate_environment(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    workdir = tmp_path / "UnixBench"
    workdir.mkdir()
    run_file = workdir / "Run"
    run_file.write_text("#!/bin/sh\necho ok\n")
    run_file.chmod(0o755)

    cfg = UnixBenchConfig(workdir=workdir)
    gen = UnixBenchGenerator(cfg)
    assert gen._validate_environment() is True


def test_validate_environment_missing(tmp_path: Path) -> None:
    cfg = UnixBenchConfig(workdir=tmp_path / "missing")
    gen = UnixBenchGenerator(cfg)
    assert gen._validate_environment() is False


def test_run_command_collects_output(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    workdir = tmp_path / "UnixBench"
    workdir.mkdir()
    run_file = workdir / "Run"
    run_file.write_text("#!/bin/sh\necho hello\n")
    run_file.chmod(0o755)

    popen_calls = {}

    def fake_popen(cmd, cwd=None, stdout=None, stderr=None, text=None, **_kwargs):
        popen_calls["cmd"] = cmd
        popen_calls["cwd"] = cwd

        class DummyProc:
            def __init__(self):
                self.returncode = 0

            def communicate(self, timeout=None):
                return "hello\n", ""

        return DummyProc()

    monkeypatch.setattr("subprocess.Popen", fake_popen)

    cfg = UnixBenchConfig(workdir=workdir)
    gen = UnixBenchGenerator(cfg)
    gen._run_command()

    assert popen_calls["cwd"] == workdir
    assert popen_calls["cmd"][0] == "./Run"
    assert gen._result["returncode"] == 0
