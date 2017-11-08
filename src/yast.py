from ycp import YCPSymbol as Symbol
from ycp import YCPList as List
from ycp import YCPString as String
from ycp import YCPTerm as Term
from ycp import YCPInteger as Integer
from ycp import YCPBoolean as Boolean
from ycp import YCPFloat as Float
from ycp import YCPCode as Code
from ycp import YCPMap as Map
from ycp import Id, Opt

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
    return Term(func, l)

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
