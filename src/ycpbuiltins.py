from __future__ import absolute_import, division, print_function, unicode_literals

def get_caller_loginfo(frames):
    '''Returns the caller n frames back
    '''
    import inspect
    frame = inspect.currentframe()
    for i in range(0, frames):
        frame = frame.f_back
    info = inspect.getframeinfo(frame)
    return info

def y2milestone(*args):
    '''Log a milestone to the y2log.
    '''
    from ycp import y2milestone
    frame_info = get_caller_loginfo(2)
    y2milestone(frame_info[0], frame_info[1], frame_info[2], sformat(*args))

def y2warning(*args):
    '''Log a warning to the y2log.
    '''
    from ycp import y2warning
    frame_info = get_caller_loginfo(2)
    y2warning(frame_info[0], frame_info[1], frame_info[2], sformat(*args))

def y2error(*args):
    '''Log an error to the y2log.
    '''
    from ycp import y2error
    frame_info = get_caller_loginfo(2)
    y2error(frame_info[0], frame_info[1], frame_info[2], sformat(*args))

def y2debug(*args):
    '''Log a message to the y2log.
    '''
    from ycp import y2debug
    frame_info = get_caller_loginfo(2)
    y2debug(frame_info[0], frame_info[1], frame_info[2], sformat(*args))

def y2internal(*args):
    '''Log an internal message to the y2log.
    '''
    from ycp import y2internal
    frame_info = get_caller_loginfo(2)
    y2internal(frame_info[0], frame_info[1], frame_info[2], sformat(*args))

def y2security(*args):
    '''Log a security message to the y2log.
    '''
    from ycp import y2security
    frame_info = get_caller_loginfo(2)
    y2security(frame_info[0], frame_info[1], frame_info[2], sformat(*args))

# placeholder for Buildins.foreach
def foreach(listOrMap):
    '''
    Process the content of a map
    Processes the content of a list
    '''
    try:
        iterator = iter(listOrMap)
    except:
        y2error("%s is not iterable %s"%type(listOrMap))
        return None
    return listOrMap

# add - Add a key/value pair to a map or list
def add(listOrMap, key, value=None):
    '''
    Adds element to copy of element and return such copy.
    '''
    from ycp import pyval_to_ycp, List, Term

    if isinstance(listOrMap, dict):
        listOrMap[key] = value
    elif isinstance(listOrMap, List) or isinstance(listOrMap, Term):
         ycpvalue = pyval_to_ycp(key)
         listOrMap.add(ycpvalue)
    else: # assume list
        listOrMap.append(key)
    # should we clone the listOrMap here ?
    return listOrMap

def size(listMapOrTerm):
    '''
    size() Yast built-in

    Size of a map
    Returns the number of path elements
    Returns size of list
    Returns the number of arguments of the term TERM.
    Returns the number of characters of the string s
    '''
    from ycp import Term
    if isinstance(listMapOrTerm, Term):
        return listMapOrTerm.size()
    # assume list or map 
    return len(listMapOrTerm)

def sleep(millisecs):
    '''
    Sleeps a number of milliseconds.
    '''
    import time
    time.sleep(float(millisecs)/1000)

def tostring(val):
    '''
    Converts a value to a string in ycp.
    '''
    try:
        return val.toString()
    except:
        return str(val)

def sformat(*pars):
    '''
    Yast compatible way how to format string with type conversion see tostring for type conversion
    '''
    list_pars = list(pars)
    form = list_pars.pop(0)
    placeholders = ['%1', '%2', '%3', '%4', '%5', '%6', '%7', '%8', '%9', '%%']
    arg_positions = []
    for placeholder in placeholders:
        index = 0
        if placeholder in form:
            while True:
                index = form.find(placeholder, index)
                if index == -1:
                    break
                pos = form[index + 1]
       	        if pos != '%':
                    try:
                        # assume YCP value
                        arg_positions.append(pars[int(pos)].toString())
                    except:
                        arg_positions.append(pars[int(pos)])

                    form = form.replace(placeholder, '%s')
                index = index + 2
    if len(arg_positions):
        return form%tuple(arg_positions)
    return form 

def flatten(lists):
    '''
    Flattens List
    '''
    newlist = []
    for l in lists:
        newlist = newlist + l
    return newlist

def union(list1, list2):
    '''
    Unions of lists
    Union of 2 maps
    '''
    return list(set().union(list1, list2))

def merge(list1, list2):
    '''
    merge() Yast built-in Merges two lists into one
    '''
    return list1 + list2

def random(maxint):
    '''
    Random number generator.
    '''
    from random import randint as pyrand_range
    return pyrand_range(0, maxint)

def mergestring(listofstrings, glue):
    '''
    mergestring() Yast built-in Joins list elements with a string
    '''
    first = True
    result = None
    for item in listofstrings:
        if first:
            result = item
            first = False
        else:
            result = result + glue + item 
    return result

def substring(s, start, num_chars=None):
    '''
    substring() Yast built-in Extracts a substring
    '''
    result = None
    try:
        result = s[start:start + num_chars]
    except:
        result = ""
    return result

def regexpmatch(searchtext, pattern):
    '''
    Searches a string for a POSIX Extended Regular Expression match.
    If string or pattern is None, or if pattern is an invalid regex, None is returned.

    Parameters:
    string (String) - a string to search
    pattern (String) - a regex in the C syntax

    Returns:
    (Boolean, None) - does string match pattern
    '''
    import re
    return re.search(pattern, searchtext) is not None

del absolute_import, division, print_function, unicode_literals
