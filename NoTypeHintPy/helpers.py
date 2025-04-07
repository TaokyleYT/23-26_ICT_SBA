import os
import re
import string
import sys
import time
if sys.platform == 'win32':
    import ctypes
    import ctypes.wintypes
else:
    import termios
    import tty
def animated_print(txt='', end='\n', delay=0.01, line_offset=1, _override=False, wrap_override=False):
    """
    Prints text with an animation effect, simulating a typewriter-style output.

    This function displays text character by character with a delay between each character,
    creating a typewriter-like animation effect. It handles multi-line text, text wrapping,
    and preserves ANSI escape sequences for colored or formatted text.

    printing steps:
    repeat:
        ↟ to the top
        repeat:
            → prints � ↲
        until reach line that is not yet at their turn to print or after last line
    until everything is printed out

    per iteration:
    ```
    ↑→→→
    ↑  ↲
    ↑ ↲
    ↑↲
    ```

    Warning: Multi-line text including ANSI codes may not output as expected, as
    full support would require significantly more complex implementation.

    More Warning: line wrapping, despite implemented, seldom fail for whatever reason
    and I can't seem to fix it without breaking something else.
    Please use a bigger terminal or a smaller font size to avoid breaking everything that is being outputted

    Args:
        txt (str | Iterable[str] | Iterable[Iterable[str]]):
            The text to print. Can be a single string, a list of strings, or a nested list of strings.
        end (str):
            A string to print after the entire text has been animated (default: newline).
        delay (float):
            The time in seconds between each character print (default: 0.01s).
        line_offset (int):
            The number of lines to offset the text vertically for animation (default: 1).
        _override (bool):
            An internal parameter for optimization during recursion to override certain type checks.
            Not intended for direct use.
        wrap_override (bool):
            When True, enables line wrapping even when _override is True (default: False).
            Intended for direct use when you touched the "Not intended for direct use" _override parameter

    Raises:
        TypeError: If `end` is not a string, `delay` is not a number, or `txt` is not
                    a string or an iterable of strings.

    Returns:
        None
    """
    if not isinstance(end, str):
        raise TypeError('end must be a string')
    if not isinstance(delay, (int, float)):
        raise TypeError('delay must be a number')
    if len(txt) == 0:
        print(end=end)
        return
    if all((all((isinstance(subchar, str) for subchar in char)) if isinstance(char, (list, tuple)) and _override else isinstance(char, str) for char in txt)):
        if all((len(char) == 1 for char in txt)):
            txt = ''.join(txt).split('\n')
        else:
            txt = list(txt)
    else:
        raise TypeError('txt must be a str or iterable of str')
    term_size = os.get_terminal_size()
    txt_lst = []
    for line in txt:
        if _override and (not wrap_override):
            txt_lst = txt
            break
        if not line:
            txt_lst.append('')
            continue
        if _override and wrap_override:
            txt_lst_temp = []
            current_line = []
            for char in line:
                current_line.append(char)
                if len(current_line) >= term_size.columns - 1:
                    txt_lst_temp.append(current_line)
                    current_line = []
            if current_line:
                txt_lst_temp.append(current_line)
            txt_lst.extend(txt_lst_temp)
        else:
            temp = split_exclude_ANSI(line, ' ')
            words: list[str] = [item if i == len(temp) - 1 else item + ' ' for i, item in enumerate(temp)]
            index: int = 0
            while index < len(words):
                if len(words[index]) > term_size.columns - 1:
                    for wrapped_line in (line[i:i + term_size.columns - 1] for i in range(0, len(line), term_size.columns - 1)):
                        txt_lst.append(wrapped_line)
                    index += 1
                    continue
                txt_lst.append('')
                for i, word in enumerate(words[index:]):
                    if len(txt_lst[-1]) + len(word) > term_size.columns - 1:
                        index += i
                        break
                    txt_lst[-1] += word
                else:
                    break
    if not _override:
        txt_lst = [split_exclude_ANSI(line) for line in txt_lst]
    txt_lst, truncated = (txt_lst[:term_size.lines - 1], txt_lst[term_size.lines - 1:])
    max_wordlen = max((len(line) for line in txt_lst))
    print('\n' * len(txt_lst), end='\x1b[A')
    for i in range(max_wordlen + line_offset * len(txt_lst)):
        print('\x1b[A' * (len(txt_lst) - 1), end='')
        time.sleep(delay)
        for j, line in enumerate(txt_lst):
            current_char = j * line_offset + 1
            if i - current_char >= 0 and i - current_char < len(line):
                print('\x1b[' + str(current_char) + 'D' + line[i - current_char] + '\x1b[' + str(current_char) + 'C' + '\x08\x1b[B', end='', flush=True)
            else:
                print('\x1b[B', end='', flush=True)
        print('\x1b[A\x1b[C', end='', flush=True)
    time.sleep(delay)
    print('\x1b[' + str(line_offset * len(txt_lst)) + 'D', end='\n' if truncated else '', flush=True)
    animated_print(truncated, end, delay, line_offset, _override=True, wrap_override=wrap_override)
    return
def animated_input(prompt='', delay=0.01, line_offset=1, single_letter=False, _log=False):
    """
    Animated version of input() that displays a prompt with animation effects.

    This function displays an animated prompt and accepts user input with
    character-by-character animation. Special keys like backspace are handled,
    and ANSI escape sequences in the input are supported.

    Warning: Multi-line prompts including ANSI codes may not output as expected
    due to implementation complexity.

    Note that this input does not support multi-line input, just like the original one

    Args:
        prompt (str):
            Text to display before the input field.
        delay (float):
            Time in seconds between character animations (default: 0.01s).
        line_offset (int):
            Number of lines to offset the text vertically (default: 1).
        single_letter (bool):
            Whether to accept a single letter input and return immediately (default: False).
            If True, skips animation and returns after a single keypress.
        _log (bool):
            Whether to log input for debugging purposes (internal use, default: False).
            When enabled, writes input events to "input_log.txt".

    Returns:
        str: The user's input string (without the trailing newline).
    """
    animated_print(prompt, ' ', delay, line_offset)
    columns = os.get_terminal_size().columns - 2
    if sys.platform == 'win32':
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
    if single_letter:
        if _log:
            with open('input_log.txt', 'a') as f:
                f.write('\n-----\nInput started (single letter)\n-----\n')
        result = '\n'
        while result == '\n':
            result = sys.stdin.read(1)
        if result in '\x03\x04':
            if _log:
                with open('input_log.txt', 'a') as f:
                    f.write(f'KeyboardInterrupt with {result}\n')
            raise KeyboardInterrupt
        print(result)
        if sys.platform == 'win32':
            kernel.SetConsoleMode(kernel.GetStdHandle(-10), dword)
            kernel.SetConsoleMode(kernel.GetStdHandle(-11), dword)
        else:
            termios.tcsetattr(stdin, termios.TCSANOW, original_term)
        if _log:
            with open('input_log.txt', 'a') as f:
                f.write(f'submitted {repr(result)} \n')
        return result
    sys.stdout.write('\x1b[?25l\x1b[6n')
    sys.stdout.flush()
    result = sys.stdin.read(1)
    while not result.endswith('R'):
        result += sys.stdin.read(1)
    reg = re.match('^\\x1b\\[(\\d*);(\\d*)R', result)
    ptr = int(reg.groups()[1]) if reg else 1
    printables = [' '] + list(string.printable)[:-6]
    output = sys.stdout.write
    char = sys.stdin.read(1)
    result = ''
    ansi = ''
    if _log:
        with open('input_log.txt', 'a') as f:
            f.write('\n-----\nInput started\n-----\n')
    while char != '\n':
        if char in '\x03\x04':
            if _log:
                with open('input_log.txt', 'a') as f:
                    f.write(f'KeyboardInterrupt with {char}\n')
            raise KeyboardInterrupt
        if char in '\x7f\x08':
            if len(result) > 0:
                if _log:
                    with open('input_log.txt', 'a') as f:
                        f.write('del\n')
                result = result[:-1]
                if ptr % columns != 0:
                    output('\x08 \x08')
                else:
                    output(f'\x1b[F\x1b[{columns - 1}G\x08 \x08')
                sys.stdout.flush()
                ptr -= 1
        else:
            if _log:
                with open('input_log.txt', 'a') as f:
                    f.write(f'add {repr(char)} \n')
            result += char
            if ptr % columns == 0:
                output(' \n')
            if char == '\x1b':
                ansi = char
            elif ansi:
                ansi += char
            if char in printables:
                end_cyc = linear_search(printables, char) + 1
            elif char in '\x00 \x08\n' or ansi:
                end_cyc = 0
            else:
                end_cyc = len(printables)
            for c in printables[:end_cyc]:
                output(ansi)
                output(c + '\x08')
                sys.stdout.flush()
                time.sleep(delay / 10)
            if ansi == '':
                output(char)
            elif ansi == '\x1b[' or ansi[-1] < '@' or ansi[-1] > '~':
                pass
            else:
                output(result + ' \x08')
                ansi = ''
            sys.stdout.flush()
            ptr += 1
        char = sys.stdin.read(1)
    output('\n')
    if sys.platform == 'win32':
        kernel.SetConsoleMode(kernel.GetStdHandle(-10), dword)
        kernel.SetConsoleMode(kernel.GetStdHandle(-11), dword)
    else:
        termios.tcsetattr(stdin, termios.TCSANOW, original_term)
    if _log:
        with open('input_log.txt', 'a') as f:
            f.write(f'submitted {repr(result)} \n')
    return result
def quick_sort(iterable, /, *, key=None, reverse=False):
    """
    Sorts a list using the quick sort algorithm.

    This is a recursive implementation of the quick sort algorithm that uses
    the first element as the pivot. It creates new lists rather than sorting in-place.

    Args:
        Iterable (Iterable):
            The list or sequence to sort.
        key (callable):
            A key function to extract a comparison key from each element (default: None).
        reverse (bool):
            reverse flag can be set to request the result in descending order.

    Returns:
        list: A new sorted list.

    Time Complexity:
        - Average case: O(n log n)
        - Worst case: O(n^2) when the list is already sorted

    Space Complexity:
        O(n) due to the creation of new lists during recursion.
    """
    if len(iterable) < 2:
        return iterable
    pivot = iterable[0]
    comp_pivot = pivot if key is None else key(pivot)
    less = []
    more = []
    for item in iterable[1:]:
        comp_item = item if key is None else key(item)
        if not reverse:
            if comp_item < comp_pivot:
                less.append(item)
            else:
                more.append(item)
        elif comp_item > comp_pivot:
            less.append(item)
        else:
            more.append(item)
    return list(quick_sort(less, reverse=reverse)) + [pivot] + list(quick_sort(more, reverse=reverse))
def linear_search(iterable, value, start=0, stop=9223372036854775807, /):
    """
    Performs a linear search for a value in a list.

    Sequentially checks each element in the list until it finds a match or reaches the end.
    Allows specifying a range to search within.

    Args:
        iterable (list):
            The list to search in.
        value:
            The value to search for.
        start (int):
            Starting index for the search (default: 0).
        stop (int):
            Ending index (exclusive) for the search
            (default: 9223372036854775807, which is 2^63-1,
            aka largest signed integer in 64 bit system, I copied it straight out from list.index docs,
            to search the entire list).

    Returns:
        int: Index of the first occurrence of `value` if found, -1 otherwise.

    Time Complexity:
        O(n) where n is the number of elements in the specified search range.
    """
    stop = min(stop, len(iterable))
    for n in range(start, stop):
        if iterable[n] == value:
            return n
    return -1
def split_exclude_ANSI(text, sep=''):
    r"""
    Splits a string by separator(s) while preserving ANSI escape sequences.

    This functions similar to `str.split()` but retains ANSI escape codes within each
    resulting substring. If the separator is empty, it splits into individual characters
    while keeping ANSI sequences together.

    Args:
        text (str):
            The string to split.
        sep (str | list[str] | tuple[str]):
            Separator(s) to split by. Can be a string or an iterable (list or tuple) of strings.
            If empty string, it splits into individual characters.

    Returns:
        list[str]: A list of strings after splitting by separator(s).

    Raises:
        TypeError: If `sep` is not a string, a list of strings, or a tuple of strings.

    Example:
        >>> split_exclude_ANSI("\\x1b[31mHello\\x1b[0m World", "")
        ['\\x1b[31m', 'Hello, '\\x1b[0m', 'World']
        >>> split_exclude_ANSI("\\x1b[31mHello\\x1b[0m World", " ")
        ['\\x1b[31mHello\\x1b[0m', 'World']
    """
    if not (isinstance(sep, str) or all((isinstance(s, str) for s in sep))):
        raise TypeError('sep should be either string or an iterable that contains only strings')
    if not text:
        return []
    separators = [sep] if isinstance(sep, str) else list(sep)
    result = []
    i = 0
    start = 0
    in_ansi = False
    ansi_start = -1
    while i < len(text):
        if text[i] == '\x1b' and i + 1 < len(text) and (text[i + 1] == '['):
            in_ansi = True
            ansi_start = i
        if in_ansi and i > ansi_start + 1 and (text[i] > '@') and (text[i] < '~'):
            in_ansi = False
        if not in_ansi:
            if separators == ['']:
                i += 1
            for separator in separators:
                if i + len(separator) <= len(text) and text[i:i + len(separator)] == separator:
                    result.append(text[start:i])
                    i += len(separator) - 1
                    start = i + 1
                    break
        i += 1
    result.append(text[start:])
    while result and result[-1] == '':
        del result[-1]
    return result
def max(*args):
    """
    Returns the largest item in an iterable or the largest of multiple arguments.

    This function reimplements the built-in max() to allow use without directly importing
    built-in functions or creating excessively large loops.

    Args:
        *args: Accepts either a single iterable or multiple arguments to compare.

    Returns:
        The largest item among those provided.

    Raises:
        TypeError: If no arguments are provided.

    Example:
        >>> max(1, 2, 3)
        3
        >>> max([1, 2, 3])
        3
    """
    if not args:
        raise TypeError('max expected at least 1 argument, 0 received')
    elif len(args) == 1:
        args = args[0]
        if hasattr(args, '__iter__') and not isinstance(args, (str, bytes)):
            args = list(args)
        else:
            return args
    maximum = args[0]
    for n in args:
        if n > maximum:
            maximum = n
    return maximum
def min(*args):
    """
    Returns the smallest item in an iterable or the smallest of multiple arguments.

    This function reimplements the built-in min() to allow use without directly importing
    built-in functions or creating excessively large loops.

    Args:
        *args: Accepts either a single iterable or multiple arguments to compare.

    Returns:
        The smallest item among those provided.

    Raises:
        TypeError: If no arguments are provided.

    Example:
        >>> min(1, 2, 3)
        1
        >>> min([1, 2, 3])
        1
    """
    if not args:
        raise TypeError('min expected at least 1 argument, 0 received')
    elif len(args) == 1:
        args = args[0]
        if hasattr(args, '__iter__') and not isinstance(args, (str, bytes)):
            args = list(args)
        else:
            return args
    minimum = args[0]
    for n in args:
        if n < minimum:
            minimum = n
    return minimum
def all(*args):
    """
    Returns True if all elements of the iterable are true (or if iterable is empty).

    This function reimplements the built-in all() to allow use without importing
    built-in functions or creating excessively large loops.

    Args:
        *args: Accepts either a single iterable or multiple arguments to check.

    Returns:
        bool: True if all elements are true, False otherwise.

    Example:
        >>> all([True, True, True])
        True
        >>> all([True, False, True])
        False
    """
    if not args:
        return True
    elif len(args) == 1:
        args = args[0]
        if hasattr(args, '__iter__') and not isinstance(args, (str, bytes)):
            args = list(args)
        else:
            return args
    for n in args:
        if not n:
            return False
    return True
def any(*args):
    """
    Returns True if any element of the iterable is true.

    This function reimplements the built-in any() to allow use without directly importing
    built-in functions or creating excessively large loops. If the iterable is empty, returns False.

    Args:
        *args: Accepts either a single iterable or multiple arguments to check.

    Returns:
        bool: True if any element is true, False otherwise.

    Example:
        >>> any([False, False, True])
        True
        >>> any([False, False, False])
        False
    """
    if not args:
        return False
    elif len(args) == 1:
        args = args[0]
        if hasattr(args, '__iter__') and not isinstance(args, (str, bytes)):
            args = list(args)
        else:
            return args
    for n in args:
        if n:
            return True
    return False