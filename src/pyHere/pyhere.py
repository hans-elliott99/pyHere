from pathlib import Path

class Here:
    """Simplify filepath management throughout your project.

    To use pyHere create an instance of Here and specify the name of the root 
    directory so that Here knows where your project starts.  
    Use Here.here("path/from/inside/root") to get the absolute path to a file or 
    folder inside your root directory.  
    pyHere.Here is built ontop of python's pathlib module, and can be set to return 
    pathlib.Path instances instead of strings.

    :param project_dir: The name of the root directory for your project.
    :type project_dir: str
    :param as_path: Default False. Sets the default value for as_path in downstream methods. 
        If True, pathlib.Path instances will be returned instead of strings.
    :type as_string: bool

    Example usage:

    .. code-block:: python
        >>> here = Here(project_dir = "my_project")
        >>> here.here("folder_1/dataset1.csv")
        "C:/users/ExampleUser/Documents/my_project/folder_2/dataset2.csv"
        >>> here.here("folder_2/dataset2.csv", as_path=True)
        WindowsPath("C:/users/ExampleUser/Documents/my_project/folder_1/dataset1.csv")
    """

    def __init__(self, project_dir, as_path=False):
        top = str(project_dir).replace("\\", "/").replace("/", "").lstrip(".")            
        cwd = Path().cwd().as_posix().split("/")
        assert top in cwd, \
            "Top directory not found in working path. Ensure that 'top_directory' is an existing directory."
        self.root = Path('/'.join(cwd[0 : cwd.index(top) + 1]))
        self._as_pthlib = as_path

    def here(self, relative_path="", as_path=None):
        """Get the absolute path to a file or folder within your project directory.

        :param relative_path: The relative path from the root/project directory to the target 
            file or folder. If not provided, returns the absolute path to the root directory.
        :param type: Union[str, pathlib.Path]
        :param as_path: Default None. If True, return the path as a pathlib.Path instance. If False, 
            return as a string. If None, use the default value set at initialization, which itself  
            defaults to False (return str).
        :param type: Union[bool, None]
        :return: The absolute path to the provide relative path.
        :rtype: Union[str, pathlib.Path]
        """
        p = self.root / Path(relative_path)
        if as_path is None:
            as_path = self._as_pthlib
        if as_path:
            return p
        else:
            return p.as_posix()
    
    def __str__(self):
        return self.root.as_posix()
