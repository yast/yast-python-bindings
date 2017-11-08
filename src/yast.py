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

def BarGraph(*args):
    """Horizontal bar graph (optional widget)

    Synopsis
    BarGraph (	list values , list labels );
 
    Parameters
    list values  the initial values (integer numbers)

    Optional Arguments
    list labels  the labels for each part; use "%1" to include the current numeric value. May include newlines.
    """
    return run('BarGraph', *args)

def BusyIndicator(*args):
    """Graphical busy indicator

    Synopsis
    BusyIndicator (	string label , integer timeout );
 
    Parameters
    string label  the label describing the bar

    Optional Arguments
    integer timeout  the timeout in milliseconds until busy indicator changes to stalled state, 1000ms by default
    """
    return run('BusyIndicator', *args)

def ButtonBox(*args):
    """Layout for push buttons that takes button order into account

    Synopsis
    ButtonBox ( term button1, term button2 );

    Parameters
    term buttons  list of PushButton items

    """
    return run('ButtonBox', *args)

def CheckBox(*args):
    """Clickable on/off toggle button

    Synopsis
    CheckBox (	string label , boolean|nil checked );
 
    Parameters
    string label  the text describing the check box

    Options
    boldFont  use a bold font

    Optional Arguments
    boolean|nil checked  whether the check box should start checked -
        nil means tristate condition, i.e. neither on nor off
    """
    return run('CheckBox', *args)

def CheckBoxFrame(*args):
    """Frame with clickable on/off toggle button

    Synopsis
    CheckBoxFrame (	string label , boolean checked , term child );
 
    Parameters
    string label  the text describing the check box
    boolean checked  whether the check box should start checked
    term child  the child widgets for frame content - typically `VBox(...) or `HBox(...)

    Options
    noAutoEnable  do not enable/disable frame children upon status change
    invertAutoAnable  disable frame children if check box is checked
    """
    return run('CheckBoxFrame', *args)

def ComboBox(*args):
    """drop-down list selection (optionally editable)

    Synopsis
    ComboBox ( string label, list items );

    Parameters
    string label

    Options
    editable  the user can enter any value.

    Optional Arguments
    list items  the items contained in the combo box

    """
    return run('ComboBox', *args)

def DateField(*args):
    """Date input field

    Synopsis
    DateField (	string label , string initialDate );

    Parameters
    string label

    Optional Arguments
    string initialDate
    """
    return run('DateField', *args)

def DownloadProgress(*args):
    """Self-polling file growth progress indicator (optional widget)

    Synopsis
    DownloadProgress (	string label , string filename , integer expectedSize );
 
    Parameters
    string label  label above the indicator
    string filename  file name with full path of the file to poll
    integer expectedSize  expected final size of the file in bytes
    """
    return run('DownloadProgress', *args)

def DumbTab(*args):
    """Simplistic tab widget that behaves like push buttons

    Synopsis
    DumbTab ( list tabs , term contents );

    Parameters
    list tabs  page headers
    term contents  page contents - usually a ReplacePoint
    """
    return run('DumbTab', *args)

def Empty(*args):
    """Placeholder widget

    Synopsis
    Empty (	void);
    """
    return run('Empty', *args)

def Frame(*args):
    """Frame with label

    Synopsis
    Frame ( string label, term child );

    Parameters
    string label  title to be displayed on the top left edge
    term child  the contained child widget

    """
    return run('Frame', *args)

def Graph(*args):
    """graph

    Synopsis
    Graph (	void);
    """
    return run('Graph', *args)

def HBox(*args):
    """Generic layout: Arrange widgets horizontally

    Synopsis
    HBox ( children... );

    Optional Arguments
    list children  children widgets

    """
    return run('HBox', *args)

def VBox(*args):
    """Generic layout: Arrange widgets vertically

    Synopsis
    VBox ( children... );

    Optional Arguments
    list children  children widgets

    """
    return run('VBox', *args)

def HSpacing(*args):
    """Fixed size empty space for layout

    Synopsis
    HSpacing ( integer|float size );

    Optional Arguments
    integer|float size

    """
    return run('HSpacing', *args)

def VSpacing(*args):
    """Fixed size empty space for layout

    Synopsis
    VSpacing ( integer|float size );

    Optional Arguments
    integer|float size

    """
    return run('VSpacing', *args)

def HStretch(*args):
    """Fixed size empty space for layout

    Synopsis
    HStretch ( integer|float size );

    Optional Arguments
    integer|float size

    """
    return run('HStretch', *args)

def VStretch(*args):
    """Fixed size empty space for layout

    Synopsis
    VStretch ( integer|float size );

    Optional Arguments
    integer|float size

    """
    return run('VStretch', *args)

def HSquash(*args):
    """Layout aid: Minimize widget to its preferred size

    Synopsis
    HSquash (	term child );

    Parameters
    term child  the child widget
    """
    return run('HSquash', *args)

def VSquash(*args):
    """Layout aid: Minimize widget to its preferred size

    Synopsis
    VSquash (   term child );

    Parameters
    term child  the child widget
    """
    return run('VSquash', *args)

def HVSquash(*args):
    """Layout aid: Minimize widget to its preferred size

    Synopsis
    HVSquash (   term child );

    Parameters
    term child  the child widget
    """
    return run('HVSquash', *args)

def HWeight(*args):
    """Control relative size of layouts

    Synopsis
    HWeight ( integer weight, term child );

    Parameters
    integer weight  the new weight of the child widget
    term child  the child widget

    """
    return run('HWeight', *args)

def VWeight(*args):
    """Control relative size of layouts

    Synopsis
    VWeight ( integer weight, term child );

    Parameters
    integer weight  the new weight of the child widget
    term child  the child widget

    """
    return run('VWeight', *args)

def Image(*args):
    """Pixmap image

    Synopsis
    Image (	string imageFileName );
 
    Parameters
    string imageFileName  file name (with path) of the image to display

    Options
    animated  show an animated image (MNG, animated GIF)
    scaleToFit  scale the pixmap so it fits the available space: zoom in or out as needed
    zeroWidth  make widget report a preferred width of 0
    zeroHeight  make widget report a preferred height of 0
    """
    return run('Image', *args)

def InputField(*args):
    """Input field

    Synopsis
    InputField ( string label, string defaulttext );

    Parameters
    string label  the label describing the meaning of the entry

    Options
    shrinkable  make the input field very small

    Optional Arguments
    string defaulttext  The text contained in the text entry

    """
    return run('InputField', *args)

def TextEntry(*args):
    """Input field

    Synopsis
    TextEntry ( string label, string defaulttext );

    Parameters
    string label  the label describing the meaning of the entry

    Options
    shrinkable  make the input field very small

    Optional Arguments
    string defaulttext  The text contained in the text entry

    """
    return run('TextEntry', *args)

def Password(*args):
    """Input field

    Synopsis
    Password ( string label, string defaulttext );

    Parameters
    string label  the label describing the meaning of the entry

    Options
    shrinkable  make the input field very small

    Optional Arguments
    string defaulttext  The text contained in the text entry

    """
    return run('Password', *args)

def IntField(*args):
    """Numeric limited range input field

    Synopsis
    IntField (	string label , integer minValue , integer maxValue , integer initialValue );
 
    Parameters
    string label  Explanatory label above the input field
    integer minValue  minimum value
    integer maxValue  maximum value
    integer initialValue  initial value
    """
    return run('IntField', *args)

def Label(*args):
    """Simple static text

    Synopsis
    Label ( string label );

    Parameters
    string label

    Options
    outputField  make the label look like an input field in read-only mode
    boldFont  use a bold font

    """
    return run('Label', *args)

def Heading(*args):
    """Simple static text

    Synopsis
    Heading ( string label );

    Parameters
    string label

    Options
    outputField  make the label look like an input field in read-only mode
    boldFont  use a bold font

    """
    return run('Heading', *args)

def Left(*args):
    """Layout alignment

    Synopsis
    Left ( term child, string pixmap );

    Parameters
    term child  The contained child widget

    Optional Arguments
    background pixmap

    """
    return run('Left', *args)

def Right(*args):
    """Layout alignment

    Synopsis
    Right ( term child, string pixmap );

    Parameters
    term child  The contained child widget

    Optional Arguments
    background pixmap

    """
    return run('Right', *args)

def Top(*args):
    """Layout alignment

    Synopsis
    Top ( term child, string pixmap );

    Parameters
    term child  The contained child widget

    Optional Arguments
    background pixmap

    """
    return run('Top', *args)

def Bottom(*args):
    """Layout alignment

    Synopsis
    Bottom ( term child, string pixmap );

    Parameters
    term child  The contained child widget

    Optional Arguments
    background pixmap

    """
    return run('Bottom', *args)

def HCenter(*args):
    """Layout alignment

    Synopsis
    HCenter ( term child, string pixmap );

    Parameters
    term child  The contained child widget

    Optional Arguments
    background pixmap

    """
    return run('HCenter', *args)

def VCenter(*args):
    """Layout alignment

    Synopsis
    VCenter ( term child, string pixmap );

    Parameters
    term child  The contained child widget

    Optional Arguments
    background pixmap

    """
    return run('VCenter', *args)

def HVCenter(*args):
    """Layout alignment

    Synopsis
    HVCenter ( term child, string pixmap );

    Parameters
    term child  The contained child widget

    Optional Arguments
    background pixmap

    """
    return run('HVCenter', *args)

def LogView(*args):
    """scrollable log lines like "tail -f"

    Synopsis
    LogView (	string label , integer visibleLines , integer maxLines );

    Parameters
    string label  (above the log lines)
    integer visibleLines  number of visible lines (without scrolling)
    integer maxLines  number of log lines to store (use 0 for "all")
    """
    return run('LogView', *args)

def MarginBox(*args):
    """Margins around one child widget

    Synopsis
    MarginBox (	float horMargin , float vertMargin , term child );
 
    Parameters
    float horMargin  margin left and right of the child widget
    float vertMargin  margin above and below the child widget
    term child  The contained child widget
    """
    return run('MarginBox', *args)

def MenuButton(*args):
    """Button with popup menu

    Synopsis
    MenuButton (	string label , itemList menu );
 
    Parameters
    string label
    itemList menu  items
    """
    return run('MenuButton', *args)

def MinWidth(*args):
    """Layout minimum size

    Synopsis
    MinWidth ( float|integer size, term child );

    Parameters
    float|integer size  minimum width
    term child  The contained child widget

    """
    return run('MinWidth', *args)

def MinHeight(*args):
    """Layout minimum size

    Synopsis
    MinHeight ( float|integer size, term child );

    Parameters
    float|integer size  minimum heigh
    term child  The contained child widget

    """
    return run('MinHeight', *args)

def MinSize(*args):
    """Layout minimum size

    Synopsis
    MinSize ( float|integer width, float|integer height, term child );

    Parameters
    float|integer size  minimum width
    float|integer size  minimum height
    term child  The contained child widget

    """
    return run('MinSize', *args)

def MultiLineEdit(*args):
    """multiple line text edit field

    Synopsis
    MultiLineEdit (	string label , string initialValue );
 
    Parameters
    string label  label above the field

    Optional Arguments
    string initialValue  the initial contents of the field
    """
    return run('MultiLineEdit', *args)

def MultiSelectionBox(*args):
    """Selection box that allows selecton of multiple items

    Synopsis
    MultiSelectionBox (	string label , list items );

    Parameters
    string label

    Options
    shrinkable  make the widget very small

    Optional Arguments
    list items  the items initially contained in the selection box
    """
    return run('MultiSelectionBox', *args)

def PackageSelector(*args):
    """Complete software package selection

    Synopsis
    PackageSelector (	void);	 
 
    Options
    youMode  start in YOU (YaST Online Update) mode
    updateMode  start in update mode
    searchMode  start with the "search" filter view
    summaryMode  start with the "installation summary" filter view
    repoMode  start with the "repositories" filter view
    repoMgr  enable "Repository Manager" menu item
    confirmUnsupported  user has to confirm all unsupported (non-L3) packages

    Optional Arguments
    string floppyDevice
    """
    return run('PackageSelector', *args)

def PartitionSplitter(*args):
    """Hard disk partition splitter tool (optional widget)

    Synopsis
    PartitionSplitter (	integer usedSize ,
 	    integer totalFreeSize ,
     	integer newPartSize ,
 	    integer minNewPartSize ,
     	integer minFreeSize ,
 	    string usedLabel ,
     	string freeLabel ,
 	    string newPartLabel ,
     	string freeFieldLabel ,
 	    string newPartFieldLabel );
 
    Parameters
    integer usedSize  size of the used part of the partition
    integer totalFreeSize  total size of the free part of the partition
        (before the split)
    integer newPartSize  suggested size of the new partition
    integer minNewPartSize  minimum size of the new partition
    integer minFreeSize  minimum free size of the old partition
    string usedLabel  BarGraph label for the used part of the old partition
    string freeLabel  BarGraph label for the free part of the old partition
    string newPartLabel  BarGraph label for the new partition
    string freeFieldLabel  label for the remaining free space field
    string newPartFieldLabel  label for the new size field
    """
    return run('PartitionSplitter', *args)

def PatternSelector(*args):
    """High-level widget to select software patterns (selections)

    Synopsis
    PatternSelector (	void);
    """
    return run('PatternSelector', *args)

def ProgressBar(*args):
    """Graphical progress indicator

    Synopsis
    ProgressBar (	string label , integer maxvalue , integer progress );

    Parameters
    string label  the label describing the bar

    Optional Arguments
    integer maxvalue  the maximum value of the bar
    integer progress  the current progress value of the bar
    """
    return run('ProgressBar', *args)

def PushButton(*args):
    """Perform action on click

    Synopsis
    PushButton ( string label );

    Parameters
    string label

    Options
    default  makes this button the dialogs default button
    helpButton  automatically shows topmost `HelpText
    okButton  assign the [OK] role to this button (see ButtonBox)
    cancelButton  assign the [Cancel] role to this button (see ButtonBox)
    applyButton  assign the [Apply] role to this button (see ButtonBox)
    customButton  override any other button role assigned to this button

    """
    return run('PushButton', *args)

def RadioButton(*args):
    """Clickable on/off toggle button for radio boxes

    Synopsis
    RadioButton (	string label , boolean selected );

    Parameters
    string label

    Options
    boldFont  use a bold font

    Optional Arguments
    boolean selected
    """
    return run('RadioButton', *args)

def RadioButtonGroup(*args):
    """Radio box - select one of many radio buttons

    Synopsis
    RadioButtonGroup (	term child );
 
    Parameters
    term child  the child widget
    """
    return run('RadioButtonGroup', *args)

def ReplacePoint(*args):
    """Pseudo widget to replace parts of a dialog

    Synopsis
    ReplacePoint ( term child );

    Parameters
    term child  the child widget
    """
    return run('ReplacePoint', *args)

def RichText(*args):
    """Static text with HTML-like formatting

    Synopsis
    RichText ( string text );

    Parameters
    string text

    Options
    plainText  don't interpret text as HTML
    autoScrollDown  automatically scroll down for each text change
    shrinkable  make the widget very small

    """
    return run('RichText', *args)

def SelectionBox(*args):
    """Scrollable list selection

    Synopsis
    SelectionBox (	string label , list items );
 
    Parameters
    string label

    Options
    shrinkable  make the widget very small
    immediate  make `notify trigger immediately when the selected item changes

    Optional Arguments
    list items  the items contained in the selection box
    """
    return run('SelectionBox', *args)

def SimplePatchSelector(*args):
    """Simplified approach to patch selection

    Synopsis
    SimplePatchSelector (	void);
    """
    return run('SimplePatchSelector', *args)

def Slider(*args):
    """Numeric limited range input (optional widget)

    Synopsis
    Slider (	string label ,
 	    integer minValue ,
     	integer maxValue ,
     	integer initialValue );

    Parameters
    string label  Explanatory label above the slider
    integer minValue  minimum value
    integer maxValue  maximum value
    integer initialValue  initial value
    """
    return run('Slider', *args)

def Table(*args):
    """Multicolumn table widget

    Synopsis
    Table ( term header, list items );

    Parameters
    term header  the headers of the columns

    Optional Arguments
    list items  the items contained in the selection box

    """
    return run('Table', *args)

def Header(*args):
    return run('header', *args)

def Item(*args):
    return run('item', *args)

def TimeField(*args):
    """Time input field

    Synopsis
    TimeField (	string label , string initialTime );

    Parameters
    string label

    Optional Arguments
    string initialTime
    """
    return run('TimeField', *args)

def TimezoneSelector(*args):
    """Timezone selector map

    Synopsis
    TimezoneSelector (	string pixmap , map timezones );

    Parameters
    string pixmap  path to a jpg or png of a world map - with being the middle of the picture
    map timezones  a map of timezones. The map should be between e.g. Europe/London
        and the tooltip to be displayed ("United Kingdom")
    """
    return run('TimezoneSelector', *args)


def Tree(*args):
    """Scrollable tree selection

    Synopsis
    Tree ( string label );

    Parameters
    string label

    Options
    immediate  make `notify trigger immediately when the selected item changes

    Optional Arguments
    itemList items  the items contained in the tree

    """
    return run('Tree', *args)

def VMultiProgressMeter(*args):
    """Progress bar with multiple segments (optional widget)

    Synopsis
    VMultiProgressMeter (	List<integer> maxValues );

    Parameters
    List<integer> maxValues  maximum values
    """
    return run('VMultiProgressMeter', *args)

def HMultiProgressMeter(*args):
    """Progress bar with multiple segments (optional widget)

    Synopsis
    HMultiProgressMeter (   List<integer> maxValues );

    Parameters
    List<integer> maxValues  maximum values
    """
    return run('HMultiProgressMeter', *args)

