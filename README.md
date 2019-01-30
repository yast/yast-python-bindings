# YaST - The Python Bindings #

[![Travis Build](https://travis-ci.org/yast/yast-python-bindings.svg?branch=master)](https://travis-ci.org/yast/yast-python-bindings)
[![Jenkins Build](http://img.shields.io/jenkins/s/https/ci.opensuse.org/yast-yast-python-bindings-master.svg)](https://ci.opensuse.org/view/Yast/job/yast-yast-python-bindings-master/)

The API documentation for the UI can be found [here][api]. For more details,
check the [YaST documentation][doc].

[api]: http://yast-ui-bindings.surge.sh
[doc]: http://yast.opensuse.org/documentation

## Python versions
The yast python bindings will build in both python2 and python3. Suppying the
--enable-python3 option during configure will switch to python3 bindings.

## Calling YaST from Python

### Publish, Import and Include

The connection to the [YaST component system][arch] has two parts.
The first one is the ability
to be called from the component system. *Clients* can be called via WFM
and *modules* provide an interface via the `Declare` decorator, where the type
signature is specified.

[arch]: https://yastgithubio.readthedocs.org/en/latest/architecture/

The second part is calling methods from the component system. *Clients* are called
via WFM. Methods from *modules* are imported with {yast.import_module}, which
loads a component and creates a python object in the Yast namespace from it, on which
exported methods can be called.

#### A simple yast python module (example)
Modules must be installed in one of the YaST2 modules directories:
/y2update/modules; $HOME/.yast2/modules; /usr/share/YaST2/modules

```python
# ~/.yast2/modules/pytest.py
from yast import Declare
@Declare('integer', 'integer', 'integer')
def suma(a, b):
    return a + b
```

#### Calling this module from python

```python
import yast
yast.import_module('pytest')
print(yast.pytest.suma(2, 3))
```

#### Calling this module from ruby

```ruby
require "yast"
Yast.import "pytest"
puts Yast::pytest.suma(2, 3)
```

#### Calling this module from perl

```perl
use YaPI;
YaST::YCP::Import("pytest");
pytest.suma(2, 3);
```

### How to call UI from YaST in Python

```python
# test.py
import yast
yast.import_module('Popup')
yast.Popup.Message('Example text')
```

You must execute UI code using y2base, for example:

```bash
/usr/lib/YaST2/bin/y2base ./test.py ncurses
```


### How to call SCR from python
There are 4 functions for working with SCR SCR.Dir, SCR.Read, SCR.Write
and SCR.Execute. The first argument of a function is a ycp path as string.
e.g. ".target.bash_output"

```python
>>> import yast
>>> yast.SCR.Execute(yast.Path('.target.bash_output'),'pwd')
{'exit': 0, 'stderr': '', 'stdout': '/home/user\n'}
```


### Symbol, Path and Term in python
After importing yast python has 3 classes for building yast type such as
symbol, path or term.

```python
path = Path('.my.path')
symbol = Symbol('Enabled')
term = Term('VBox',Term('Label','&Example Label'), Term('PushButton', '&So What'))
```

### UI Shortcuts
Yast python provides shortcuts for UI terms, which is useful for constructing dialogs.

```python
# usage with Term
content = yast.Term(
  yast.Symbol('ButtonBox'),
  yast.Term(
    yast.Symbol('PushButton'),
    yast.Term(yast.Symbol('id'), yast.Symbol('ok_button')),
    "OK"
  ),
  yast.Term(
    yast.Symbol('PushButton'),
    yast.Term(yast.Symbol('id'), yast.Symbol('cancel_button')),
    "Cancel"
  )
)

# usage with shortcuts
content = ButtonBox(
  PushButton(Id('ok_button'), "OK"),
  PushButton(Id('cancel_button'), "Cancel")
)
```

### Further Information

More information about YaST can be found on its [homepage](http://yast.opensuse.org).

## Packager information

### Build dependencies

Build dependencies include autotools, a c++ compiler, python devel files, swig,
and yast2 build dependencies. For a more detailed list, see the included
spec file.

### How to Compile

Use the latest yast2-devtools, then use these calls:

```bash
make -f Makefile.cvs all
./configure --enable-python3
make
```

### How to Install

Compile it, and from the `build` directory call as root:

```bash
make install
```

