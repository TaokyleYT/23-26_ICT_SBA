import os
import re
import string
import sys
import time
from typing import Iterable
if (sys.platform == 'win32'):
    import ctypes
    import ctypes.wintypes
else:
    import termios
    import tty

def animated_print(txt='', end='\n', delay=0.01, line_offset=1, _override=False, wrap_override=False):
    '\n    Prints text with an animation effect, simulating a typewriter-style output.\n\n    This function displays text character by character with a delay between each character,\n    creating a typewriter-like animation effect. It handles multi-line text, text wrapping,\n    and preserves ANSI escape sequences for colored or formatted text.\n\n    printing steps:\n    repeat:\n        ↟ to the top\n        repeat:\n            → prints ← ↲\n        until reach line that is not yet at their turn to print or after last line\n    until everything is printed out\n\n    per iteration:\n    ```\n    ↑→→→\n    ↑  ↲\n    ↑ ↲\n    ↑↲\n    ```\n\n    Warning: Multi-line text including ANSI codes may not output as expected, as\n    full support would require significantly more complex implementation.\n\n    More Warning: line wrapping, despite implemented, seldom fail for whatever reason\n    and I can\'t seem to fix it without breaking something else.\n    Please use a bigger terminal or a smaller font size to avoid breaking everything that is being outputted\n\n    Args:\n        txt (str | Iterable[str,] | Iterable[Iterable[str,],]):\n            The text to print. Can be a single string, a list of strings, or a nested list of strings.\n        end (str):\n            A string to print after the entire text has been animated (default: newline).\n        delay (float):\n            The time in seconds between each character print (default: 0.01s).\n        line_offset (int):\n            The number of lines to offset the text vertically for animation (default: 1).\n        _override (bool):\n            An internal parameter for optimization during recursion to override certain type checks.\n            Not intended for direct use.\n        wrap_override (bool):\n            When True, enables line wrapping even when _override is True (default: False).\n            Intended for direct use when you touched the "Not intended for direct use" _override parameter\n\n    Raises:\n        TypeError: If `end` is not a string, `delay` is not a number, or `txt` is not\n                    a string or an iterable of strings.\n\n    Returns:\n        None\n    '
    if (not isinstance(end, str)):
        raise TypeError('end must be a string')
    if (not isinstance(delay, (int, float))):
        raise TypeError('delay must be a number')
    if (len(txt) == 0):
        print(end=end)
        return
    if all(((all((isinstance(subchar, str) for subchar in char)) if (isinstance(char, (list, tuple)) and _override) else isinstance(char, str)) for char in txt)):
        if all(((len(char) == 1) for char in txt)):
            txt = ''.join(txt).split('\n')
        else:
            txt = list(txt)
    else:
        raise TypeError('txt must be a str or iterable of str')
    term_size = os.get_terminal_size()
    txt_lst = []
    for line in txt:
        if (_override and (not wrap_override)):
            txt_lst = txt
            break
        if (not line):
            txt_lst.append('')
            continue
        if (_override and wrap_override):
            txt_lst_temp = []
            current_line = []
            for char in line:
                current_line.append(char)
                if (len(current_line) >= (term_size.columns - 1)):
                    txt_lst_temp.append(current_line)
                    current_line = []
            if current_line:
                txt_lst_temp.append(current_line)
            txt_lst.extend(txt_lst_temp)
        else:
            temp = split_exclude_ANSI(line, ' ')
            words: list[str] = [(item if (i == (len(temp) - 1)) else (item + ' ')) for (i, item) in enumerate(temp)]
            index: int = 0
            while (index < len(words)):
                if (len(words[index]) > (term_size.columns - 1)):
                    for wrapped_line in (line[i:((i + term_size.columns) - 1)] for i in range(0, len(line), (term_size.columns - 1))):
                        txt_lst.append(wrapped_line)
                    index += 1
                    continue
                txt_lst.append('')
                for (i, word) in enumerate(words[index:]):
                    if ((len(txt_lst[(- 1)]) + len(word)) > (term_size.columns - 1)):
                        index += i
                        break
                    txt_lst[(- 1)] += word
                else:
                    break
    if (not _override):
        txt_lst = [split_exclude_ANSI(line) for line in txt_lst]
    (txt_lst, truncated) = (txt_lst[:(term_size.lines - 1)], txt_lst[(term_size.lines - 1):])
    max_wordlen = max((len(line) for line in txt_lst))
    print(('\n' * len(txt_lst)), end='\x1b[A')
    for i in range((max_wordlen + (line_offset * len(txt_lst)))):
        print(('\x1b[A' * (len(txt_lst) - 1)), end='')
        time.sleep(delay)
        for (j, line) in enumerate(txt_lst):
            current_char = ((j * line_offset) + 1)
            if (((i - current_char) >= 0) and ((i - current_char) < len(line))):
                print(((((((('\x1b[' + str(current_char)) + 'D') + line[(i - current_char)]) + '\x1b[') + str(current_char)) + 'C') + '\x08\x1b[B'), end='', flush=True)
            else:
                print('\x1b[B', end='', flush=True)
        print('\x1b[A\x1b[C', end='', flush=True)
    time.sleep(delay)
    print((('\x1b[' + str((line_offset * len(txt_lst)))) + 'D'), end=('\n' if truncated else ''), flush=True)
    animated_print(truncated, end, delay, line_offset, _override=True, wrap_override=wrap_override)
    return

def animated_input(prompt='', delay=0.01, line_offset=1, single_letter=False, _log=False):
    '\n    Animated version of input() that displays a prompt with animation effects.\n\n    This function displays an animated prompt and accepts user input with\n    character-by-character animation. Special keys like backspace are handled,\n    and ANSI escape sequences in the input are supported.\n\n    Warning: Multi-line prompts including ANSI codes may not output as expected\n    due to implementation complexity.\n\n    Note that this input does not support multi-line input, just like the original one\n\n    Args:\n        prompt (str):\n            Text to display before the input field.\n        delay (float):\n            Time in seconds between character animations (default: 0.01s).\n        line_offset (int):\n            Number of lines to offset the text vertically (default: 1).\n        single_letter (bool):\n            Whether to accept a single letter input and return immediately (default: False).\n            If True, skips animation and returns after a single keypress.\n        _log (bool):\n            Whether to log input for debugging purposes (internal use, default: False).\n            When enabled, writes input events to "input_log.txt".\n\n    Returns:\n        str: The user\'s input string (without the trailing newline).\n    '
    animated_print(prompt, ' ', delay, line_offset)
    columns = (os.get_terminal_size().columns - 2)
    if (sys.platform == 'win32'):
        dword = ctypes.wintypes.DWORD()
        kernel = ctypes.windll.kernel32
        kernel.GetConsoleMode(kernel.GetStdHandle((- 10)), ctypes.byref(dword))
        kernel.SetConsoleMode(kernel.GetStdHandle((- 10)), 0)
        kernel.GetConsoleMode(kernel.GetStdHandle((- 11)), ctypes.byref(dword))
        kernel.SetConsoleMode(kernel.GetStdHandle((- 11)), 7)
    else:
        stdin = sys.stdin.fileno()
        original_term = termios.tcgetattr(stdin)
        tty.setcbreak(stdin, termios.TCSANOW)
    if single_letter:
        if _log:
            with open('input_log.txt', 'a') as f:
                f.write('\n-----\nInput started (single letter)\n-----\n')
        result = '\n'
        while (result == '\n'):
            result = sys.stdin.read(1)
        if (result in '\x03\x04'):
            if _log:
                with open('input_log.txt', 'a') as f:
                    f.write(f'''KeyboardInterrupt with {result}
''')
            raise KeyboardInterrupt
        print(result)
        if (sys.platform == 'win32'):
            kernel.SetConsoleMode(kernel.GetStdHandle((- 10)), dword)
            kernel.SetConsoleMode(kernel.GetStdHandle((- 11)), dword)
        else:
            termios.tcsetattr(stdin, termios.TCSANOW, original_term)
        if _log:
            with open('input_log.txt', 'a') as f:
                f.write(f'''submitted {repr(result)} 
''')
        return result
    sys.stdout.write('\x1b[?25l\x1b[6n')
    sys.stdout.flush()
    result = sys.stdin.read(1)
    while (not result.endswith('R')):
        result += sys.stdin.read(1)
    reg = re.match('^\\x1b\\[(\\d*);(\\d*)R', result)
    ptr = (int(reg.groups()[1]) if reg else 1)
    printables = ([' '] + list(string.printable)[:(- 6)])
    output = sys.stdout.write
    char = sys.stdin.read(1)
    result = ''
    ansi = ''
    if _log:
        with open('input_log.txt', 'a') as f:
            f.write('\n-----\nInput started\n-----\n')
    while (char != '\n'):
        if (char in '\x03\x04'):
            if _log:
                with open('input_log.txt', 'a') as f:
                    f.write(f'''KeyboardInterrupt with {char}
''')
            raise KeyboardInterrupt
        if (char in '\x7f\x08'):
            if (len(result) > 0):
                if _log:
                    with open('input_log.txt', 'a') as f:
                        f.write('del\n')
                result = result[:(- 1)]
                if ((ptr % columns) != 0):
                    output('\x08 \x08')
                else:
                    output(f'[F[{(columns - 1)}G ')
                sys.stdout.flush()
                ptr -= 1
        else:
            if _log:
                with open('input_log.txt', 'a') as f:
                    f.write(f'''add {repr(char)} 
''')
            result += char
            if ((ptr % columns) == 0):
                output(' \n')
            if (char == '\x1b'):
                ansi = char
            elif ansi:
                ansi += char
            if (char in printables):
                end_cyc = (linear_search(printables, char) + 1)
            elif ((char in '\x00 \x08\n') or ansi):
                end_cyc = 0
            else:
                end_cyc = len(printables)
            for c in printables[:end_cyc]:
                output(ansi)
                output((c + '\x08'))
                sys.stdout.flush()
                time.sleep((delay / 10))
            if (ansi == ''):
                output(char)
            elif ((ansi == '\x1b[') or (ansi[(- 1)] < '@') or (ansi[(- 1)] > '~')):
                pass
            else:
                output((result + ' \x08'))
                ansi = ''
            sys.stdout.flush()
            ptr += 1
        char = sys.stdin.read(1)
    output('\n')
    if (sys.platform == 'win32'):
        kernel.SetConsoleMode(kernel.GetStdHandle((- 10)), dword)
        kernel.SetConsoleMode(kernel.GetStdHandle((- 11)), dword)
    else:
        termios.tcsetattr(stdin, termios.TCSANOW, original_term)
    if _log:
        with open('input_log.txt', 'a') as f:
            f.write(f'''submitted {repr(result)} 
''')
    return result

def quick_sort(iterable: Iterable, /, *, key=None, reverse: bool=False):
    '\n    Sorts a list using the quick sort algorithm.\n\n    This is a recursive implementation of the quick sort algorithm that uses\n    the first element as the pivot. It creates new lists rather than sorting in-place.\n\n    Args:\n        Iterable (Iterable):\n            The list or sequence to sort.\n        key (callable):\n            A key function to extract a comparison key from each element (default: None).\n        reverse (bool):\n            reverse flag can be set to request the result in descending order.\n\n    Returns:\n        list: A new sorted list.\n\n    Time Complexity:\n        - Average case: O(n log n)\n        - Worst case: O(n^2) when the list is already sorted\n\n    Space Complexity:\n        O(n) due to the creation of new lists during recursion.\n    '
    if (len(iterable) < 2):
        return iterable
    pivot = iterable[0]
    comp_pivot = (pivot if (key is None) else key(pivot))
    less = []
    more = []
    for item in iterable[1:]:
        comp_item = (item if (key is None) else key(item))
        if (not reverse):
            if (comp_item < comp_pivot):
                less.append(item)
            else:
                more.append(item)
        elif (comp_item > comp_pivot):
            less.append(item)
        else:
            more.append(item)
    return ((list(quick_sort(less, reverse=reverse)) + [pivot]) + list(quick_sort(more, reverse=reverse)))

def linear_search(iterable: list, value, start=0, stop=9223372036854775807, /):
    '\n    Performs a linear search for a value in a list.\n\n    Sequentially checks each element in the list until it finds a match or reaches the end.\n    Allows specifying a range to search within.\n\n    Args:\n        iterable (list):\n            The list to search in.\n        value:\n            The value to search for.\n        start (int):\n            Starting index for the search (default: 0).\n        stop (int):\n            Ending index (exclusive) for the search\n            (default: 9223372036854775807, which is 2^63-1,\n            aka largest signed integer in 64 bit system, I copied it straight out from list.index docs,\n            to search the entire list).\n\n    Returns:\n        int: Index of the first occurrence of `value` if found, -1 otherwise.\n\n    Time Complexity:\n        O(n) where n is the number of elements in the specified search range.\n    '
    stop = min(stop, len(iterable))
    for n in range(start, stop):
        if (iterable[n] == value):
            return n
    return (- 1)

def split_exclude_ANSI(text, sep=''):
    '\n    Splits a string by separator(s) while preserving ANSI escape sequences.\n\n    This functions similar to `str.split()` but retains ANSI escape codes within each\n    resulting substring. If the separator is empty, it splits into individual characters\n    while keeping ANSI sequences together.\n\n    Args:\n        text (str):\n            The string to split.\n        sep (str | list[str] | tuple[str]):\n            Separator(s) to split by. Can be a string or an iterable (list or tuple) of strings.\n            If empty string, it splits into individual characters.\n\n    Returns:\n        list[str]: A list of strings after splitting by separator(s).\n\n    Raises:\n        TypeError: If `sep` is not a string, a list of strings, or a tuple of strings.\n\n    Example:\n        >>> split_exclude_ANSI("\\x1b[31mHello\\x1b[0m World", "")\n        [\'\\x1b[31m\', \'Hello, \'\\x1b[0m\', \'World\']\n        >>> split_exclude_ANSI("\\x1b[31mHello\\x1b[0m World", " ")\n        [\'\\x1b[31mHello\\x1b[0m\', \'World\']\n    '
    if (not (isinstance(sep, str) or all((isinstance(s, str) for s in sep)))):
        raise TypeError('sep should be either string or an iterable that contains only strings')
    if (not text):
        return []
    separators = ([sep] if isinstance(sep, str) else list(sep))
    result = []
    i = 0
    start = 0
    in_ansi = False
    ansi_start = (- 1)
    while (i < len(text)):
        if ((text[i] == '\x1b') and ((i + 1) < len(text)) and (text[(i + 1)] == '[')):
            in_ansi = True
            ansi_start = i
        if (in_ansi and (i > (ansi_start + 1)) and (text[i] > '@') and (text[i] < '~')):
            in_ansi = False
        if (not in_ansi):
            if (separators == ['']):
                i += 1
            for separator in separators:
                if (((i + len(separator)) <= len(text)) and (text[i:(i + len(separator))] == separator)):
                    result.append(text[start:i])
                    i += (len(separator) - 1)
                    start = (i + 1)
                    break
        i += 1
    result.append(text[start:])
    while (result and (result[(- 1)] == '')):
        del result[(- 1)]
    return result

def max(*args):
    '\n    Returns the largest item in an iterable or the largest of multiple arguments.\n\n    This function reimplements the built-in max() to allow use without directly importing\n    built-in functions or creating excessively large loops.\n\n    Args:\n        *args: Accepts either a single iterable or multiple arguments to compare.\n\n    Returns:\n        The largest item among those provided.\n\n    Raises:\n        TypeError: If no arguments are provided.\n\n    Example:\n        >>> max(1, 2, 3)\n        3\n        >>> max([1, 2, 3])\n        3\n    '
    if (not args):
        raise TypeError('max expected at least 1 argument, 0 received')
    elif (len(args) == 1):
        args = args[0]
        if isinstance(args, Iterable):
            args = list(args)
        else:
            return args
    maximum = args[0]
    for n in args:
        if (n > maximum):
            maximum = n
    return maximum

def min(*args):
    '\n    Returns the smallest item in an iterable or the smallest of multiple arguments.\n\n    This function reimplements the built-in min() to allow use without directly importing\n    built-in functions or creating excessively large loops.\n\n    Args:\n        *args: Accepts either a single iterable or multiple arguments to compare.\n\n    Returns:\n        The smallest item among those provided.\n\n    Raises:\n        TypeError: If no arguments are provided.\n\n    Example:\n        >>> min(1, 2, 3)\n        1\n        >>> min([1, 2, 3])\n        1\n    '
    if (not args):
        raise TypeError('min expected at least 1 argument, 0 received')
    elif (len(args) == 1):
        args = args[0]
        if isinstance(args, Iterable):
            args = list(args)
        else:
            return args
    minimum = args[0]
    for n in args:
        if (n < minimum):
            minimum = n
    return minimum

def all(*args):
    '\n    Returns True if all elements of the iterable are true (or if iterable is empty).\n\n    This function reimplements the built-in all() to allow use without importing\n    built-in functions or creating excessively large loops.\n\n    Args:\n        *args: Accepts either a single iterable or multiple arguments to check.\n\n    Returns:\n        bool: True if all elements are true, False otherwise.\n\n    Example:\n        >>> all([True, True, True])\n        True\n        >>> all([True, False, True])\n        False\n    '
    if (not args):
        return True
    elif (len(args) == 1):
        args = args[0]
        if isinstance(args, Iterable):
            args = list(args)
        else:
            return args
    for n in args:
        if (not n):
            return False
    return True

def any(*args):
    '\n    Returns True if any element of the iterable is true.\n\n    This function reimplements the built-in any() to allow use without directly importing\n    built-in functions or creating excessively large loops. If the iterable is empty, returns False.\n\n    Args:\n        *args: Accepts either a single iterable or multiple arguments to check.\n\n    Returns:\n        bool: True if any element is true, False otherwise.\n\n    Example:\n        >>> any([False, False, True])\n        True\n        >>> any([False, False, False])\n        False\n    '
    if (not args):
        return False
    elif (len(args) == 1):
        args = args[0]
        if isinstance(args, Iterable):
            args = list(args)
        else:
            return args
    for n in args:
        if n:
            return True
    return False