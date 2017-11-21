import ycpbuiltins
from ycp import Symbol, List, String, Integer, Boolean, Float, Code, Map, Byteblock, Path, Void

from ycp import Term as YCPTerm


def import_module(module):
    from ycp import import_module as ycp_import_module
    if ycp_import_module(module):
        globals()[module] = __import__(module)

import_module('UI')
import_module('Wizard')
import_module('Sequencer')

def run(func, *args):
    from ycp import pyval_to_ycp
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
        'Bottom': False,
        'Cell': False,
        'Center': False,
        'CheckBox': False,
        'CheckBoxFrame': False,
        'ColoredLabel': False,
        'ComboBox': False,
        'DateField': False,
        'DownloadProgress': False,
        'DumbTab': False,
        'Dummy': False,
        'DummySpecialWidget': False,
        'Empty': False,
        'Frame': False,
        'Graph': False,
        'HBox': False,
        'HCenter': False,
        'HMultiProgressMeter': False,
        'HSpacing': False,
        'HSquash': False,
        'HStretch': False,
        'HVCenter': False,
        'HVSquash': False,
        'HVStretch': False,
        'HWeight': False,
        'Heading': False,
        'IconButton': False,
        'Image': False,
        'InputField': False,
        'IntField': False,
        'Label': False,
        'Left': False,
        'LogView': False,
        'MarginBox': False,
        'MenuButton': False,
        'MinHeight': False,
        'MinSize': False,
        'MinWidth': False,
        'MultiLineEdit': False,
        'MultiSelectionBox': False,
        'PackageSelector': False,
        'PatternSelector': False,
        'PartitionSplitter': False,
        'Password': False,
        'PkgSpecial': False,
        'ProgressBar': False,
        'PushButton': False,
        'RadioButton': False,
        'RadioButtonGroup' : False,
        'ReplacePoint': False,
        'RichText': False,
        'Right': False,
        'SelectionBox': False,
        'Slider': False,
        'Table': False,
        'TextEntry': False,
        'TimeField': False,
        'TimezoneSelector': False,
        'Top': False,
        'Tree': False,
        'VBox': False,
        'VCenter': False,
        'VMultiProgressMeter': False,
        'VSpacing': False,
        'VSquash': False,
        'VStretch': False,
        'VWeight': False,
        'SimplePatchSelector' : False,
        # special cases
        'Header' : True,
        'Item' : True,
       }

for func in meta_funcs.keys():
    setattr(current_module, func, meta_func_creator(func, meta_funcs[func]))

def Term(*args):
    args_list = []
    for item in args:
        args_list.append(item)
    name = args_list.pop(0)
    l = None
    if len(args_list):
      l = List()
      for item in args_list:
          l = ycpbuiltins.add(l, item)
    if l is not None:
        return YCPTerm(name, l)
    return YCPTerm(name)

def Opt(*args):
    l = List()
    for arg in args:
        l.add(Symbol(arg))
    return YCPTerm("opt", l)

def YCPWizard(*args):
    return run("Wizard", *args)

# Id can take argument other than string
def Id(arg, dont_force_sym = False):
  from ycp import pyval_to_ycp
  l = List()
  if isinstance(arg, str) and not dont_force_sym:
      l.add(Symbol(arg))
  else:
      l.add(pyval_to_ycp(arg))
  return YCPTerm("id", l)

