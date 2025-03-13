
from collections.abc import Iterable, Sequence
from typing import Any
import types
import time
import os
import sys
import string
import re
if sys.platform == "win32":
    import ctypes
    import ctypes.wintypes
else:
    import termios
    import tty


def animated_print(txt,
                   delay: float = 0.02,
                   line_offset: int = 1,
                   _overload: bool = False):
    """
    Prints text with an animation effect, simulating a typewriter-style output.
    
    This function handles multi-line text and deals with ANSI color codes.
    It also wraps text to fit the terminal width.
    
    Args:
        txt (str or list): The text to print. Can be a string or list of strings.
        delay (float): Time in seconds between each character print (0.02s default).
        line_offset (int): Number of lines to offset the text vertically.
        _overload (bool): Internal parameter for optimization during recursion.
    """
    if all(
        (all(isinstance(subchar, str) for subchar in char)\
         if (isinstance(char, (list, tuple)) and _overload)\
         else isinstance(char, str)) for char in txt):
        if all(len(char) == 1 for char in txt):
            # It's a str, convert to lines
            txt = (''.join(txt)).split('\n')
        else:
            txt = list(txt)
    else:
        raise TypeError("txt must be a str or iterable of str")
    if not isinstance(delay, (int, float)):
        raise TypeError("delay must be a number")
    
    if len(txt) == 0:
        return #if need print nothing, prints nothing
    input(txt)

    # Get terminal size for text wrapping
    term_size = os.get_terminal_size()
    txt_lst = []

    # Process each line for wrapping and animation
    for line in txt:
        if _overload: #optimization by skipping an O(n^3)? algorithm if input already processed
            txt_lst = txt
            break
        if not line:
            txt_lst.append("") #newline, use empty string to replace
            continue
        temp = split_exclude_ANSI(line, " ") # Split line by spaces, preserving ANSI codes
        words: list[str] = [(item if i == len(temp) else item + " ")
                            for i, item in enumerate(temp)]
        # Wrap text to terminal width
        index: int = 0
        while index < len(words):
            if len(words[index]) > term_size.columns-1:
                # Handle words longer than terminal width
                for warpped_line in (
                        line[i:i + term_size.columns-1]
                        for i in range(0, len(line), term_size.columns-1)):
                    txt_lst.append(warpped_line)
                index += 1
                continue
            # Add words to line until it would exceed terminal width
            txt_lst.append("")
            for i, word in enumerate(words[index:]):
                if len(txt_lst[-1]) + len(word) > term_size.columns-1:
                    index += i
                    break  #break for loop
                txt_lst[-1] += word
            else:
                break  # Break while loop if all words processed
    if not _overload:
        # Split each line into characters while preserving ANSI codes
        # (Because ANSI codes are technically >=4 characters long, but prints as 0 characters, treating them as a character won't cause issue)
        # (and if they are not preserved, they will be seperated and broken and thus raw ANSI code is being printed)
        txt_lst = [split_exclude_ANSI(line) for line in txt_lst]

    # Truncate text if it would exceed terminal height
    txt_lst, truncated = txt_lst[:term_size.lines - 1], txt_lst[term_size.lines - 1:]

    # Find the maximum line length (aka width of animation rectangle) for animation timing
    max_wordlen = max(len(line) for line in txt_lst)

    # Create space for the animation
    print('\n' * (len(txt_lst)), end='\x1b[A')

    # Animate text character by character
    for i in range(max_wordlen + line_offset * (len(txt_lst))):
        print("\x1b[A" * (len(txt_lst) - 1), end='')
        time.sleep(delay)
        for j, line in enumerate(txt_lst):
            current_char = j * line_offset + 1
            # Determine if this line needs updating at this step
            if (i - current_char >= 0
                    and i - current_char < len(line)):
                # Print current character with front effect
                print("\x1b[" + str(current_char) + "D" + # Move cursor left
                      line[i - current_char] + 
                      "\x1b[" + str(current_char) + 
                      "C" + "\b\x1b[1B",
                      end='',
                      flush=True)
            else:
                print("\x1b[1B", end='', flush=True)
        print("\x1b[1A\x1b[1C", end='', flush=True)
    time.sleep(delay)
    print("\x1b[" + str(line_offset * len(txt_lst)) + "D", end='\n', flush=True)
    animated_print(truncated,
                   delay,
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
    Animated version of input() that displays a prompt with animation effects.
    
    This function displays an animated prompt and then accepts user input with
    character-by-character animation as the user types.
    
    Args:
        prompt (str): Text to display before the input.
        delay (float): Time in seconds between character animations (0.02s default).
        front_effect (str): String to display at front of animated text.
        line_offset (int): Number of lines to offset the text vertically.
        _log (bool): Whether to log input for debugging (internal use).
        
    Returns:
        str: The user's input string (without the trailing newline).
    """
    # Display the prompt with animation
    animated_print(prompt, "", delay, front_effect, line_offset)
    
    # Get terminal width
    columns = os.get_terminal_size().columns - 2
    
    # Set terminal to character-by-character input mode
    if sys.platform == "win32":
        # Windows implementation
        dword = ctypes.wintypes.DWORD()
        kernel = ctypes.windll.kernel32
        kernel.GetConsoleMode(kernel.GetStdHandle(-10), ctypes.byref(dword))
        kernel.SetConsoleMode(kernel.GetStdHandle(-10), 0)
        kernel.GetConsoleMode(kernel.GetStdHandle(-11), ctypes.byref(dword))
        kernel.SetConsoleMode(kernel.GetStdHandle(-11), 7)
    else:
        # Unix/Linux implementation
        stdin = sys.stdin.fileno()
        original_term = termios.tcgetattr(stdin)
        tty.setcbreak(stdin, termios.TCSANOW)

    # Get cursor position
    sys.stdout.write("\x1b[?25l\x1b[6n")  # Hide cursor and request position
    sys.stdout.flush()
    a = sys.stdin.read(1)
    while not a.endswith("R"):
        a += sys.stdin.read(1)

    # Parse cursor position response
    r = re.match(r"^\x1b\[(\d*);(\d*)R", a)
    ptr = int(r.groups()[1]) if r else 1
    
    # Prepare character sets for animation
    printables = [" "] + list(string.printable)[:-6]  # Printable ASCII minus control chars
    output = sys.stdout.write

    # Read input char by char until enter key
    char = sys.stdin.read(1)
    result = ""
    ansi = ""
    
    if _log:
        with open("input_log.txt", "a") as f:
            f.write("\n-----\nInput started\n-----\n")
    # Handle input with fancy animation
    while char != "\n":
        if char in "\x03\x04":
            raise KeyboardInterrupt
        if char in "\x7f\x08":  # Backspace character
            if len(result) > 0:  # If can backspace
                if _log:
                    with open("input_log.txt", "a") as f:
                        f.write("del\n")
                result = result[:-1]  # Remove last char from result
                
                if ptr % columns != 0:
                    output("\b \b")  # Erase character on same line
                else:  # If at beginning of line, go to previous line
                    output(f"\x1b[F\x1b[{columns-1}G\b \b")
                    
                sys.stdout.flush()  # Show changes
                ptr = ptr - 1  # Move cursor position back
        else:  # Regular input character
            if _log:
                with open("input_log.txt", "a") as f:
                    f.write(f"add {repr(char)} \n")
                    
            result += char  # Add to result string
            
            if ptr % columns == 0:
                output(" \n")  # Create new line if at end of terminal
            
            # Determine animation for this character
            if char == "\x1b":  # Start of ANSI escape sequence
                ansi = char
            elif ansi:  # Continue ANSI sequence
                ansi += char
                
            # Determine how many character animations to show
            if char in printables:
                end_cyc = linear_search(printables, char) + 1
            elif char in "\0 \b\n" or ansi:
                end_cyc = 0
            else:
                end_cyc = len(printables)
                
            # Perform character animation
            for c in printables[:end_cyc]:
                output(ansi)
                output(c + "\b")  # Show character then backspace
                sys.stdout.flush()
                time.sleep(delay / 10)
            
            # Handle final character display
            if ansi == "":
                output(char)
            elif ansi == "\x1b[" or ansi[-1] < "@" or ansi[-1] > "~":
                pass  # Incomplete ANSI sequence
            else:
                output(a + " \b")
                ansi = ""
            
            sys.stdout.flush()
            ptr = ptr + 1  # Move cursor position forward
            
        char = sys.stdin.read(1)  # Read next character
    
    output("\n")  # Final newline
    
    # Restore terminal state
    if sys.platform == "win32":
        kernel.SetConsoleMode(kernel.GetStdHandle(-10), dword)
        kernel.SetConsoleMode(kernel.GetStdHandle(-11), dword)
    else:
        termios.tcsetattr(stdin, termios.TCSANOW, original_term)

    # Log final result if enabled
    if _log:
        with open("input_log.txt", "a") as f:
            f.write(f"submitted {repr(result)} \n")
            
    return result


def type_check(instance: Any,
               _type: type | types.GenericAlias | types.UnionType) -> bool:
    """
    Advanced type checking that supports generics and unions.
    
    This function extends beyond isinstance() to handle complex type annotations
    like list[int], tuple[str, int], and Union types.
    
    Args:
        instance (Any): The object to check.
        _type (type | types.GenericAlias | types.UnionType): 
               The type to check against, can be a simple type, generic type (like list[int]),
               or a union type (like int | str).
               
    Returns:
        bool: True if instance matches the type specification, False otherwise.
        
    Raises:
        TypeError: If _type is not a valid type.
        AssertionError: If a GenericAlias doesn't have expected attributes.
    """
    # Check that _type is actually a type
    if not isinstance(_type, (
            type,
            types.GenericAlias,
            types.UnionType,
    )):
        raise TypeError("_type must be a type")

    # Handle Union types (int | str)
    if isinstance(_type, types.UnionType):
        return any(type_check(instance, t) for t in _type.__args__)

    # Handle generic types like list[int] or tuple[str,int]
    if isinstance(_type, types.GenericAlias):
        if not hasattr(_type, '__origin__') or not hasattr(_type, '__args__'):
            raise AssertionError(
                "GenericAlias should always have __origin__ and __args__")

        # Check if instance matches the container type
        if not isinstance(instance, _type.__origin__):
            return False
            
        # Special handling for tuples with specific element types
        if isinstance(instance, tuple):
            if len(_type.__args__) != len(instance):
                return False
            return all((type_check(instance[i], _type.__args__[i]))
                       for i in range(len(_type.__args__)))
                       
        # Handle other containers (list, set, etc.)
        return all(type_check(item, _type.__args__[0]) for item in instance)
        
    # Normal isinstance check for simple types
    return isinstance(instance, _type)


def quick_sort(input_list: Sequence, ascending: bool = True):
    """
    Sorts a list using the quick sort algorithm.
    
    This is a recursive implementation of the quick sort algorithm
    that uses the first element as pivot.
    
    Args:
        input_list (Sequence): The list/sequence to sort
        ascending (bool): Sort in ascending order if True, descending if False
        
    Returns:
        list: A new sorted list containing the same elements
    """
    # Base case (when list has 1 or 0 items it's already sorted)
    if len(input_list) < 2:
        return input_list

    pivot = input_list[0]  # Use first element as pivot
    less = []  # Elements less than pivot
    more = []  # Elements greater than or equal to pivot

    # Divide into "less than pivot" and "greater than/equal to pivot"
    for item in input_list[1:]:
        if item < pivot:
            less.append(item)
        else:
            more.append(item)

    # Recursively sort both partitions and combine
    # Reverse the result if descending order is requested
    return (list(quick_sort(less)) + [pivot] +
            list(quick_sort(more)))[::1 if ascending else -1]



def linear_search(input_list: list,
                  value,
                  start=0,
                  stop=9223372036854775807,
                  /):
    """
    Performs a linear search for a value in a list.
    
    Sequentially checks each element in the list until
    it finds a match or reaches the end.
    
    Args:
        input_list (list): The list to search in
        value: The value to search for
        start (int): Starting index for the search
        stop (int): Ending index (exclusive) for the search
            (default is max 64-bit integer to search entire list)
        
    Returns:
        int: Index of the first occurrence of value if found, -1 otherwise
    """
    # Ensure stop doesn't exceed list length
    stop = min(stop, len(input_list))
    
    # Check each element in range
    for n in range(start, stop):
        if input_list[n] == value:
            return n
    return -1






def split_exclude_ANSI(text: str, sep: str | list[str] | tuple[str] = ""):
    """
    Splits a string by separator(s) while preserving ANSI escape sequences.
    
    This is similar to str.split() but keeps ANSI escape codes intact within each
    resulting substring. If separator is empty, splits into individual characters.
    
    Args:
        text (str): The string to split
        sep (str | list[str] | tuple[str]): Separator(s) to split by.
            Can be a string, list of strings, or tuple of strings.
            If empty string, splits into individual characters.
            
    Returns:
        list[str]: List of strings after splitting by separator(s)
        
    Raises:
        TypeError: If sep is not a string, list of strings, or tuple of strings
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
    """
    Returns the largest item in an iterable or the largest of multiple arguments.
    
    Similar to built-in max() but reimplemented to avoid using built-in functions.
    
    Args:
        *args: Either a single iterable or multiple arguments to compare
        
    Returns:
        The largest item
        
    Raises:
        TypeError: If no arguments are provided
    """
    if not args:
        raise TypeError("max expected at least 1 argument, 0 received")
    elif len(args) == 1:
        # If a single argument is provided, treat it as an iterable
        args = args[0]
        if isinstance(args, Iterable):
            args = list(args)
        else:
            return args
            
    # Find the maximum value
    maximum = args[0]
    for n in args:
        if n > maximum:
            maximum = n
    return maximum


def min(*args):
    """
    Returns the smallest item in an iterable or the smallest of multiple arguments.
    
    Similar to built-in min() but reimplemented to avoid using built-in functions.
    
    Args:
        *args: Either a single iterable or multiple arguments to compare
        
    Returns:
        The smallest item
        
    Raises:
        TypeError: If no arguments are provided
    """
    if not args:
        raise TypeError("min expected at least 1 argument, 0 received")
    elif len(args) == 1:
        # If a single argument is provided, treat it as an iterable
        args = args[0]
        if isinstance(args, Iterable):
            args = list(args)
        else:
            return args
            
    # Find the minimum value
    minimum = args[0]
    for n in args:
        if n < minimum:
            minimum = n
    return minimum


def all(*args):
    """
    Returns True if all elements of the iterable are true (or if iterable is empty).
    
    Similar to built-in all() but reimplemented to avoid using built-in functions.
    
    Args:
        *args: Either a single iterable or multiple arguments to check
        
    Returns:
        bool: True if all elements are true, False otherwise
    """
    if not args:
        return True
    elif len(args) == 1:
        # If a single argument is provided, treat it as an iterable
        args = args[0]
        if isinstance(args, Iterable):
            args = list(args)
        else:
            return args
            
    # Check if all elements are true
    for n in args:
        if not n:
            return False
    return True


def any(*args):
    """
    Returns True if any element of the iterable is true.
    
    Similar to built-in any() but reimplemented to avoid using built-in functions.
    
    Args:
        *args: Either a single iterable or multiple arguments to check
        
    Returns:
        bool: True if any element is true, False otherwise
    """
    if not args:
        return False
    elif len(args) == 1:
        # If a single argument is provided, treat it as an iterable
        args = args[0]
        if isinstance(args, Iterable):
            args = list(args)
        else:
            return args
            
    # Check if any element is true
    for n in args:
        if n:
            return True
    return False


def find_all_str(input_str, target_str):
    """
    Find all occurrences of a substring within a string.
    
    This is a manual implementation that doesn't use built-in string methods.
    
    Args:
        input_str (str): The string to search within
        target_str (str): The substring to search for
        
    Returns:
        list: List of starting indices where target_str is found in input_str
    """
    result = []
    current_ptr = 0
    
    # Iterate through each character in the input string
    for n in range(len(input_str)):
        if input_str[n] == target_str[current_ptr]:
            # Current character matches the current position in target
            current_ptr += 1
            
            # If we've matched the entire target string
            if current_ptr == len(target_str):
                # Add the starting position to the result
                result.append(n - current_ptr + 1)
                current_ptr = 0  # Reset to look for next occurrence
        else:
            # Reset the match on any mismatch
            current_ptr = 0
            
    return result
