from collections.abc import Iterable, Sequence
from typing import Any
import types
import time
import os
import sys
import string
import re
import ctypes
import ctypes.wintypes
import termios
import tty


def animated_print(txt,
                   end: str = '\n',
                   delay: float = 0.02,
                   front_effect: str = '',
                   line_offset: int = 1,
                   _overload: bool = False):
    """
    Prints text with an animation effect, simulating a typewriter-style output.

    Parameters:
    - txt: The text to print. It can be a string or an iterable of strings.
    - end: A string appended after the last value, default is a newline.
    - delay: Time in seconds between each character print, default is 0.02 seconds.
    - front_effect: A string effect applied at the front of animated text.
    - line_offset: Number of lines to offset the text vertically.
    """
    if len(txt) == 0:
        return
    if all(
        (all(isinstance(subchar, str) for subchar in char)\
         if (isinstance(char, (list, tuple)) and _overload)\
         else isinstance(char, str)) for char in txt):
        if all(len(char) == 1 for char in txt):
            #its a str
            txt = ''.join(txt).split('\n')
        else:
            txt = list(txt)
    else:
        raise TypeError("txt must be a str or iterable of str")
    if not isinstance(delay, (int, float)):
        raise TypeError("delay must be a number")
    if not isinstance(front_effect, str):
        raise TypeError("front_effect must be a str")

    term_size = os.get_terminal_size()
    txt_lst = []
    for line in txt:
        if _overload: #optimization by skipping an O(n^3)? algorithm if input alr processed
            txt_lst = txt
            break #dont wanna indent the entire thing even more or else it would be ugly
        if not line:
            txt_lst.append("")
            continue
        temp = split_exclude_ANSI(line, " ")
        words: list[str] = [(item if i == len(temp) else item + " ")
                            for i, item in enumerate(temp)]
        index: int = 0
        while index < len(words):
            if len(words[index]) > term_size.columns-1:
                for warpped_line in (
                        line[i:i + term_size.columns-1]
                        for i in range(0, len(line), term_size.columns-1)):
                    txt_lst.append(warpped_line)
                index += 1
                continue
            txt_lst.append("")
            for i, word in enumerate(words[index:]):
                if len(txt_lst[-1]) + len(word) > term_size.columns-1:
                    index += i
                    break  #break for loop
                txt_lst[-1] += word
            else:
                break  #break while loop
    if not _overload:
        txt_lst = [split_exclude_ANSI(line) for line in txt_lst]
    txt_lst, truncated = txt_lst[:term_size.lines - 1], txt_lst[term_size.lines - 1:]
    max_wordlen = max(len(line) for line in txt_lst)
    print('\n' * (len(txt_lst)), end='\x1b[A')
    for i in range(max_wordlen + line_offset * (len(txt_lst))):
        print("\x1b[A" * (len(txt_lst) - 1), end='')
        time.sleep(delay)
        for j, line in enumerate(txt_lst):
            current_char = j * line_offset + 1
            print(' ' * len(front_effect) + "\x1b[D" * len(front_effect),
                  end='')
            if (i - current_char >= 0
                    and i - current_char < len(line)):  #needs animated update
                print("\x1b[" + str(current_char) + "D" +
                      line[i - current_char] + front_effect +
                      "\x1b[D" * len(front_effect) + "\x1b[" +
                      str(current_char) + "C" + "\b\x1b[1B",
                      end='',
                      flush=True)
            else:
                print("\x1b[1B", end='', flush=True)
        print("\x1b[1A\x1b[1C", end='', flush=True)
    time.sleep(delay)
    print("\x1b[" + str(line_offset * len(txt_lst)) + "D", end=end, flush=True)
    animated_print(truncated,
                   end,
                   delay,
                   front_effect,
                   line_offset,
                   _overload=True)
    return
    #deprecated cuz buggy
    '''
    elif front_effect[1] == 0:
        for i in range(len(txt)):
            time.sleep(delay)
            print(front_effect[0][i % len(front_effect[0])], end='', flush=True)
        print("\x1b[1G", end='')
        for char in txt:
            time.sleep(delay)
            print(char, end='', flush=True)
    else:
        for i in range(len(txt)+front_effect[1]):
            time.sleep(delay)
            print(front_effect[0][i % len(front_effect[0])], end='', flush=True)
            if i - front_effect[1] >= 0:
                print("\x1b["+str(front_effect[1]+1)+"D"+
                    txt[i - front_effect[1]]+
                    "\x1b["+str(front_effect[1])+"C", 
                    end='', flush=True)
        print("\x1b["+str(front_effect[1])+"D", end='')
        for _ in range(front_effect[1]):
            time.sleep(delay)
            print(' ', end='', flush=True)
    print(end=end)
    return
    '''


def animated_input(prompt: str,
                   delay: float = 0.02,
                   front_effect="",
                   line_offset: int = 1,
                   _log: bool = False):
    """
    Same as animated_print but with input
    
    Parameters:
    - prompt: Text to display before the input
    - delay: Time in seconds between each character print (for non-fancy mode)
    - front_effect: A string effect applied at the front of animated text
    - line_offset: Number of lines to offset the text vertically
    """
    
    animated_print(prompt, "", delay, front_effect, line_offset)
    columns = os.get_terminal_size().columns - 2
    if sys.platform == "win32":
        dword = ctypes.wintypes.DWORD()
        kernel = ctypes.windll.kernel32
        kernel.GetConsoleMode(kernel.GetStdHandle(-10), ctypes.byref(dword))
        kernel.SetConsoleMode(kernel.GetStdHandle(-10), 0)
        kernel.GetConsoleMode(kernel.GetStdHandle(-11), ctypes.byref(dword))
        kernel.SetConsoleMode(kernel.GetStdHandle(-11), 7)

       
    else:
        stdin = sys.stdin.fileno()
        original_term = termios.tcgetattr(stdin)
        tty.setcbreak(stdin, termios.TCSANOW)

    sys.stdout.write("\x1b[?25l\x1b[6n")
    sys.stdout.flush()
    a = sys.stdin.read(1)
    while not a.endswith("R"):
        a += sys.stdin.read(1)

    r = re.match(r"^\x1b\[(\d*);(\d*)R", a)
    ptr = int(r.groups()[1]) if r else 1
    # Prepare prompt for fancy input
    printables = [" "] + list(string.printable)[:-6]
    output = sys.stdout.write

    char = sys.stdin.read(1)
    result = ""
    ansi = ""
    # Handle input with fancy animation
    while char != "\n":    
        if char in "\x7f\x08": #if backspace character
            if len(result) > 0: #if can backspace
                if _log:
                    with open("input_log.txt", "a") as f:
                        f.write("del\n")
                result = result[:-1] #backspace 1 character
                if ptr % columns != 0:
                    output("\b \b") #flush the character away
                else: #if need go back previous line
                    output(f"\x1b[F\x1b[{columns-1}G\b \b") #go back previous line and flush
                sys.stdout.flush() #show change to terminal
                ptr = ptr - 1 #column pointer also go back one
        else: #regular input
            if _log:
                with open("input_log.txt", "a") as f:
                    f.write(f"add {repr(char)} \n")
            result += char
            if ptr % columns == 0:
                output(" \n")
            
            # Animation for input character
            if char == "\x1b":
                ansi = char
            elif ansi:
                ansi += char
            if char in printables:
                end_cyc = linear_search(printables, char) + 1
            elif char in "\0 \b\n" or ansi:
                end_cyc = 0
            else:
                end_cyc = len(printables)
            for c in printables[:end_cyc]:
                output(ansi)
                output(c + "\b")
                sys.stdout.flush()
                time.sleep(delay / 10)
            
            if ansi == "":
                output(char)
            elif ansi == "\x1b[" or ansi[-1] < "@" or ansi[-1] > "~":
                pass
            else:
                output(a + " \b")
                ansi = ""
            
            sys.stdout.flush()
            ptr = ptr + 1
        char = sys.stdin.read(1)
    
    output("\n")
    # Restore terminal state
    if sys.platform == "win32":
        kernel.SetConsoleMode(kernel.GetStdHandle(-10), dword)
        kernel.SetConsoleMode(kernel.GetStdHandle(-11), dword)
    else:
        termios.tcsetattr(stdin, termios.TCSANOW, original_term)

    if _log:
        with open("input_log.txt", "a") as f:
            f.write(f"submitted {repr(result)} \n")
    return result


def type_check(instance: Any,
               _type: type | types.GenericAlias | types.UnionType) -> bool:
    """
    Checks if the given instance is of the given type.

        instance (Any): The instance to check.
        _type (type | types.GenericAlias | types.UnionType): The type to check against.

    Returns:
        bool: True if instance is of type _type, False otherwise.
    """

    if not isinstance(_type, (
            type,
            types.GenericAlias,
            types.UnionType,
    )):
        raise TypeError("_type must be a type")

    if isinstance(_type, types.UnionType):
        return any(type_check(instance, t) for t in _type.__args__)

    #check if _type is sth like list[int] or tuple[str,int]
    if isinstance(_type, types.GenericAlias):
        if not hasattr(_type, '__origin__') or not hasattr(_type, '__args__'):
            raise AssertionError(
                "GenericAlias should always have __origin__ and __args__")

        if not isinstance(instance, _type.__origin__):
            return False
        if isinstance(instance, tuple):
            if len(_type.__args__) != len(instance):
                return False
            return all((type_check(instance[i], _type.__args__[i]))
                       for i in range(len(_type.__args__)))
        return all(type_check(item, _type.__args__[0]) for item in instance)
    # normal check
    # check if instance is a subclass of _type
    return isinstance(instance, _type)


def quick_sort(input_list: Sequence, ascending: bool = True):
    """
    Sorts a list using the quick sort algorithm.
    
    Args:
        input_list: List to sort
        ascending: Sort in ascending order if True, descending if False
    
    Returns:
        Sorted list
    """
    # Base case (when list have 1 or 0 item its sorted)
    if len(input_list) < 2:
        return input_list

    pivot = input_list[0]  # First pivot
    less = []
    more = []

    # Divide into 3 parts
    for item in input_list[1:]:
        if item < pivot:
            less.append(item)
        else:
            more.append(item)

    # Recurse + conquer + return
    return (list(quick_sort(less)) + [pivot] +
            list(quick_sort(more)))[::1 if ascending else -1]



def linear_search(input_list: list,
                  value,
                  start=0,
                  stop=9223372036854775807,
                  /):
    """
    Linear search for value in a list.
    
    Args:
        input_list: List to search
        value: Value to search for
        start: Start index
        stop: Stop index
    
    Returns:
        Index of value if found, -1 otherwise
    """
    stop = min(stop, len(input_list))
    for n in range(start, stop):
        if input_list[n] == value:
            return n
    return -1






def split_exclude_ANSI(text: str, sep: str | list[str] | tuple[str] = ""):
    """
    Splits a string by separator(s) while preserving ANSI escape sequences.

    Args:
        text: The string to split
        sep: Separator(s) to split by. Can be a string, list of strings, or tuple of strings.
             If empty string, split into individual characters.

    Returns:
        List of strings after splitting by separator(s)
    """
    if not type_check(sep, str | list[str] | tuple[str]):
        raise TypeError(
            f"sep should be either string or list or tuple that contains only strings, not {type(sep)}"
        )

    # Handle empty text case
    if not text:
        return []

    # Convert sep to list for uniform handling
    separators = [sep] if isinstance(sep, str) else list(sep)

    # Handle empty separator case (split into characters)
    result = []
    i = 0
    start = 0
    in_ansi = False
    ansi_start = -1

    while i < len(text):
        # Check if we're in an ANSI escape sequence
        if text[i] == '\x1b' and i + 1 < len(text) and text[i + 1] == '[':
            in_ansi = True
            ansi_start = i

        # Check if we're at the end of an ANSI sequence
        if in_ansi and i > ansi_start+1 and text[i] > "@" and text[i] < "~":
            in_ansi = False

        # Only check for separators if we're not in an ANSI sequence
        if not in_ansi:
            if separators == [""]:
                i += 1
            # Check if current position matches any separator
            for separator in separators:
                if i + len(separator) <= len(text) and text[i:i + len(separator)] == separator:
                    result.append(text[start:i])
                    i += len(separator) - 1  # -1 because we'll increment i at the end of the loop
                    start = i + 1
                    break

        i += 1

    # Add the last segment
    result.append(text[start:])
    
    while result[-1] == "":
        del result[-1] #in case null strings showed up at the end by some separator mess (causes trouble)

    return result


def max(*args):
    if not args:
        raise TypeError("max expected at least 1 argument, 0 received")
    elif len(args) == 1:
        args = args[0]
        if isinstance(args, Iterable):
            args = list(args)
        else:
            return args
    maximum = args[0]
    for n in args:
        if n > maximum:
            maximum = n
    return maximum


def min(*args):
    if not args:
        raise TypeError("min expected at least 1 argument, 0 received")
    elif len(args) == 1:
        args = args[0]
        if isinstance(args, Iterable):
            args = list(args)
        else:
            return args
    minimum = args[0]
    for n in args:
        if n < minimum:
            minimum = n
    return minimum


def all(*args):
    if not args:
        return True
    elif len(args) == 1:
        args = args[0]
        if isinstance(args, Iterable):
            args = list(args)
        else:
            return args
    for n in args:
        if not n:
            return False
    return True


def any(*args):
    if not args:
        return False
    elif len(args) == 1:
        args = args[0]
        if isinstance(args, Iterable):
            args = list(args)
        else:
            return args
    for n in args:
        if n:
            return True
    return False


def find_all_str(input_str, target_str):
    result = []
    current_ptr = 0
    for n in range(len(input_str)):
        if input_str[n] == target_str[current_ptr]:
            current_ptr += 1
            if current_ptr == len(target_str):
                result.append(n - current_ptr)
                current_ptr = 0
        else:
            current_ptr = 0
    return result

