import sys
import warnings

if sys.version_info[0] == 2:
    from pathlib2 import Path
else:
    from pathlib import Path


def _join(paths):
    p = paths[0]
    for f in paths[1:]:
        p /= f
    return p


def _update_config(a, b):
    if b:
        all_keys = a.keys()
        for key in b.keys():
            if key not in all_keys:
                warnings.warn(
                    f"Provide kwarg, {key}, is not valid and will be ignored.",
                    category=UserWarning)
            else:
                a[key] = b[key]
    return a


class Here:
    """Simplify filepath management throughout your project.
    Create an instance of Here and specify the name of the root directory so
    that Here knows where your project starts.
    Use Here.here("path/from/inside/root") to get the absolute path to a file
    or folder inside your root directory.
    therepy.Here is built on python's pathlib module, and can be set to return
    pathlib.Path instances instead of strings.

    Parameters
    ----------
    project_dir : str
        The name of the root directory for your project.
    **kwargs : dict, optional
        Default parameters, such as the return type, can be set at
        initialization. Refer to documentation for a list of all possible
        arguments.


    Examples
    --------
    >>> from therepy import Here
    >>> here = Here(project_dir = "my_project")
    >>> here.here("folder_1/dataset1.csv")
    "C:/users/ExampleUser/Documents/my_project/folder_1/dataset1.csv"

    By default, Here.here returns strings. That behavior can be overwritten at
    initialization or in downstream methods.

    >>> here = Here("my_project", as_path = True)
    >>> here.here()
    WindowsPath("C:/users/ExampleUser/Documents/my_project")
    >>> here.here("my_project", as_str = True)
    "C:/users/ExampleUser/Documents/my_project"
    """

    def __init__(self, project_dir, **kwargs):
        top = Path(project_dir).as_posix()
        cwd = Path().cwd().as_posix().split("/")
        assert top in cwd, \
            "Project directory not found in working path. " + \
            "Ensure that 'project_dir' is an existing parent directory on " + \
            "your system."
        self.root = Path('/'.join(cwd[0:cwd.index(top) + 1]))
        self.config = _update_config(self._init_config(), kwargs)

    def _init_config(self):
        return {"as_str": True,
                "as_path": False}

    def _resolve_output(self, path, config):
        if config["as_str"]:
            return path.as_posix()
        elif config["as_path"]:
            return path
        else:
            warnings.warn("Args 'as_str' and 'as_path' are both False, "
                          + "defaulting to as_str.",
                          category=UserWarning)
            return path.as_str()

    def _abs_path(self, *rel_pth):
        # Get absolute path to provided relative path w/in project dir
        return self.root / _join([Path(a.replace("\\", "/")) for a in rel_pth])

    def here(self, *relative_path, **kwargs):
        """Get the absolute path to a file/folder within the project directory.

        Parameters
        ----------
        *relative_path : str or tuple of str
            The relative path from the root/project directory to the target
            file or folder. Can be concatenated as one string, or each
            folder/file can be listed separately (as a variable length
            positional). If not provided, the absolute path to the root
            directory will be returned.

        **kwargs : dict, optional
            Default parameters, such as the return type, can be overwritten.
            Refer to documentation for a list of all possible arguments.

        Returns
        -------
        str or pathlib.Path
            The absolute path to the provided relative path.
        """
        if len(relative_path):
            p = self._abs_path(*relative_path)
        else:
            p = self.root
        config = _update_config(self.config, kwargs)
        return self._resolve_output(p, config)

    def exists(self, *relative_path):
        """Check if a file exists within your project directory.
        Simply wraps pathlib.exists, so a user doesn't have to do:
            Here.here("relative/path", as_path=True).exists()

        Parameters
        ----------
        *relative_path : str or tuple of str
            The relative path from the root/project directory to the target
            file or folder. Can be concatenated as one string, or each
            folder/file can be listed separately (as a variable length
            positional). If not provided, the absolute path to the root
            directory will be checked.

        Returns
        -------
        bool
            True if the path exists, False otherwise.
        """
        return self._abs_path(*relative_path).exists()

    def __str__(self):
        return self.root.as_posix()
