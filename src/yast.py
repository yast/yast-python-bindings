import ycpbuiltins
from ycp import Opt, Symbol, List, String, Integer, Boolean, Float, Code, Map, Byteblock, Path, Void

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

