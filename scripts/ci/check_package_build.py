"""Validate built lumid-hooks distributions."""

import argparse
import subprocess
import tempfile
import venv
from pathlib import Path


def _python_bin(env_dir: Path) -> Path:
    return env_dir / "bin" / "python"


def _run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)  # nosec B603: fixed argv list, no shell.


def _wheel(dist_dir: Path) -> Path:
    wheels = sorted(dist_dir.glob("lumid_hooks-*-py3-none-any.whl"))
    if len(wheels) != 1:
        raise SystemExit(f"Expected one lumid-hooks wheel, found {len(wheels)}")
    return wheels[0]


def _smoke_install(wheel: Path) -> None:
    """Install the built wheel in a fresh venv and exercise public imports."""
    code = """
from lumid_hooks import BaseBindings, HookBindings, PrincipalContext, ResourceRef

assert isinstance(BaseBindings(), HookBindings)

p = PrincipalContext(
    principal_id="p",
    org_id="o",
    external_id="e",
    principal_type="user",
    scopes=[],
)
r = ResourceRef(kind="k")
assert p.principal_id == "p" and r.kind == "k"
"""
    with tempfile.TemporaryDirectory(prefix="lumid-hooks-smoke-") as tmp:
        env_dir = Path(tmp) / ".venv"
        venv.EnvBuilder(with_pip=True).create(env_dir)
        python = _python_bin(env_dir)
        _run(
            [
                python.as_posix(),
                "-m",
                "pip",
                "install",
                wheel.as_posix(),
            ]
        )
        _run([python.as_posix(), "-c", code])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dist",
        default="dist",
        type=Path,
        help="Directory containing distributions built by `uv build`.",
    )
    args = parser.parse_args()

    dist_dir = args.dist.resolve()
    if not dist_dir.is_dir():
        raise SystemExit(f"Distribution directory does not exist: {dist_dir}")

    _smoke_install(_wheel(dist_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
