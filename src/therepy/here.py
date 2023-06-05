import sys
from pathlib import Path


def _join(paths):
    """Join list of pathlib.Paths into one pathlib.Path
    """
    p = paths[0]
    for f in paths[1:]:
        p /= f
    return p


def _from_cwd(top, cwd, skip):
    """Get path to project root from the current working path
    """
    idx = len(cwd) - cwd[::-1].index(top)
    for _ in range(skip):
        try:
            cwd = cwd[0:idx-1]
            idx = len(cwd) - cwd[::-1].index(top)
        except ValueError as e:
            sys.tracebacklimit = 0
            raise ValueError("Directory '" + top
                             + "' not found with skip = " + str(skip)) from e
    return Path('/'.join(cwd[0:idx])).resolve()


def _find_file(file, dir):
    """Get path to the project root from a filename using pathlib.Path.glob
    """
    try:
        _ = next(dir.glob(file))
        return dir
    except StopIteration:
        pass
    dir = (dir / "..").resolve()
    if dir == Path(dir.anchor):
        sys.tracebacklimit = 0
        raise FileNotFoundError(
            "Reached filesystem root and did not find file: " + file
        )
    return _find_file(file, dir)


class Here:
    """Simplify file path management for project-oriented python workflows.
    Create an instance of Here and specify the project's root directory.
    Use Here.here("relative/path/from/root") to get the absolute path to a file
    or folder inside your root directory.
    Here returns instances of pathlib.Path by default, but can be set to return
    strings instead.

    Parameters
    ----------
    pattern : str
        Either the exact name of the root directory for your project or a glob-
        style expression which identifies a file or folder within your root
        directory.
    skip : int, default=0
        The number of occurrences of 'pattern' to skip as the current working
        path is travsersed backwards.
    as_str : bool, default=False
        Sets the default return type for Here.here. If False (the default),
        Here.here returns a pathlib.Path. If True, it just returs a string.
        This can be overwritten by specifying 'as_str' in the Here.here call.

    Examples
    --------
    >>> from therepy import Here
    >>> here = Here("my_project")
    >>> here.here("folder/dataset.csv")
    PosixPath("/home/user/Documents/my_project/folder/dataset.csv")

    You can also declare the root directory by providing the name of a file or
    folder inside of your project's root.

    >>> here = Here(".git")

    Glob style expressions also work for identifying files.

    >>> here = Here("*.Rproj")

    By default, Here.here returns a pathlib.Path. That behavior can be
    overwritten at initialization or in downstream methods.

    >>> here = Here("my_project", as_str=True)
    >>> here.here()
    "/home/user/Documents/my_project"
    >>> here.here("my_project", as_str=False)
    PosixPath("/home/user/Documents/my_project")

    If your pattern occurs multiple times in your working path, you can skip
    to the desired occurrence.

    >>> from pathlib import Path
    >>> Path.cwd()
    PosixPath("/home/user/Documents/module/module")
    >>> here = Here("module", skip=0)
    >>> here.here()
    PosixPath("/home/user/Documents/module/module")
    >>> here = Here("module", skip=1)
    >>> here.here()
    PosixPath("/home/user/Documents/module")
    """

    def __init__(self, pattern, skip=0, as_str=False):
        top = Path(pattern).as_posix()
        cwd = Path.cwd().as_posix().split("/")
        if top in cwd:
            self.root = _from_cwd(top, cwd, skip)
        else:
            self.root = _find_file(pattern, Path.cwd())
        self.as_str = as_str

    def __resolve_pathlib(self, path, as_str):
        if as_str is None:
            as_str = self.as_str
        return path.as_posix() if as_str else path

    def __abspath(self, *rel_pth):
        # Get absolute path to provided relative path w/in project dir
        return (self.root /
                _join([Path(str(a).replace("\\", "/")) for a in rel_pth])
                ).resolve()

    def here(self, *rel_path, as_str=None):
        """Get the absolute path to a file/folder within the project directory.

        Parameters
        ----------
        *rel_path : str or tuple of str
            The relative path from the root/project directory to the target
            file or folder. Can be concatenated as one string, or each
            folder/file can be listed separately (as a variable length
            positional). If not provided, the absolute path to the root
            directory will be returned.

        as_str : bool or None, default=None
            If True, return a string. If False, return a pathlib.Path.
            If None, (the default) Here.here uses the value for 'as_str' set
            at initialization, which itself defaults to False.

        Returns
        -------
        pathlib.Path or str
            The absolute path to the provided relative path.
        """
        p = self.__abspath(*rel_path) if len(rel_path) else self.root
        return self.__resolve_pathlib(p, as_str)

    def __str__(self):
        return self.root.as_posix()
