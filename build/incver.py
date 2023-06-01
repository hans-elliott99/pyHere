#!/usr/bin/env python

# Increment the version number in pyproject.toml
import sys
from therepy import Here
here = Here("therepy")

if len(sys.argv) < 2:
    raise SystemExit("""
[ERROR] Required argument is missing.
Usage: ./incver.py n
    - n : int
        The part of the version string (x.xx.xx) to increment.
        Either 1 (major), 2 (minor), or 3 (patch).
""")
v_num = int(sys.argv[1])  # version number: major(1).minor(2).patch(3)


def format_new_ver(v_str, v_num):
    abc = v_str.split('.')
    v = str(int(abc[v_num - 1]) + 1)
    if v_num > 1 and int(v) < 10:
        v = "0" + v
    abc[v_num - 1] = v
    return '.'.join(abc)


if __name__ == "__main__":
    # extract current version number
    toml_file = here.here("pyproject.toml")
    with open(toml_file, "r") as f:
        lines = f.readlines()

    v_str = ''
    line_idx = None
    for i, line in enumerate(lines):
        if line.startswith("version = "):
            v_str += line.split("=")[-1].strip().strip("\"'")
            line_idx = i
            break

    if line_idx is None:
        raise SystemExit("ERROR: No 'version = x.x.x' line in pyproject.toml")

    # increment new version
    new_ver = format_new_ver(v_str, v_num)
    lines[line_idx] = 'version = "' + new_ver + '"\n'
    do = input(
        "Incrementing version from " + v_str + " to " + new_ver
        + ". Continue? [y/n]: "
    )

    if do.startswith("y"):
        with open(toml_file, "w") as f:
            f.writelines(lines)
    else:
        raise SystemExit("Canceling deployment.")
