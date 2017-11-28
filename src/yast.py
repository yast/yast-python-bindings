import ycpbuiltins
from ycp import Symbol, List, String, Integer, Boolean, Float, Code, Map, Byteblock, Path, Void

def import_module(module):
    from ycp import import_module as ycp_import_module
    if ycp_import_module(module):
        globals()[module] = __import__(module)

def SCR_Run(func, *args):
    from ycp import _SCR_Run, pyval_to_ycp
    l = List()
    for item in args:
        l.push_back(pyval_to_ycp(item))
    return _SCR_Run('SCR::'+func, l)

scr_meta_funcs = [
    'Read',
    'Write',
    'Execute',
    'Dir',
    'Error',
    'RegisterAgent',
    'RegisterNewAgents',
    'UnregisterAgent',
    'UnregisterAllAgents',
    'UnmountAgent',
]

class SCR:
    pass

def scr_meta_func_creator(func):
    return staticmethod(lambda *args : SCR_Run(func, *args))

for func in scr_meta_funcs:
    setattr(SCR, func, scr_meta_func_creator(func))

def run(func, *args):
    from ycp import pyval_to_ycp
    from ycp import Term as YCPTerm
    l = List()
    for item in args:
        l.push_back(pyval_to_ycp(item))
    return YCPTerm(func, l)

def meta_func_creator(func, lowercase):
    if lowercase:
        func = func.lower()
    return (lambda *args : run(func, *args))

current_module = __import__(__name__)
meta_funcs = {
        'BarGraph': False,
        'BusyIndicator': False,
        'ButtonBox': False,
        'CheckBox': False,
        'CheckBoxFrame': False,
        'ComboBox': False,
        'DateField': False,
        'DownloadProgress': False,
        'DumbTab': False,
        'Empty': False,
        'Graph': False,
        'Frame': False,
        'HBox': False,
        'VBox': False,
        'HSpacing': False,
        'VSpacing': False,
        'HStretch': False,
        'VStretch': False,
        'HSquash': False,
        'VSquash': False,
        'HVSquash': False,
        'HWeight': False,
        'VWeight': False,
        'Image': False,
        'InputField': False,
        'TextEntry': False,
        'Password': False,
        'IntField': False,
        'Label': False,
        'Heading': False,
        'Left': False,
        'Right': False,
        'Top': False,
        'Bottom': False,
        'HCenter': False,
        'VCenter': False,
        'HVCenter': False,
        'LogView': False,
        'MarginBox': False,
        'MenuButton': False,
        'MinWidth': False,
        'MinHeight': False,
        'MinSize': False,
        'MultiLineEdit': False,
        'MultiSelectionBox': False,
        'PackageSelector': False,
        'PartitionSplitter': False,
        'PatternSelector': False,
        'ProgressBar': False,
        'PushButton': False,
        'RadioButton': False,
        'RadioButtonGroup' : False,
        'ReplacePoint': False,
        'RichText': False,
        'SelectionBox': False,
        'SimplePatchSelector' : False,
        'Slider': False,
        'Table': False,
        'Header' : True,
        'Item' : True,
        'TimeField': False,
        'TimezoneSelector': False,
        'Tree': False,
        'VMultiProgressMeter': False,
        'HMultiProgressMeter': False,
        'Cell': False,
        'Center': False,
        'ColoredLabel': False,
        'Dummy': False,
        'DummySpecialWidget': False,
        'HVStretch': False,
        'IconButton': False,
        'PkgSpecial': False,
        'Wizard': False,
       }

for func in meta_funcs.keys():
    setattr(current_module, func, meta_func_creator(func, meta_funcs[func]))

del scr_meta_funcs, scr_meta_func_creator, meta_func_creator, current_module, meta_funcs, func

def Term(*args):
    from ycp import Term as YCPTerm
    name = args[0]
    if len(args) > 1:
        l = List()
        for item in args[1:]:
            l.add(item)
    if l is not None:
        return YCPTerm(name, l)
    return YCPTerm(name)

def Opt(*args):
    from ycp import Term as YCPTerm
    l = List()
    for arg in args:
        l.add(Symbol(arg))
    return YCPTerm("opt", l)

# Id can take argument other than string
def Id(arg, dont_force_sym = False):
    from ycp import pyval_to_ycp
    from ycp import Term as YCPTerm
    l = List()
    if isinstance(arg, str) and not dont_force_sym:
        l.add(Symbol(arg))
    else:
        l.add(pyval_to_ycp(arg))
    return YCPTerm("id", l)

