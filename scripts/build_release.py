"""Build a wheel and normalize the sdist archive for byte-for-byte rebuilds."""
import argparse
import gzip
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import tomllib


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=Path("dist"))
    args = parser.parse_args()
    try:
        epoch = int(os.environ["SOURCE_DATE_EPOCH"])
        if not 315532800 <= epoch < 2**32:
            raise ValueError
    except (KeyError, ValueError):
        parser.error("Set SOURCE_DATE_EPOCH to a Unix timestamp from 1980 through 2106")

    root = Path(__file__).resolve().parents[1]
    project = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    suffix = project["name"].replace("-", "_") + "-" + project["version"]
    args.outdir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as directory:
        staging = Path(directory)
        subprocess.run([sys.executable, "-m", "build", "--no-isolation", "--outdir", directory],
                       cwd=root, check=True)
        source_name = f"{suffix}.tar.gz"
        with (tarfile.open(staging / source_name, "r:gz") as original,
              (args.outdir / source_name).open("wb") as output,
              gzip.GzipFile(filename="", mode="wb", fileobj=output, mtime=epoch) as compressed,
              tarfile.open(fileobj=compressed, mode="w", format=tarfile.USTAR_FORMAT) as archive):
            for entry in sorted(original.getmembers(), key=lambda member: member.name):
                if not (entry.isfile() or entry.isdir()):
                    raise ValueError(f"Unexpected source archive entry: {entry.name}")
                mode = 0o755 if entry.isdir() or entry.mode & 0o111 else 0o644
                entry = entry.replace(mtime=epoch, uid=0, gid=0, uname="", gname="", mode=mode)
                payload = original.extractfile(entry) if entry.isfile() else None
                archive.addfile(entry, payload)
                if payload is not None:
                    payload.close()
        wheel = staging / f"{suffix}-py3-none-any.whl"
        shutil.copyfile(wheel, args.outdir / wheel.name)


if __name__ == "__main__":
    main()
