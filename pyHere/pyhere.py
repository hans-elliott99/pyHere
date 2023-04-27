from pathlib import Path



class Here:
    """Simplify filepath management throughout your project.

    To use pyHere create an instance of Here and specify the name of the root 
    directory so that Here knows where your project starts.  
    Use Here.here("path/from/inside/root") to get the absolute path to a file or 
    folder inside your root directory.  
    pyHere.Here is built ontop of python's pathlib module, and by default it 
    will return pathlib.Path instances.

    :param project_dir: The name of the root directory for your project.
    :type project_dir: str

    Example usage:

    .. code-block:: python
        >>> here = Here(project_dir = "my_project")
        >>> here.here("folder_1/dataset1.csv")
        WindowsPath("C:/users/ExampleUser/Documents/my_project/folder_1/dataset1.csv")
        >>> here.here("folder_2/dataset2.csv", as_string=True)
        "C:/users/ExampleUser/Documents/my_project/folder_2/dataset2.csv"
    """

    def __init__(self, project_dir:str) -> None:
        top = str(project_dir).replace("\\", "/").replace("/", "").lstrip(".")
        cwd = Path().cwd().as_posix().split("/")
        assert top in cwd, \
            "Top directory not found in working path. Ensure that 'top_directory' is an existing directory."
        pth = []
        i = 0
        while (cwd[i] != top):
            pth.append(cwd[i]) 
            i += 1
        pth.append(top)
        self.root = Path("/".join(pth))
    
    def here(self, path:str, as_string=False):
        """Get the absolute path to the target file or folder within your project directory.

        :param target: the relative path from the project directory to the target folder or file.
        :param type: str
        :param as_string: Default False. If True, return the path as a string and not as a pathlib.Path instance.
        :param type: bool
        :return: The absolute path to the provide path.
        """
        if not as_string:
            return self.root / Path(str(path)) 
        else:
            return (self.root / Path(str(path))).as_posix()
    
    def __str__(self) -> str:
        return self.root.as_posix()
    
    
    