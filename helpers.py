from collections.abc import Iterable, Sequence  # Import Iterable and Sequence types for type hinting
import time  # For implementing delays in output
import os  # For accessing and manipulating the file system
import sys  # For system-specific parameters and functions
import string  # For string constants and character classifications
import re  # For regular expression operations for string matching

# Platform-specific imports for terminal control to change input mode and handle character printing
if sys.platform == "win32":
    import ctypes  # Required for Windows console control
    import ctypes.wintypes  # Required for Windows data types
else:
    import termios  # For controlling terminal settings on Unix/Linux
    import tty  # For setting terminal to character-by-character input mode

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
    
    printing steps:
    repeat:
        ↟ to the top
        repeat:
            → prints ← ↲
        until reach line that is not yet at their turn to print or after last line
    until everything is printed out
    
    per iteration:
    ```
    ↑→→→
    ↑  ↲
    ↑ ↲
    ↑↲
    ```

    Warning: Multi-line text including ANSI codes may not output as expected, as full
    support would require significantly more complex implementation.

    Args:
        txt (str | Iterable[str] | Iterable[Iterable[str]]): 
            The text to print. Can be a single string, a list of strings, or a nested list of strings.
        end (str): 
            A string to print after the entire text has been animated (default: newline).
        delay (float): 
            The time in seconds between each character print (default: 0.02s).
        line_offset (int): 
            The number of lines to offset the text vertically for animation (default: 1).
        _override (bool): 
            An internal parameter for optimization during recursion to override certain type checks. 
            Not intended for direct use.

    Raises:
        TypeError: If `end` is not a string, `delay` is not a number, or `txt` is not
                    a string or an iterable of strings.

    Returns:
        None
    """

    # Validate input parameters to ensure correct types
    if not isinstance(end, str):
        raise TypeError("end must be a string")
    if not isinstance(delay, (int, float)):
        raise TypeError("delay must be a number")

    # Handle case where no text is provided
    if len(txt) == 0:
        print(end=end)  # Print the "end" string (newline or other)
        return  # Exit function to avoid additional processing


    # Process and validate the input text
    if all(
        (all(isinstance(subchar, str) for subchar in char)  # Ensure nested strings in iterables
         if (isinstance(char, (list, tuple)) and _override)  # Handling nested iterables
         else isinstance(char, str)) 
        for char in txt):  # Ensure all elements are strings
        if all(len(char) == 1 for char in txt):  # If all items are single characters
            txt = (''.join(txt)).split('\n')  # Merge the txt and split it into lines
        else:
            txt = list(txt)  # Convert txt to a list for processing
    else:
        raise TypeError("txt must be a str or iterable of str")  # Raise an error for incorrect types

    # Get terminal size for proper text wrapping
    term_size = os.get_terminal_size()
    txt_lst = []  # Initialize a list to hold processed text lines

    # Process each line for wrapping and animation
    for line in txt:
        if _override:  # Optimization: if already processed
            txt_lst = txt  # Skip additional processing
            break
        if not line:
            txt_lst.append("")  # Handle empty line
            continue  # Continue to next line
        
        # Split line by spaces while excluding ANSI escape sequences
        temp = split_exclude_ANSI(line, " ")
        words: list[str] = [(item if i == len(temp)-1 else item + " ")
                            for i, item in enumerate(temp)]  # Append space to all but last word
        index: int = 0  # Initialize index for processing words

        # Wrap text according to terminal width
        while index < len(words):
            if len(words[index]) > term_size.columns - 1:
                # Break long words that exceed terminal width into chunks
                for wrapped_line in (
                        line[i:i + term_size.columns - 1]
                        for i in range(0, len(line), term_size.columns - 1)):
                    txt_lst.append(wrapped_line)  # Append wrapped line to list
                index += 1
                continue
            # Add words to line until it exceeds terminal width
            txt_lst.append("")  # Start new line
            for i, word in enumerate(words[index:]):
                if len(txt_lst[-1]) + len(word) > term_size.columns - 1:
                    index += i  # Update index for next processing
                    break  # Break word addition
                txt_lst[-1] += word
            else:
                break  # Exit while loop if all words processed
    
    if not _override:
        # Split each processed line into characters while preserving ANSI codes
        txt_lst = [split_exclude_ANSI(line) for line in txt_lst]

    # Truncate text if it exceeds terminal height
    txt_lst, truncated = txt_lst[:term_size.lines - 1], txt_lst[term_size.lines - 1:]

    # Find the maximum line length for animation timing
    max_wordlen = max(len(line) for line in txt_lst)

    # Print spaces for the animation based on the number of lines
    print('\n' * (len(txt_lst)), end='\x1b[A')  # Move cursor up to start animation
    
    # Animate the text character by character
    for i in range(max_wordlen + line_offset * len(txt_lst)):
        # Move cursor up to the top of the animation output
        print("\x1b[A" * (len(txt_lst) - 1), end='')
        time.sleep(delay)  # Pause between characters
        for j, line in enumerate(txt_lst):
            current_char = j * line_offset + 1  # Track the current character position
            # Update lines that need to be redrawn
            if (i - current_char >= 0 and i - current_char < len(line)):
                # Print current character with front effect
                print(
                    "\x1b[" + str(current_char) + "D" +  # Move cursor left to overwrite character
                    line[i - current_char] +  # Print the current character
                    "\x1b[" + str(current_char) + "C" +  # Move cursor right
                    "\b\x1b[B",  # Move cursor to the next line
                    end='',
                    flush=True)  # Ensure immediate printing
            else:
                print("\x1b[B", end='', flush=True)  # Move line without printing
        print("\x1b[A\x1b[C", end='', flush=True)  # Move cursor back up for the next iteration

    time.sleep(delay)  # Additional delay to complete character output
    # Reset cursor position for any following outputs
    print("\x1b[" + str(line_offset * len(txt_lst)) + "D",
          end='\n' if truncated else '',
          flush=True)

    # Recursively handle any truncated text for complete output
    animated_print(truncated, end, delay, line_offset, _override=True)
    return


def animated_input(prompt: str = "",
                   delay: float = 0.01,
                   line_offset: int = 1,
                   single_letter: bool = False,
                   _log: bool = False):
    """
    Animated version of input() that displays a prompt with animation effects.

    This function displays an animated prompt and accepts user input with
    character-by-character animation. Special keys like backspace are handled,
    and ANSI escape sequences in the input are supported.

    Warning: Multi-line prompts including ANSI codes may not output as expected
    due to implementation complexity. Note that the input does not support multi-line input.

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
    # Display the prompt with animated typing effect
    animated_print(prompt, "", delay, line_offset)

    # Get terminal width for text wrapping
    columns = os.get_terminal_size().columns - 2  # Adjust for prompt/other text

    # Set terminal to character-by-character input mode (raw mode)
    if sys.platform == "win32":  # Windows implementation
        dword = ctypes.wintypes.DWORD()
        kernel = ctypes.windll.kernel32
        kernel.GetConsoleMode(kernel.GetStdHandle(-10), ctypes.byref(dword))
        kernel.SetConsoleMode(kernel.GetStdHandle(-10), 0)  # Set to raw mode
        kernel.GetConsoleMode(kernel.GetStdHandle(-11), ctypes.byref(dword))
        kernel.SetConsoleMode(kernel.GetStdHandle(-11), 7)  # Enable ANSI support
    else:  # Unix/Linux implementation
        stdin = sys.stdin.fileno()  # Get standard input file descriptor
        original_term = termios.tcgetattr(stdin)  # Get current terminal attributes
        tty.setcbreak(stdin, termios.TCSANOW)  # Set terminal to raw mode for character input

    # Check if single letter input mode is enabled
    if single_letter:
        if _log:  # If logging is enabled, write to log file
            with open("input_log.txt", "a") as f:
                f.write("\n-----\nInput started (single letter)\n-----\n")
        result = "\n"  # Initialize result with newline

        while result == "\n":  # Await input until a character is provided
            # This loop is to handle Windows stdin buffering issues
            # On Windows, sometimes need to press enter twice due to buffer behavior
            result = sys.stdin.read(1)  # Read one character from stdin
        # Handle keyboard Interrupt (Ctrl+C and Ctrl+D)
        if result in "\x03\x04":
            if _log:  # If logging is enabled, note the event
                with open("input_log.txt", "a") as f:
                    f.write(f"KeyboardInterrupt with {result}\n")
            raise KeyboardInterrupt  # Raise KeyboardInterrupt if Ctrl+C is pressed
        print(result)  # Print the character immediately
        # Restore terminal state
        if sys.platform == "win32":  # Windows restoration
            kernel.SetConsoleMode(kernel.GetStdHandle(-10), dword)
            kernel.SetConsoleMode(kernel.GetStdHandle(-11), dword)
        else:  # Unix/Linux restoration
            termios.tcsetattr(stdin, termios.TCSANOW, original_term)
        if _log:  # Log the submitted input
            with open("input_log.txt", "a") as f:
                f.write(f"submitted {repr(result)} \n")
        return result  # Return the single character

    # Get cursor position for multi-character input
    sys.stdout.write("\x1b[?25l\x1b[6n")  # Hide cursor and request cursor position
    sys.stdout.flush()  # Ensure stdout is updated
    result = sys.stdin.read(1)  # Read initial character
    while not result.endswith("R"):  # Await complete cursor position response
        result += sys.stdin.read(1)  # Append additional read characters

    # Parse cursor position response from terminal
    reg = re.match(r"^\x1b\[(\d*);(\d*)R", result)  # Extract row and column from ANSI response
    ptr = int(reg.groups()[1]) if reg else 1  # Get current cursor position

    # Prepare character sets for animation
    printables = [" "] + list(string.printable)[:-6]  # Include printable ASCII characters
    output = sys.stdout.write  # Alias for writing output

    # Read input character by character until the Enter key
    char = sys.stdin.read(1)  # Read first character
    result = ""  # Input string to gather characters
    ansi = ""  # Holder for ANSI escape sequences

    if _log:  # Log input start
        with open("input_log.txt", "a") as f:
            f.write("\n-----\nInput started\n-----\n")

    # Main input loop
    while char != "\n":  # Continue until Enter key
        # Handle Keyboard Interrupt (Ctrl+C and Ctrl+D)
        if char in "\x03\x04":  # Ctrl+C or Ctrl+D
            if _log:  # Log the keyboard interrupt
                with open("input_log.txt", "a") as f:
                    f.write(f"KeyboardInterrupt with {char}\n")
            raise KeyboardInterrupt
        # Handle backspace character for deleting input
        if char in "\x7f\x08":
            if len(result) > 0:  # If there is a character to backspace
                if _log:  # Log the deletion action
                    with open("input_log.txt", "a") as f:
                        f.write("del\n")
                result = result[:-1]  # Remove last character from result
            
                if ptr % columns != 0:  # If not at start of the line
                    output("\b \b")  # Erase character on same line
                else:  # If at the start of the line
                    output(f"\x1b[F\x1b[{columns-1}G\b \b")  # Move up one line and back to the last character

                sys.stdout.flush()  # Show updated result immediately
                ptr -= 1  # Move cursor back
        else:  # If a normal input character
            if _log:  # Log addition of character
                with open("input_log.txt", "a") as f:
                    f.write(f"add {repr(char)} \n")
            result += char  # Add character to result
            
            if ptr % columns == 0:  # If at end of terminal width
                output(" \n")  # Create a new line to continue input
            
            # Handle ANSI escape sequences explicitly here
            if char == "\x1b":  # Start of ANSI escape sequence
                ansi = char  # Store starting ANSI sequence
            elif ansi:  # Continue building ANSI sequence
                ansi += char
            
            # Determine animation length based on character type
            if char in printables:  # If character is printable
                end_cyc = linear_search(printables, char) + 1  # Index for animation limit
            elif char in "\0 \b\n" or ansi:  # Handle special characters and ANSI
                end_cyc = 0
            else:  # If not special
                end_cyc = len(printables)

            # Animation effect: cycle through characters
            for c in printables[:end_cyc]:  # Show each character in printables
                output(ansi)  # Print any ANSI information
                output(c + "\b")  # Show character then backspace to show just the animated char
                sys.stdout.flush()  # Prompt for immediate output
                time.sleep(delay / 10)  # Shorter sleep for quicker animation

            # Handle final character display
            if ansi == "":
                output(char)  # Print character if no ANSI involved
            elif ansi == "\x1b[" or ansi[-1] < "@" or ansi[-1] > "~":
                pass  # Incomplete ANSI sequence, do nothing
            else:
                output(result + " \b")  # Display result string followed by backspace
                ansi = ""  # Reset ANSI storage for next sequence

            sys.stdout.flush()  # Prompt for immediate output
            ptr += 1  # Increment cursor position

        char = sys.stdin.read(1)  # Read next character

    output("\n")  # Final newline to complete input

    # Restore terminal state to original settings based on platform
    if sys.platform == "win32":  # Windows restoration
        kernel.SetConsoleMode(kernel.GetStdHandle(-10), dword)
        kernel.SetConsoleMode(kernel.GetStdHandle(-11), dword)
    else:  # Unix/Linux restoration
        termios.tcsetattr(stdin, termios.TCSANOW, original_term)

    # Log final result if logging is enabled
    if _log:
        with open("input_log.txt", "a") as f:
            f.write(f"submitted {repr(result)} \n")

    return result  # Return the string input by the user


def quick_sort(input_list: Sequence, ascending: bool = True):
    """
    Sorts a list using the quick sort algorithm.
    
    This is a recursive implementation of the quick sort algorithm that uses
    the first element as the pivot. It creates new lists rather than sorting in-place.

    Args:
        input_list (Sequence): 
            The list or sequence to sort.
        ascending (bool): 
            Sort in ascending order if True, otherwise in descending order (default: True).
        
    Returns:
        list: A new sorted list containing the same elements as `input_list`.
        
    Time Complexity:
        - Average case: O(n log n)
        - Worst case: O(n^2) when the list is already sorted
        
    Space Complexity:
        O(n) due to the creation of new lists during recursion.
    """
    # Base case: If list has 1 or 0 items, it's already sorted
    if len(input_list) < 2:
        return input_list

    pivot = input_list[0]  # Choose the first element as the pivot
    less = []  # List to hold elements less than the pivot
    more = []  # List to hold elements greater than or equal to the pivot

    # Divide the input list into smaller partitions based on the pivot
    for item in input_list[1:]:
        if item < pivot:
            less.append(item)  # Add to "less" if it's smaller than the pivot
        else:
            more.append(item)  # Add to "more" otherwise

    # Recursively sort both partitions and combine them
    # Reverse the result if descending order is requested
    return (list(quick_sort(less)) + [pivot] +
            list(quick_sort(more)))[::1 if ascending else -1]


def linear_search(input_list: list,
                  value,
                  start=0,
                  stop=9223372036854775807,
                  /):  # The '/' indicates that the parameters to the left cannot be passed as keyword arguments.
    """
    Performs a linear search for a value in a list.
    
    Sequentially checks each element in the list until it finds a match or reaches the end.
    Allows specifying a range to search within.

    Args:
        input_list (list): 
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
    # Ensure `stop` does not exceed the length of the list
    stop = min(stop, len(input_list))

    # Check each element from start to stop
    for n in range(start, stop):
        if input_list[n] == value:  # If element matches the searched value
            return n  # Return the index
    return -1  # Return -1 if the value is not found


def split_exclude_ANSI(text: str, sep: str | list[str] | tuple[str] = ""):
    """
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
        >>> split_exclude_ANSI("\x1b[31mHello\x1b[0m World", "")
        ['\x1b[31m', 'Hello, '\x1b[0m', 'World']
        >>> split_exclude_ANSI("\x1b[31mHello\x1b[0m World", " ")
        ['\x1b[31mHello\x1b[0m', 'World']
    """
    # Check the type of `sep` to ensure it is valid
    if not (isinstance(sep, str) or all(isinstance(s, str) for s in sep)):
        raise TypeError(
            f"sep should be either string or an iterable that contains only strings"
        )

    # Handle case where text is empty
    if not text:
        return []  # Return an empty list if there is no text

    # Convert `sep` to a list for uniform handling
    separators = [sep] if isinstance(sep, str) else list(sep)

    # Initialize variables for splitting logic
    result = []  # Resultant list of split strings
    i = 0  # Index to traverse the text
    start = 0  # Start index for current segment
    in_ansi = False  # Flag indicating if we are within an ANSI sequence
    ansi_start = -1  # Start index of the ANSI sequence

    while i < len(text):
        # Check if entering an ANSI escape sequence
        if text[i] == '\x1b' and i + 1 < len(text) and text[i + 1] == '[':
            in_ansi = True  # Set flag indicating we are inside an ANSI sequence
            ansi_start = i  # Mark the start index of the ANSI sequence

        # Check if at the end of an ANSI sequence
        if in_ansi and i > ansi_start + 1 and text[i] > "@" and text[i] < "~":
            in_ansi = False  # Reset flag when we exit the ANSI sequence

        # Split logic outside of ANSI sequences
        if not in_ansi:
            # Special case: if separator is empty, split into individual characters
            if separators == [""]:
                i += 1  # Increment index to read next character
            # Check for any specified separator matches
            for separator in separators:
                if i + len(separator) <= len(text) and text[i:i + len(separator)] == separator:
                    result.append(text[start:i])  # Append current segment
                    i += len(separator) - 1  # Move index past the separator
                    start = i + 1  # Update start for the next segment
                    break  # Break to re-check for more separators as needed

        i += 1  # Advance the iterator

    # Add the last segment post-loop
    result.append(text[start:])  

    # Remove any trailing empty strings in the result
    while result and result[-1] == "":
        del result[-1]  # Delete empty strings at the end of the list

    return result  # Return the list of split sections


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
    if not args:  # Check if no arguments were received
        raise TypeError("max expected at least 1 argument, 0 received") 
        
    elif len(args) == 1:  # Handle single iterable input
        args = args[0] 
        if isinstance(args, Iterable):  # Convert to list if it's an iterable
            args = list(args)
        else:
            return args  # Directly return the value if it's a single non-iterable argument

    maximum = args[0]  # Initialize maximum with the first argument
    for n in args:  # Loop to find maximum
        if n > maximum:  # If current value is greater than maximum
            maximum = n  # Update maximum
    return maximum  # Return the largest value found


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
    if not args:  # Check if no arguments were received
        raise TypeError("min expected at least 1 argument, 0 received")

    elif len(args) == 1:  # Handle single iterable input
        args = args[0]
        if isinstance(args, Iterable):  # Convert to list if it's an iterable
            args = list(args)
        else:
            return args  # Directly return the value if it's a single non-iterable argument

    minimum = args[0]  # Initialize minimum with the first argument
    for n in args:  # Loop to find minimum
        if n < minimum:  # If current value is smaller than minimum
            minimum = n  # Update minimum
    return minimum  # Return the smallest value found


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
    if not args:  # Check if no arguments were received
        return True  # Return True since empty iterables are considered "all true"
        
    elif len(args) == 1:  # Handle single iterable input
        args = args[0]
        if isinstance(args, Iterable):  # Convert iterable to list
            args = list(args)
        else:
            return args  # Directly return value if it's a single non-iterable argument

    for n in args:  # Iterate through each argument
        if not n:  # If any argument evaluates to False
            return False  # return False
    return True  # All elements are true


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
    if not args:  # Check if no arguments were received
        return False  # Return False since empty iterables are considered "no true values"
        
    elif len(args) == 1:  # Handle single iterable input
        args = args[0]
        if isinstance(args, Iterable):  # Convert iterable to list
            args = list(args)
        else:
            return args  # Directly return value if it's a single non-iterable argument

    for n in args:  # Iterate through each argument
        if n:  # If any argument evaluates to True
            return True  # return True
    return False  # Neither element is true