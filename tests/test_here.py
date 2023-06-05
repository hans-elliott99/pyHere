import os
import shutil
import random
from pathlib import Path
from therepy import Here
from therepy.here import _join
from therepy.here import _find_file
from therepy.here import _from_cwd

top = "." if Path.cwd().as_posix().split("/")[-1] == "tests" else "tests"
TMP_DIR_NAME = top + "/_tmp"
here = Here("therepy")


def _setup(n):
    # Creates some fake files and directories for testing
    os.makedirs(TMP_DIR_NAME, exist_ok=True)
    f = TMP_DIR_NAME + "/" + \
        ''.join(random.choices("abcdefghijklmnopqrstuvwxyz", k=5))
    files = ['' for _ in range(int(n))]
    for i in range(int(n)):
        files[i] = f + str(i)
        if i % 2 == 0:
            open(files[i], "w").close()
        else:
            os.mkdir(files[i])
        assert os.path.exists(files[i]), "During setup, failed to make file"
    return files


def test_abspath():
    # here.Here.__abspath(*relative_path)
    ap = here._Here__abspath

    def ap_true(x):
        return (Path.cwd() / x)

    error_msg = "Error parsing the absolute path from provided relative path."

    assert ap("./test/") == ap_true("test"), error_msg
    assert ap(".\\test\\") == ap_true("test"), error_msg
    assert ap("test", "that") == ap_true("test/that"), error_msg
    assert ap(Path("test"), Path("that")) == ap_true("test/that"), error_msg
    assert ap(Path("./test")) == ap_true("./test")
    assert ap(Path(".\\test")) == ap_true("./test")


def test_join():
    # therepy.here._join(paths)
    paths = [Path(ch) for ch in "abcd"]
    assert _join(paths) == Path("a/b/c/d")


def test_find_file():
    # therepy.here._find_file(file, dir)
    # file found:
    home = Path(Path.cwd().as_posix().split("therepy")[0] + "/therepy")
    assert _find_file("*.toml", Path.cwd()) == home, "_find_file failed"
    assert _find_file("src", Path.cwd()) == home, "_find_file_ failed"
    # file not found
    try:
        _find_file("_not_a_real_file_", Path.cwd())
        raise AssertionError("_find_file_ failed")
    except FileNotFoundError:
        pass


def test_from_cwd():
    # therepy.here._from_cwd(top, cwd, skip)
    # basic:
    home = Path(Path.cwd().as_posix().split("therepy")[0] + "/therepy")
    cwd = Path.cwd().as_posix().split("/")
    assert _from_cwd("therepy", cwd, 0) == home, "_from_cwd failed basic test"
    # cwd has multiple occurences of the root dir, and so skip is specified
    cwd += ["therepy"]
    assert _from_cwd("therepy", cwd, 1) == home, "_from_cwd failed for skip=1"
    cwd += ["therepy"]
    assert _from_cwd("therepy", cwd, 2) == home, "_from_cwd failed for skip=2"
    # ensure it fails correctly
    try:
        _from_cwd("therepy", cwd, 3)
        raise AssertionError(
                "_from_cwd should raise ValueError when over-skipping.")
    except ValueError:
        pass


def test_Here_init():
    home = Path(Path.cwd().as_posix().split("therepy")[0] + "/therepy")
    h = Here("therepy")
    assert h.here() == home, "basic directory pointing failed"

    h = Here(".venv")
    assert h.here() == home, "basic file finding did not work"

    h = Here("*.git", as_str=True)
    assert h.here() == home.as_posix()


def test_here():
    # here.Here.here
    files = _setup(2)
    for i, file in enumerate(files):
        f = file.split("/")[-1]
        truth = Path.cwd() / "tests" / f
        assert here.here("tests", f) == truth, "Relative path not found."


def test_atexit():
    # pytest runs all fns w/ 'test_' prefix, so we want cleanup to run last
    shutil.rmtree(TMP_DIR_NAME)
