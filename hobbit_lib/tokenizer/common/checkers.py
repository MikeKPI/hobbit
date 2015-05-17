def isDigit(checkable):
    """
    checks if checkable is digit or not and returns True if it's a digit,
    otherwise - False
    """
    return 47 < ord(checkable) < 58

def isLetter(checkable):
    """
    checks if checkable is letter
    :returns True if it's a digit, otherwise - False
    """
    temp = ord(checkable)
    return (54 < temp < 91) or \
           (96 < temp < 123) or \
           temp == 95

def isDoubleHook(checkable):
    """
    checks for Hooks
    :returns True if it's a hook, otherwise returns False
    """
    if checkable == '"':
        return True
    else:
        return False

def isExMark(checkable):
    """
    checks for '!'
    :returns True if it's a '!', otherwise - False
    """
    if checkable == '!':
        return True
    else:
        return False

def isACommentStart(checkable):
    """
    checks for start of comment
    :returns True if checkable == '#', otherwise - False
    """
    if checkable == '#':
        return True
    else:
        return False

def isE(checkable):
    """
    checks for 'e' in float numbers
    :returns True if checkable == 'e', otherwise - False
    """
    if checkable == 'e':
        return True
    else:
        return False

def isSplitterDot(checkable):
    """
    checks for '.' in floating numbers
    :returns True if checkable == '.', otherwise - False
    """
    if checkable == '.':
        return True
    else:
        return False

def isVerticalLine(checkable):
    """
    checks for '|' in splitters
    :returns True if checkable == '|', otherwise - False
    """
    if checkable == '|':
        return True
    else:
        return False

def isSingleAnd(checkable):
    """
    checks for '&' in splitters
    :returns True if checkable == '&', otherwise - False
    """
    if checkable == '&':
        return True
    else:
        return False

def isSingleEqu(checkable):
    """
    checks for '=' in splitters
    :returns True if checkable == '=', otherwise - False
    """
    if checkable == '=':
        return True
    else:
        return False

def isSingleSplitter(checkable):
    """
    checks is it single splitter
    :returns True if checkable is single splitter, otherwise - False
    """
    single_splitters = ['*', '/', '%', '(', ')', '{', '}', '\n', ',']
    if checkable in single_splitters:
        return True
    else:
        return False

def isFirtsPartOfDoubleSplitter(checkable):
    """
    checks for first part of double splitters
    :returns True if checkable is first part of double splitter, otherwise - False
    """
    fpds = ['<', '>']
    if checkable in fpds:
        return True
    else:
        return False

def isPlusOrMinus(checkable):
    """
    checks for '+' and '-'
    :returns True if checkable == '+' or '-', otherwise - False
    """
    pom = ['+', '-']
    if checkable in pom:
        return True
    else:
        return False

def isWhiteSplitter(checkable):
    """
    checks for white splitter like tab and space
    :returns True if checkable is white splitter, otherwise - False
    """
    ws = ['\t', ' ']
    if checkable in ws:
        return True
    else:
        return False
