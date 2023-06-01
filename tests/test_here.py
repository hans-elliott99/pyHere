import os
import shutil
import random
from pathlib import Path
from therepy import Here

top = "." if Path.cwd().as_posix().split("/")[-1] == "test" else "tests"
TMP_DIR_NAME = top + "/_tmp"
here = Here("therepy")


def _setup(n):
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
    files = _setup(2)
    for i, file in enumerate(files):
        f = file.split("/")[-1]
        truth = Path.cwd().joinpath("tests").joinpath(f).as_posix()
        assert here.here("tests", f) == truth, "Relative path not found."


def test_exists():
    files = _setup(2)
    for i, file in enumerate(files):
        if i % 2 == 0:
            assert here.exists(file) is True
        else:
            assert here.exists(file + '1') is False


def test_abspath():

    ap = here._abs_path

    def ap_true(x):
        return (Path.cwd() / x)

    error_msg = "Error parsing the absolute path from provided relative path."

    assert ap("./test/") == ap_true("test"), error_msg
    assert ap(".\\test\\") == ap_true("test"), error_msg
    assert ap("test", "that") == ap_true("test/that"), error_msg


def test_atexit():
    # pytest runs all fns w/ 'test_' prefix, so we want cleanup to run last
    shutil.rmtree(TMP_DIR_NAME)
