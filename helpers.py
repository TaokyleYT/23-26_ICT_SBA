from collections.abc import Iterable, Sequence
import time
import os
import sys
import string
import re
# Platform-specific imports for terminal control
if sys.platform == "win32":
    import ctypes
    import ctypes.wintypes
else:
    import termios
    import tty


def animated_print(txt: str | Iterable[str] | Iterable[Iterable[str]] = "",
                   end: str = "\n",
                   delay: float = 0.02,
                   line_offset: int = 1,
                   _override: bool = False):
    """
    Prints text with an animation effect, simulating a typewriter-style output.

    This function displays text character by character with a delay between each character,
    creating a typewriter-like animation effect. It handles multi-line text, text wrapping,
    and preserves ANSI escape sequences for colored or formatted text.

    Warning: Multi-line text including ANSI codes may not output as expected, as full
    support would require significantly more complex implementation.

    Args:
        txt (str | Iterable[str] | Iterable[Iterable[str]]): 
            The text to print. Can be a string, list of strings, or nested list of strings.
        end (str): 
            String to print after the entire text has been animated (default: newline).
        delay (float): 
            Time in seconds between each character print (default: 0.02s).
        line_offset (int): 
            Number of lines to offset the text vertically (default: 1).
            Controls the spacing between animated lines.
        _override (bool): 
            Internal parameter for optimization during recursion and to override
            certain type checks. Not intended for direct use.

    Raises:
        TypeError: If end is not a string, delay is not a number, or txt is not
                  a string or iterable of strings.

    Returns:
        None
    """

    # Validate input parameters
    if not isinstance(end, str):
        raise TypeError("end must be a string")
    if not isinstance(delay, (int, float)):
        raise TypeError("delay must be a number")

    # Handle empty text case
    if len(txt) == 0:
        print(end=end)
        return  #if need print nothing, prints nothing
    else:
        print()
        # Print an initial newline to create space for animation

    # Process and validate the input text
    if all(
        (all(isinstance(subchar, str) for subchar in char)\
         if (isinstance(char, (list, tuple)) and _override)\
         else isinstance(char, str))\
             for char in txt):
        if all(len(char) == 1 for char in txt):
            # It's a str, convert to lines
            txt = (''.join(txt)).split('\n')
        else:
            txt = list(txt)
    else:
        raise TypeError("txt must be a str or iterable of str")

    # Get terminal size for text wrapping
    term_size = os.get_terminal_size()
    txt_lst = []

    # Process each line for wrapping and animation
    for line in txt:
        if _override: #optimization by skipping an O(n^3)? algorithm if input already processed
            txt_lst = txt
            break
        if not line:
            txt_lst.append("")  #newline, use empty string to replace
            continue
        temp = split_exclude_ANSI(
            line, " ")  # Split line by spaces, preserving ANSI codes
        words: list[str] = [(item if i == len(temp) else item + " ")
                            for i, item in enumerate(temp)]
        # Wrap text to terminal width
        index: int = 0
        while index < len(words):
            if len(words[index]) > term_size.columns - 1:
                # Handle words longer than terminal width by breaking them into chunks
                for warpped_line in (
                        line[i:i + term_size.columns - 1]
                        for i in range(0, len(line), term_size.columns - 1)):
                    txt_lst.append(warpped_line)
                index += 1
                continue
            # Add words to line until it would exceed terminal width
            txt_lst.append("")
            for i, word in enumerate(words[index:]):
                if len(txt_lst[-1]) + len(word) > term_size.columns - 1:
                    index += i
                    break  #break for loop
                txt_lst[-1] += word
            else:
                break  # Break while loop if all words processed
    if not _override:
        # Split each line into characters while preserving ANSI codes
        # ANSI codes are technically >=4 characters long, but print as 0 characters
        # Preserving them prevents them from being broken and displayed as raw codes
        txt_lst = [split_exclude_ANSI(line) for line in txt_lst]

    # Truncate text if it would exceed terminal height
    txt_lst, truncated = txt_lst[:term_size.lines -
                                 1], txt_lst[term_size.lines - 1:]

    # Find the maximum line length (aka width of animation rectangle) for animation timing
    max_wordlen = max(len(line) for line in txt_lst)

    # Create space for the animation
    print('\n' * (len(txt_lst)), end='\x1b[A') # Print newlines then move cursor up

    # Animate text character by character
    for i in range(max_wordlen + line_offset * len(txt_lst)):
        print("\x1b[A" * (len(txt_lst) - 1), end='')
        time.sleep(delay)
        for j, line in enumerate(txt_lst):
            current_char = j * line_offset + 1
            # Determine if this line needs updating at this step
            if (i - current_char >= 0 and i - current_char < len(line)):
                # Print current character with front effect
                print(
                    "\x1b[" + str(current_char) + "D" +  # Move cursor left
                    line[i - current_char] + #print current character
                    "\x1b[" + str(current_char) + "C" + # Move cursor right
                    "\b\x1b[B", #move cursor to the next line
                    end='',
                    flush=True)
            else:
                print("\x1b[B", end='', flush=True) #go to the next line without printing anything
        print("\x1b[A\x1b[C", end='', flush=True) #move cursor up and then right
    time.sleep(delay)
    # Reset cursor position
    print("\x1b[" + str(line_offset * len(txt_lst)) + "D",
          end='',
          flush=True)

    # Recursively handle any truncated text
    animated_print(truncated, end, delay, line_offset, _override=True)
    return
    #deprecated cuz buggy
    '''
    elif front_effect[1] == 0:
        for i in range(len(txt)):
            time.sleep(delay)
            print(front_effect[0][i % len(front_effect[0])], end='', flush=True)
        print("\x1b[G", end='')
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


def animated_input(prompt: str = "",
                   delay: float = 0.01,
                   front_effect="",
                   line_offset: int = 1,
                   single_letter:bool = False,
                   _log: bool = False):
    """
    Animated version of input() that displays a prompt with animation effects.

    This function displays an animated prompt and then accepts user input with
    character-by-character animation as the user types. It handles special keys
    like backspace and supports ANSI escape sequences in the input.

    Warning: Multi-line prompts including ANSI codes may not output as expected due to
    implementation complexity. ANSI codes in user input are properly handled.
    Does NOT support multi-line input, just like the normal input() function.

    Args:
        prompt (str): 
            Text to display before the input field.
        delay (float): 
            Time in seconds between character animations (default: 0.01s).
        front_effect (str): 
            String to display at front of animated text (currently unused).
        line_offset (int): 
            Number of lines to offset the text vertically (default: 1).
        single_letter (bool): 
            Whether to accept a single letter input and return immediately (default: False).
            When True, skips animation and returns after a single keypress.
        _log (bool): 
            Whether to log input for debugging purposes (internal use, default: False).
            When enabled, writes input events to "input_log.txt".

    Returns:
        str: The user's input string (without the trailing newline).
    """
    # Display the prompt with animation
    animated_print(prompt, "", delay, line_offset)


    # Get terminal width for text wrapping
    columns = os.get_terminal_size().columns - 2

    # Set terminal to character-by-character input mode (raw mode)
    if sys.platform == "win32":
        # Windows implementation using ctypes
        dword = ctypes.wintypes.DWORD()
        kernel = ctypes.windll.kernel32
        kernel.GetConsoleMode(kernel.GetStdHandle(-10), ctypes.byref(dword))
        kernel.SetConsoleMode(kernel.GetStdHandle(-10), 0)
        kernel.GetConsoleMode(kernel.GetStdHandle(-11), ctypes.byref(dword))
        kernel.SetConsoleMode(kernel.GetStdHandle(-11), 7)
    else:
        # Unix/Linux implementation using termios
        stdin = sys.stdin.fileno()
        original_term = termios.tcgetattr(stdin)
        tty.setcbreak(stdin, termios.TCSANOW)

    # Handle single letter input mode (no animation)
    if single_letter:
        if _log:
            with open("input_log.txt", "a") as f:
                f.write("\n-----\nInput started (single letter)\n-----\n")
        result = "\n"
        while result == "\n":
            # Loop to handle Windows stdin buffering issues
            # On Windows, sometimes need to press enter twice due to buffer behavior
            result = sys.stdin.read(1)
        # Handle Ctrl+C and Ctrl+D
        if result in "\x03\x04":
            if _log:
                with open("input_log.txt", "a") as f:
                    f.write(f"KeyboardInterrupt with {result}\n")
            raise KeyboardInterrupt
        print(result, end='')
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

    # Get cursor position for multi-character input mode
    sys.stdout.write("\x1b[?25l\x1b[6n")  # Hide cursor and request position
    sys.stdout.flush()
    result = sys.stdin.read(1)
    while not result.endswith("R"):
        result += sys.stdin.read(1)

    # Parse cursor position response from termina
    reg = re.match(r"^\x1b\[(\d*);(\d*)R", result)
    ptr = int(reg.groups()[1]) if reg else 1

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
            if _log:
                with open("input_log.txt", "a") as f:
                    f.write(f"KeyboardInterrupt with {char}\n")
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
                output(result + " \b")
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
    if not (isinstance(sep, str) or all(isinstance(s, str) for s in sep)):
        raise TypeError(
            f"sep should be either string or an iterable that contains only strings"
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
        if in_ansi and i > ansi_start + 1 and text[i] > "@" and text[i] < "~":
            in_ansi = False

        # Only check for separators if we're not in an ANSI sequence
        if not in_ansi:
            if separators == [""]:
                i += 1
            # Check if current position matches any separator
            for separator in separators:
                if i + len(separator) <= len(text) and\
                    text[i:i + len(separator)] == separator:
                    result.append(text[start:i])
                    i += len(separator) - 1  # -1 because we'll increment i at the end of the loop
                    start = i + 1
                    break

        i += 1

    # Add the last segment
    result.append(text[start:])

    while result[-1] == "":
        del result[
            -1]  #in case null strings showed up at the end by some separator mess (causes trouble)

    return result


def max(*args):
    """
    Returns the largest item in an iterable or the largest of multiple arguments.

    Similar to built-in max() but reimplemented to avoid using built-in functions.

    Args:
        *args: Either a single iterable or multiple arguments to compare.

    Returns:
        The largest item.

    Raises:
        TypeError: If no arguments are provided.

    Example:
        >>> max(1, 2, 3)
        3
        >>> max([1, 2, 3])
        3
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
        *args: Either a single iterable or multiple arguments to compare.

    Returns:
        The smallest item.

    Raises:
        TypeError: If no arguments are provided.

    Example:
        >>> min(1, 2, 3)
        1
        >>> min([1, 2, 3])
        1
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
        *args: Either a single iterable or multiple arguments to check.

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
    If the iterable is empty, returns False.

    Args:
        *args: Either a single iterable or multiple arguments to check.

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
