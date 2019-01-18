docs = {}

docs['BarGraph'] = \
    """Horizontal bar graph (optional widget)

    Synopsis
    BarGraph (	list values , list labels );
 
    Parameters
    list values  the initial values (integer numbers)

    Optional Arguments
    list labels  the labels for each part; use "%1" to include the current numeric value. May include newlines.
    """

docs['BusyIndicator'] = \
    """Graphical busy indicator

    Synopsis
    BusyIndicator (	string label , integer timeout );
 
    Parameters
    string label  the label describing the bar

    Optional Arguments
    integer timeout  the timeout in milliseconds until busy indicator changes to stalled state, 1000ms by default
    """

docs['ButtonBox'] = \
    """Layout for push buttons that takes button order into account

    Synopsis
    ButtonBox ( term button1, term button2 );

    Parameters
    term buttons  list of PushButton items

    """

docs['CheckBox'] = \
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

docs['CheckBoxFrame'] = \
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

docs['ComboBox'] = \
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

docs['DateField'] = \
    """Date input field

    Synopsis
    DateField (	string label , string initialDate );

    Parameters
    string label

    Optional Arguments
    string initialDate
    """

docs['DownloadProgress'] = \
    """Self-polling file growth progress indicator (optional widget)

    Synopsis
    DownloadProgress (	string label , string filename , integer expectedSize );
 
    Parameters
    string label  label above the indicator
    string filename  file name with full path of the file to poll
    integer expectedSize  expected final size of the file in bytes
    """

docs['DumbTab'] = \
    """Simplistic tab widget that behaves like push buttons

    Synopsis
    DumbTab ( list tabs , term contents );

    Parameters
    list tabs  page headers
    term contents  page contents - usually a ReplacePoint
    """

docs['Empty'] = \
    """Placeholder widget

    Synopsis
    Empty (	void);
    """

docs['Frame'] = \
    """Frame with label

    Synopsis
    Frame ( string label, term child );

    Parameters
    string label  title to be displayed on the top left edge
    term child  the contained child widget

    """

docs['Graph'] = \
    """graph

    Synopsis
    Graph (	void);
    """

docs['HBox'] = \
    """Generic layout: Arrange widgets horizontally

    Synopsis
    HBox ( children... );

    Optional Arguments
    list children  children widgets

    """

docs['VBox'] = \
    """Generic layout: Arrange widgets vertically

    Synopsis
    VBox ( children... );

    Optional Arguments
    list children  children widgets

    """

docs['HSpacing'] = \
    """Fixed size empty space for layout

    Synopsis
    HSpacing ( integer|float size );

    Optional Arguments
    integer|float size

    """

docs['VSpacing'] = \
    """Fixed size empty space for layout

    Synopsis
    VSpacing ( integer|float size );

    Optional Arguments
    integer|float size

    """

docs['HStretch'] = \
    """Fixed size empty space for layout

    Synopsis
    HStretch ( integer|float size );

    Optional Arguments
    integer|float size

    """

docs['VStretch'] = \
    """Fixed size empty space for layout

    Synopsis
    VStretch ( integer|float size );

    Optional Arguments
    integer|float size

    """

docs['HSquash'] = \
    """Layout aid: Minimize widget to its preferred size

    Synopsis
    HSquash (	term child );

    Parameters
    term child  the child widget
    """

docs['VSquash'] = \
    """Layout aid: Minimize widget to its preferred size

    Synopsis
    VSquash (   term child );

    Parameters
    term child  the child widget
    """

docs['HVSquash'] = \
    """Layout aid: Minimize widget to its preferred size

    Synopsis
    HVSquash (   term child );

    Parameters
    term child  the child widget
    """

docs['HWeight'] = \
    """Control relative size of layouts

    Synopsis
    HWeight ( integer weight, term child );

    Parameters
    integer weight  the new weight of the child widget
    term child  the child widget

    """

docs['VWeight'] = \
    """Control relative size of layouts

    Synopsis
    VWeight ( integer weight, term child );

    Parameters
    integer weight  the new weight of the child widget
    term child  the child widget

    """

docs['Image'] = \
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

docs['InputField'] = \
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

docs['TextEntry'] = \
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

docs['Password'] = \
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

docs['IntField'] = \
    """Numeric limited range input field

    Synopsis
    IntField (	string label , integer minValue , integer maxValue , integer initialValue );
 
    Parameters
    string label  Explanatory label above the input field
    integer minValue  minimum value
    integer maxValue  maximum value
    integer initialValue  initial value
    """

docs['Label'] = \
    """Simple static text

    Synopsis
    Label ( string label );

    Parameters
    string label

    Options
    outputField  make the label look like an input field in read-only mode
    boldFont  use a bold font

    """

docs['Heading'] = \
    """Simple static text

    Synopsis
    Heading ( string label );

    Parameters
    string label

    Options
    outputField  make the label look like an input field in read-only mode
    boldFont  use a bold font

    """

docs['Left'] = \
    """Layout alignment

    Synopsis
    Left ( term child, string pixmap );

    Parameters
    term child  The contained child widget

    Optional Arguments
    background pixmap

    """

docs['Right'] = \
    """Layout alignment

    Synopsis
    Right ( term child, string pixmap );

    Parameters
    term child  The contained child widget

    Optional Arguments
    background pixmap

    """

docs['Top'] = \
    """Layout alignment

    Synopsis
    Top ( term child, string pixmap );

    Parameters
    term child  The contained child widget

    Optional Arguments
    background pixmap

    """

docs['Bottom'] = \
    """Layout alignment

    Synopsis
    Bottom ( term child, string pixmap );

    Parameters
    term child  The contained child widget

    Optional Arguments
    background pixmap

    """

docs['HCenter'] = \
    """Layout alignment

    Synopsis
    HCenter ( term child, string pixmap );

    Parameters
    term child  The contained child widget

    Optional Arguments
    background pixmap

    """

docs['VCenter'] = \
    """Layout alignment

    Synopsis
    VCenter ( term child, string pixmap );

    Parameters
    term child  The contained child widget

    Optional Arguments
    background pixmap

    """

docs['HVCenter'] = \
    """Layout alignment

    Synopsis
    HVCenter ( term child, string pixmap );

    Parameters
    term child  The contained child widget

    Optional Arguments
    background pixmap

    """

docs['LogView'] = \
    """scrollable log lines like "tail -f"

    Synopsis
    LogView (	string label , integer visibleLines , integer maxLines );

    Parameters
    string label  (above the log lines)
    integer visibleLines  number of visible lines (without scrolling)
    integer maxLines  number of log lines to store (use 0 for "all")
    """

docs['MarginBox'] = \
    """Margins around one child widget

    Synopsis
    MarginBox (	float horMargin , float vertMargin , term child );
 
    Parameters
    float horMargin  margin left and right of the child widget
    float vertMargin  margin above and below the child widget
    term child  The contained child widget
    """

docs['MenuButton'] = \
    """Button with popup menu

    Synopsis
    MenuButton (	string label , itemList menu );
 
    Parameters
    string label
    itemList menu  items
    """

docs['MinWidth'] = \
    """Layout minimum size

    Synopsis
    MinWidth ( float|integer size, term child );

    Parameters
    float|integer size  minimum width
    term child  The contained child widget

    """

docs['MinHeight'] = \
    """Layout minimum size

    Synopsis
    MinHeight ( float|integer size, term child );

    Parameters
    float|integer size  minimum heigh
    term child  The contained child widget

    """

docs['MinSize'] = \
    """Layout minimum size

    Synopsis
    MinSize ( float|integer width, float|integer height, term child );

    Parameters
    float|integer size  minimum width
    float|integer size  minimum height
    term child  The contained child widget

    """

docs['MultiLineEdit'] = \
    """multiple line text edit field

    Synopsis
    MultiLineEdit (	string label , string initialValue );
 
    Parameters
    string label  label above the field

    Optional Arguments
    string initialValue  the initial contents of the field
    """

docs['MultiSelectionBox'] = \
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

docs['PackageSelector'] = \
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

docs['PartitionSplitter'] = \
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

docs['PatternSelector'] = \
    """High-level widget to select software patterns (selections)

    Synopsis
    PatternSelector (	void);
    """

docs['ProgressBar'] = \
    """Graphical progress indicator

    Synopsis
    ProgressBar (	string label , integer maxvalue , integer progress );

    Parameters
    string label  the label describing the bar

    Optional Arguments
    integer maxvalue  the maximum value of the bar
    integer progress  the current progress value of the bar
    """

docs['PushButton'] = \
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

docs['RadioButton'] = \
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

docs['RadioButtonGroup'] = \
    """Radio box - select one of many radio buttons

    Synopsis
    RadioButtonGroup (	term child );
 
    Parameters
    term child  the child widget
    """

docs['ReplacePoint'] = \
    """Pseudo widget to replace parts of a dialog

    Synopsis
    ReplacePoint ( term child );

    Parameters
    term child  the child widget
    """

docs['RichText'] = \
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

docs['SelectionBox'] = \
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

docs['SimplePatchSelector'] = \
    """Simplified approach to patch selection

    Synopsis
    SimplePatchSelector (	void);
    """

docs['Slider'] = \
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

docs['Table'] = \
    """Multicolumn table widget

    Synopsis
    Table ( term header, list items );

    Parameters
    term header  the headers of the columns

    Optional Arguments
    list items  the items contained in the selection box

    """

docs['TimeField'] = \
    """Time input field

    Synopsis
    TimeField (	string label , string initialTime );

    Parameters
    string label

    Optional Arguments
    string initialTime
    """

docs['TimezoneSelector'] = \
    """Timezone selector map

    Synopsis
    TimezoneSelector (	string pixmap , map timezones );

    Parameters
    string pixmap  path to a jpg or png of a world map - with being the middle of the picture
    map timezones  a map of timezones. The map should be between e.g. Europe/London
        and the tooltip to be displayed ("United Kingdom")
    """


docs['Tree'] = \
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

docs['VMultiProgressMeter'] = \
    """Progress bar with multiple segments (optional widget)

    Synopsis
    VMultiProgressMeter (	List<integer> maxValues );

    Parameters
    List<integer> maxValues  maximum values
    """

docs['HMultiProgressMeter'] = \
    """Progress bar with multiple segments (optional widget)

    Synopsis
    HMultiProgressMeter (   List<integer> maxValues );

    Parameters
    List<integer> maxValues  maximum values
    """

docs['IconButton'] = \
    """Perform action on click

    Synopsis
    IconButton (	string iconName ,
                    string label );

    Parameters
    string iconName
    string label

    Options
    default  makes this button the dialogs default button
    helpButton  automatically shows topmost `HelpText
    okButton  assign the [OK] role to this button (see ButtonBox)
    cancelButton  assign the [Cancel] role to this button (see ButtonBox)
    applyButton  assign the [Apply] role to this button (see ButtonBox)
    customButton  override any other button role assigned to this button
    """

docs['ColoredLabel'] = \
    """Simple static text with specified background and foreground color

    Synopsis
    ColoredLabel (	string  	label ,
                    color  	foreground ,
                    color  	background ,
                    integer  	margin );

    Parameters
    string label
    color foreground
            color

    color background
            color

    integer margin
            around the widget in pixels

    Options
    boldFont
            use a bold font

    Properties
    string Value
            the label text
    """

scr_docs = {}

scr_docs['Dir'] = \
    """Gets array of all children attached directly below path.

    Synopsis
    Dir(path)

    Parameters
    string path
            sub-path where to search for children

    Returns
    string[]
            list of children names
    """

scr_docs['Error'] = \
    """Gets detailled error description from agent.

    Synopsis
    Error(path)

    Parameters
    string path
            path to agent

    Returns
    hash
            with keys "code" and "summary"
    """

scr_docs['Execute'] = \
    """Executes command

    Synopsis
    Execute(path, *args)

    Parameters
    string path
            path to agent
    args
            additional arguments depending on agent
    """

scr_docs['Read'] = \
    """Reads data

    Synopsis
    Read(path, *args)

    Parameters
    string path
            path that is combination of path where agent is attached and path inside agent
    args
            additional arguments depending on agent, usually optional
    """

scr_docs['RegisterAgent'] = \
    """Register an agent at given path with description

    Synopsis
    RegisterAgent(path, description)

    Parameters
    string path
            path to agent
    string description
            path to file description or direct term with agent description

    Returns
    bool
            if succeed
    """

scr_docs['RegisterNewAgents'] = \
    """Register new agents.
    Rescan the scrconf registration directories and register any agents at new(!) paths. Agents, even new ones, on paths that are registered already, will not be replaced. This means that .oes.specific.agent will start to work but something like adding /usr/local/etc/sysconfig to .sysconfig.network would not.

    Synopsis
    RegisterNewAgents()

    Returns
    bool
            if succeed
    """

scr_docs['UnmountAgent'] = \
    """Unmounts agent. The agent is detached, but when needed it is mounted again automatically.

    It sends to component result() which force to terminate component. If there is any lazy write, then it is properly finished.

    Synopsis
    UnmountAgent(path)

    Parameters
    string path
            path to agent
    """

scr_docs['UnregisterAgent'] = \
    """Unregister agent from given path

    Synopsis
    UnregisterAgent(path)

    Parameters
    string path
            path to agent

    Returns
    bool
            if succeed
    """

scr_docs['UnregisterAllAgents'] = \
    """Unregister all agents

    Synopsis
    UnregisterAllAgents()

    Returns
    bool
            if succeed
    """

scr_docs['Write'] = \
    """Writes data

    Synopsis
    Write(path, *args)

    Parameters
    string path
            path that is combination of path where agent is attached and path inside agent
    args
            additional arguments depending on agent

    Returns
    bool
            if succeed
    """

