from collections.abc import Iterable, Sequence
from typing import Any
import types
import time
import os


def animated_print(txt,
                   end: str = '\n',
                   delay: float = 0.02,
                   front_effect: str = '',
                   line_offset: int = 1,
                   fancy_mode: bool = False,
                   _overload: bool = False):
    """
    Prints text with an animation effect, simulating a typewriter-style output.

    Parameters:
    - txt: The text to print. It can be a string or an iterable of strings.
    - end: A string appended after the last value, default is a newline.
    - delay: Time in seconds between each character print, default is 0.02 seconds.
    - front_effect: A string effect applied at the front of animated text.
    - line_offset: Number of lines to offset the text vertically.
    - fancy_mode: Whether to use the fancy animation mode from fancy.py
    - interval: Time in milliseconds between each character in fancy mode (default: 5ms)
    """
    # Use fancy mode if enabled (from fancy.py)
    if fancy_mode:
        if isinstance(txt, (list, tuple)):
            txt = '\n'.join(str(item) for item in txt)
        
        # Import required modules for fancy mode
        import sys
        import string
        import re
        import ctypes
        import ctypes.wintypes
        import termios
        import tty

        # Get terminal dimensions
        t = os.get_terminal_size().columns - 1
        
        # Setup console mode for fancy print
        if sys.platform == "win32":
            c = ctypes
            d = ctypes.wintypes.DWORD()
            k = c.windll.kernel32
            k.GetConsoleMode(k.GetStdHandle(-10), c.byref(d))
            k.SetConsoleMode(k.GetStdHandle(-10), 0)
            k.GetConsoleMode(k.GetStdHandle(-11), c.byref(d))
            k.SetConsoleMode(k.GetStdHandle(-11), 7)
            sys.stdout.write("\x1b[?25l\x1b[6n")
            sys.stdout.flush()
            
            def read_cursor_pos(a):
                if a.endswith("R"):
                    return a
                return read_cursor_pos(a + sys.stdin.read(1))
            
            b = read_cursor_pos(sys.stdin.read(1))
            k.SetConsoleMode(k.GetStdHandle(-10), d)
            k.SetConsoleMode(k.GetStdHandle(-11), d)
            r = re.match(r"^\x1b\[(\d*);(\d*)R", b)
            b = int(r.groups()[1]) if r else 1
        else:
            s = sys.stdin.fileno()
            ta = termios.tcgetattr(s)
            tty.setcbreak(s, termios.TCSANOW)
            sys.stdout.write("\x1b[?25l\x1b[6n")
            sys.stdout.flush()
            
            def read_cursor_pos(a):
                if a.endswith("R"):
                    return a
                return read_cursor_pos(a + sys.stdin.read(1))
            
            b = read_cursor_pos("")
            termios.tcsetattr(s, termios.TCSANOW, ta)
            r = re.match(r"^\x1b\[(\d*);(\d*)R", b)
            b = int(r.groups()[1]) if r else 1
        
        # Prepare text for fancy printing
        p = list(string.printable)[:-6]
        o = sys.stdout.write
        m = (str(txt) + str(end) + "\0").split("\n")
        
        if len(m) > 0:
            m = [" \b" * ((b - 1) // 2) + "\0" * ((b - 1) % 2) + m[0]] + (m[1:] if len(m) > 1 else [])
            a = ""
            
            # Print each line
            for l in (a for b in ([l[a:a+t] for a in range(0, len(l)+1, t)] for l in m[:-1]) for a in b):
                for n in l:
                    if n == "\x1b":
                        a = n
                    elif a:
                        a = a + n
                    
                    # Animation effect for each character
                    for c in p[:(p.index(n) + 1 if n in p else 0 if n in "\0 \b" or a else len(p))]:
                        o(c + "\b")
                        sys.stdout.flush()
                        time.sleep(delay/10)
                    
                    # Write actual character
                    if a == "":
                        o(n)
                    elif a == "\x1b[" or a[-1] < "@" or a[-1] > "~":
                        pass
                    else:
                        o(a + " \b")
                        a = ""
                
                o("\x1b[1C\n")
            
            # Process the last line
            for l in (a for b in ([l[a:a+t] for a in range(0, len(l)+1, t)] for l in m[-1:]) for a in b):
                for n in l:
                    if n == "\x1b":
                        a = n
                    elif a:
                        a = a + n
                    
                    # Animation effect for each character
                    for c in p[:(p.index(n) + 1 if n in p else 0 if n in "\0 \b" or a else len(p))]:
                        o(a)
                        o(c + "\b")
                        sys.stdout.flush()
                        time.sleep(delay/10)
                    
                    # Write actual character
                    if a == "":
                        o(n)
                    elif a == "\x1b[" or a[-1] < "@" or a[-1] > "~":
                        pass
                    else:
                        o(a + " \b")
                        a = ""
            
        # Show cursor again
        o("\x1b[?25h")
        sys.stdout.flush()
        return
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
                   fancy_mode=False,  # Don't use fancy mode for recursion
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
                   fancy_mode: bool = False,
                   interval: int = 5):
    """
    Same as animated_print but with input
    
    Parameters:
    - prompt: Text to display before the input
    - delay: Time in seconds between each character print (for non-fancy mode)
    - front_effect: A string effect applied at the front of animated text
    - line_offset: Number of lines to offset the text vertically
    - fancy_mode: Whether to use the fancy animation mode from fancy.py
    - interval: Time in milliseconds between each character in fancy mode
    """
    # Use fancy input mode if enabled
    if fancy_mode:
        # Import required modules for fancy input
        import sys
        import string
        import re
        import ctypes
        import ctypes.wintypes
        import termios
        import tty
        
        # Get terminal dimensions
        t = os.get_terminal_size().columns - 1
        
        # Setup console mode for fancy input
        if sys.platform == "win32":
            c = ctypes
            d = ctypes.wintypes.DWORD()
            k = c.windll.kernel32
            k.GetConsoleMode(k.GetStdHandle(-10), c.byref(d))
            k.SetConsoleMode(k.GetStdHandle(-10), 0)
            k.GetConsoleMode(k.GetStdHandle(-11), c.byref(d))
            k.SetConsoleMode(k.GetStdHandle(-11), 7)
            sys.stdout.write("\x1b[?25l\x1b[6n")
            sys.stdout.flush()
            
            def read_cursor_pos(a):
                if a.endswith("R"):
                    return a
                return read_cursor_pos(a + sys.stdin.read(1))
            
            b = read_cursor_pos(sys.stdin.read(1))
            r = re.match(r"^\x1b\[(\d*);(\d*)R", b)
            b = int(r.groups()[1]) if r else 1
        else:
            s = sys.stdin.fileno()
            ta = termios.tcgetattr(s)
            tty.setcbreak(s, termios.TCSANOW)
            sys.stdout.write("\x1b[?25l\x1b[6n")
            sys.stdout.flush()
            
            def read_cursor_pos(a):
                if a.endswith("R"):
                    return a
                return read_cursor_pos(a + sys.stdin.read(1))
            
            b = read_cursor_pos(sys.stdin.read(1))
            r = re.match(r"^\x1b\[(\d*);(\d*)R", b)
            b = int(r.groups()[1]) if r else 1
        
        # Prepare prompt for fancy input
        p = [" "] + list(string.printable)[:-6]
        o = sys.stdout.write
        m = (str(prompt) + "\0").split("\n")
        
        if len(m) > 0:
            m = [" \b" * ((b - 1) // 2) + "\0" * ((b - 1) % 2) + m[0]] + (m[1:] if len(m) > 1 else [])
            a = ""
            
            # Print each line of the prompt
            for l in (a for b in ([l[a:a+t] for a in range(0, len(l)+1, t)] for l in m[:-1]) for a in b):
                for n in l:
                    if n == "\x1b":
                        a = n
                    elif a:
                        a = a + n
                    
                    # Animation effect for each character
                    for c in p[:(p.index(n) + 1 if n in p else 0 if n in "\0 \b" or a else len(p))]:
                        o(c + "\b")
                        sys.stdout.flush()
                        time.sleep(interval / 1000)
                    
                    # Write actual character
                    if a == "":
                        o(n)
                    elif a == "\x1b[" or a[-1] < "@" or a[-1] > "~":
                        pass
                    else:
                        o(a + " \b")
                        a = ""
                
                o("\x1b[1C\n")
            
            # Process the last line
            for l in (a for b in ([l[a:a+t] for a in range(0, len(l)+1, t)] for l in m[-1:]) for a in b):
                for n in l:
                    if n == "\x1b":
                        a = n
                    elif a:
                        a = a + n
                    
                    # Animation effect for each character
                    for c in p[:(p.index(n) + 1 if n in p else 0 if n in "\0 \b" or a else len(p))]:
                        o(a)
                        o(c + "\b")
                        sys.stdout.flush()
                        time.sleep(interval / 1000)
                    
                    # Write actual character
                    if a == "":
                        o(n)
                    elif a == "\x1b[" or a[-1] < "@" or a[-1] > "~":
                        pass
                    else:
                        o(a + " \b")
                        a = ""
            
            o("\x1b[?25h")
            sys.stdout.flush()
            
            # Handle input with fancy animation
            def read_input(a, u, pt):
                l = sys.stdin.read(1)
                
                # Handle backspace
                if l in "\x7f\x08" and len(u) > 0:
                    u = u[:-1]
                    if pt % (t - 1) != 0:
                        o("\b \b")
                    else:
                        o(f"\x1b[F\x1b[{t-2}G\b \b")
                    sys.stdout.flush()
                    pt = pt - 1
                # Handle regular input
                elif l != "\n":
                    u = u + l
                    if pt % (t - 1) == 0:
                        o(" \n")
                    
                    # Animation for input character
                    if l == "\x1b":
                        a = l
                    elif a:
                        a = a + l
                    
                    for c in p[:(p.index(l) + 1 if l in p else 0 if l in "\0 \b\n" or a else len(p))]:
                        o(a)
                        o(c + "\b")
                        sys.stdout.flush()
                        time.sleep(interval / 1000)
                    
                    if a == "":
                        o(l)
                    elif a == "\x1b[" or a[-1] < "@" or a[-1] > "~":
                        pass
                    else:
                        o(a + " \b")
                        a = ""
                    
                    sys.stdout.flush()
                    pt = pt + 1
                
                # Continue reading or return result
                if l != "\n":
                    return read_input(a, u, pt)
                return u
            
            # Read user input with animation
            result = read_input("", "", (len(m[-1]) + (b if len(m) == 1 else 0)) % (t - 1))[:-1]
            
            # Restore terminal state
            if sys.platform == "win32":
                k.SetConsoleMode(k.GetStdHandle(-10), d)
                k.SetConsoleMode(k.GetStdHandle(-11), d)
            else:
                termios.tcsetattr(s, termios.TCSANOW, ta)
            
            return result
    
    # Use original animated_input if fancy mode is disabled
    animated_print(prompt, "", delay, front_effect, line_offset, fancy_mode=False)
    return input()


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


def binary_search(input_list: list, value, /):
    """
    Binary search for value in a sorted list.
    
    Args:
        input_list: Sorted list to search
        value: Value to search for
    
    Returns:
        Index of value if found, -1 otherwise
    """
    start = 0
    end = len(input_list) - 1
    if not is_sorted(input_list):
        raise ValueError(
            "Binary_search: input list is not sorted what are you doing")
    while start <= end:
        mid = (start + end) // 2
        if value == input_list[mid]:
            return mid
        elif value < input_list[mid]:
            end = mid - 1
        else:
            start = mid + 1
    return -1


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


def is_sorted(input_list: list, default=1):
    """
    Check if input list is sorted.
    
    Args:
        input_list: List to check
        default: Default value to return if list is too short
    
    Returns:
        1 if sorted in ascending order, -1 if sorted in descending order, 0 if not sorted, default if all item in list is the same value
    """
    ascending = True
    descending = True
    if len(input_list) < 2:
        return default
    for n in range(len(input_list) - 1):
        if input_list[n] > input_list[n + 1]:
            ascending = False
        elif input_list[n] < input_list[n + 1]:
            descending = False
        if not (ascending or descending):
            break
    if ascending and descending:
        return default
    return ascending - descending


def repeat_str_to_len(word: str,
                      length: int,
                      start_index=0) -> tuple[str, int]:
    """
    Repeat string to a certain length.
    
    Args:
        word: String to repeat
        length: Desired length
        start_index: Index to start from
    
    Returns:
        Tuple of repeated string and new start index
    """
    if not isinstance(word, str):
        raise TypeError("word must be a str")
    if not (isinstance(length, int) and length >= 0):
        raise TypeError("length must be a positive int")
    if not (isinstance(start_index, int) and start_index >= 0 and
            (start_index < len(word) or not word)):
        raise TypeError(
            "start_index must be a positive int which less than the length of word"
        )
    if length == 0 or not word:
        return '', 0
    words = word * (-((-length) // len(word)) + 1)  #word * (ceil division + 1)
    return words[start_index:length +
                 start_index], (length + start_index) % len(word)


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
        if in_ansi and i > ansi_start and text[i].isalpha():
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

