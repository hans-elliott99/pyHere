# therepy
A simple [r-lib/here](https://github.com/r-lib/here) for python, to make path management less of a headache.  
For now, available on test-pypi: https://test.pypi.org/project/therepy  
[GitHub](https://github.com/hans-elliott99/therepy)  

## Overview
R's here library uses the .Rproj file to identify the top-level or root directory in an R project, and all filepaths are defined relative to this directory.  
Instead of looking for a specific file or file extension, the `therepy` module has the user define the root directory somewhere ("there", if you will):   

```python
from therepy import Here
here = Here("myproject")
```

The `Here` object allows you to specify filepaths relative to the defined root project directory (in this example, "myproject").  
It converts them to absolute paths so that the user can standardize filepaths across their python project.  
For example, if I have a dataset in a subfolder, "myproject/database/data.csv", and I want to use it in a script, "myproject/analysis/viz.py", I can specify the path like so:  

```python
# -- viz.py -- 
fp = here.here("database", "data.csv")
df = pandas.read_csv(fp)
```

The relative paths are expanded into absolute paths, so `fp` will work regardless of where `viz.py` exists.  

