import os
import shutil
import random
import warnings
from pathlib import Path
from therepy import Here
from therepy.here import _join
from therepy.here import _update_config

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


def test_here():
    # here.Here.here
    files = _setup(2)
    for i, file in enumerate(files):
        f = file.split("/")[-1]
        truth = Path.cwd().joinpath("tests").joinpath(f).as_posix()
        assert here.here("tests", f) == truth, "Relative path not found."


def test_exists():
    # here.Here.exists
    files = _setup(2)
    for i, file in enumerate(files):
        assert here.exists(file) is True
        assert here.exists(file + '1') is False


def test_abspath():
    # here.Here.__abspath(*relative_path)
    ap = here._Here__abspath

    def ap_true(x):
        return (Path.cwd() / x)

    error_msg = "Error parsing the absolute path from provided relative path."

    assert ap("./test/") == ap_true("test"), error_msg
    assert ap(".\\test\\") == ap_true("test"), error_msg
    assert ap("test", "that") == ap_true("test/that"), error_msg


def test_update_config():
    # therepy.here._update_config(a, b)
    a = {"a": 1, "b": 2, "c": 3}
    b = {"a": 9, "b": 9, "d": 1}

    with warnings.catch_warnings(record=True) as w:
        c = _update_config(a, b)
        msg = w  # warning message that key 'd' is unused

    assert a == {"a": 1, "b": 2, "c": 3}, "Source dict was modified."
    assert b == {"a": 9, "b": 9, "d": 1}, "Updater dict was modified."
    assert c == {"a": 9, "b": 9, "c": 3}, "New dict is incorrect."
    assert len(msg) == 1, f"1 warning expected but {len(msg)} recorded."


def test_join():
    # therepy.here._join(paths)
    paths = [Path(ch) for ch in "abcd"]
    assert _join(paths) == Path("a/b/c/d")


def test_atexit():
    # pytest runs all fns w/ 'test_' prefix, so we want cleanup to run last
    shutil.rmtree(TMP_DIR_NAME)
