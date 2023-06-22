# therepy
[![Documentation Status](https://readthedocs.org/projects/therepy/badge/?version=latest)](https://therepy.readthedocs.io/en/latest/?badge=latest)
[<img alt="GitHub" width="30px" src="https://raw.githubusercontent.com/edent/SuperTinyIcons/master/images/png/github.png" />](https://github.com/hans-elliott99/therepy)

A simple [r-lib/here](https://github.com/r-lib/here) for python, to make file path management less of a headache in project-oriented workflows.  

## Installation
```bash
pip install therepy
```

[See pypi for details](https://pypi.org/project/therepy/)

## Overview
R's here library uses the .Rproj file to identify the top-level or root directory in an R project, and all file paths are defined relative to this directory.  
Instead of looking for a specific file or file extension, the `therepy` module has the user define the root directory somewhere ("there", if you will):   

```python
from therepy import Here
here = Here("myproj")
```

Once initialized, the `Here` object allows you to specify file paths relative to the defined root directory (in this example, "myproj"), since it coverts them to absolute paths under the hood.  
For example, if I have a dataset in a subfolder, "myproj/database/data.csv", and I want to use it in a script, "myproj/analysis/viz.py", I can specify the path like so:  

```python
# -- viz.py -- 
fp = here.here("database", "data.csv")
print(fp)
#> PosixPath("/home/user/Documents/myproj/database/data.csv")
df = read_csv(fp)
```
The relative paths are expanded into absolute paths, so the returned file path will work even if "viz.py" gets moved around.

If you do not want to use your project's folder name to initialize `Here`, you can provide the name of a file that exists in your project's root or a [glob style expression](https://docs.python.org/3/library/glob.html) identifying such a file:  

```python
here = Here(".git")
here = Here("*.Rproj")
```

Here is built on [pathlib](https://docs.python.org/3/library/pathlib.html) and returns pathlib.Path instances by default (a PosixPath or WindowsPath depending on your system).  
This allows you to take advantage of pathlib's great features, like:  

```python
here = Here("myproj")
fp = here.here("database/data.csv")
if fp.exists():
    ... 
```

And since pathlib can resolve and join paths, you can easily define folders for reading and writing to:

```python
here = Here("myproj")
outputs = here.here("outputs")
print(outputs)
#> PosixPath("/home/user/Documents/myproj/outputs")
...

df.to_csv(here.here(outputs, "data.csv"))
```

`Here` will return strings if you ask it too:
```python
here = Here("myproj")
print(here.here(as_str=True))
#> "/home/user/Documents/myproj"
```

