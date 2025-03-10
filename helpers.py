from collections.abc import Iterable, Sequence
from typing import Any
import types
import time
import os

def animated_input(prompt:str, delay:float=0.02, front_effect="", line_offset:int=1):
    animated_print(prompt, "", delay, front_effect, line_offset)
    return input()


def animated_print(txt, end: str = '\n', delay: float = 0.02, front_effect: str = '', line_offset: int = 1):
    if len(txt) == 0:
        return
    if all(
        (all(isinstance(subchar, str) for subchar in char)\
         if isinstance(char, (list, tuple))\
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
        if len(line) == 0:
            txt_lst.append("")
            continue
        for warpped_line in (line[i:i+term_size.columns] for i in range(0, len(line), term_size.columns)):
            txt_lst.append(warpped_line)
    txt_lst = list(map(split_exclude_ANSI, txt_lst))
    txt_lst, truncated = txt_lst[:term_size.lines-1], txt_lst[term_size.lines-1:]
    max_wordlen = max([len(line) for line in txt_lst])
    print('\n' * (len(txt_lst)), end='\x1b[A')
    for i in range(max_wordlen + line_offset * (len(txt_lst))):
        print("\x1b[A"*(len(txt_lst)-1), end='')
        time.sleep(delay)
        for j, line in enumerate(txt_lst):
            current_char = j * line_offset + 1
            print(' '*len(front_effect)+"\x1b[D"*len(front_effect), end='')
            if (i - current_char >= 0 
                and i - current_char < len(line)): #needs animated update
                print("\x1b[" + str(current_char) + "D" +
                    line[i - current_char] +
                    front_effect + "\x1b[D"*len(front_effect) +
                    "\x1b[" + str(current_char) + "C" + "\b\x1b[1B",
                    end='',
                    flush=True)
            else:
                print("\x1b[1B", end='', flush=True)
        print("\x1b[1A\x1b[1C", end='', flush=True)
    time.sleep(delay)
    print("\x1b[" + str(line_offset * len(txt_lst)) + "D", end=end, flush=True)
    animated_print(truncated, end, delay, front_effect, line_offset)
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


types_tuple = (
    type,
    types.GenericAlias,
    types.UnionType,
)

def type_check(instance: Any, _type: type | types.GenericAlias | types.UnionType) -> bool:

    if not isinstance(_type, types_tuple):
        raise TypeError("_type must be a type")

    if isinstance(_type, types.UnionType):
        return any(type_check(instance, t) for t in _type.__args__)

    #check if typ is sth like list[int] or tuple[str,int]
    if isinstance(_type, types.GenericAlias):
        if hasattr(_type, '__origin__') and hasattr(_type, '__args__'):
            if not isinstance(instance, _type.__origin__):
                return False
            if isinstance(instance, tuple):
                if len(_type.__args__) != len(instance):
                    return False
                return all((type_check(instance[i], _type.__args__[i])) for i in range(len(_type.__args__)))
            return all(
                type_check(item, _type.__args__[0]) for item in instance)
        else:
            raise AssertionError("GenericAlias should always have __origin__ and __args__")

    # normal check
    # check if instance is a subclass of typ
    if isinstance(instance, _type):
        return True
    return False

def quick_sort(input_list:Sequence, ascending:bool=True):
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

    pivot = input_list[0] # First pivot
    less = []
    more = []

    # Divide into 3 parts
    for item in input_list[1:]:
        if item < pivot:
            less.append(item)
        else:
            more.append(item)

    # Recurse + conquer + return
    return (list(quick_sort(less)) + [pivot] + list(quick_sort(more)))[::1 if ascending else -1]

def binary_search(input_list:list, value, /):
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
        raise ValueError("Binary_search: input list is not sorted what are you doing")
    while start <= end:
        mid = (start + end) // 2
        if value == input_list[mid]:
            return mid
        elif value < input_list[mid]:
            end = mid - 1
        else:
            start = mid + 1
    return -1

def linear_search(input_list:list, value, start=0, stop=9223372036854775807, /):
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
    if stop > len(input_list):
        stop = len(input_list)
    for n in range(start, stop):
        if input_list[n] == value:
            return n
    return -1

def is_sorted(input_list:list, default=1):
    """
    Check if input list is sorted.
    
    Args:
        input_list: List to check
        default: Default value to return if list is too short
    
    Returns:
        1 if sorted in ascending order, -1 if sorted in descending order, 0 if not sorted
    """
    ascending = True
    descending = True
    if len(input_list) < 2:
        return default
    for n in range(len(input_list)-1):
        if input_list[n] > input_list[n+1]:
            ascending = False
        elif input_list[n] < input_list[n+1]:
            descending = False
        if not (ascending or descending):
            break
    return 1 if ascending else (-1 if descending else 0)

def repeat_str_to_len(word: str, length: int, start_index=0) -> tuple[str, int]:
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
    if not isinstance(length, int) and length >= 0:
        raise TypeError("length must be a positive int")
    if not isinstance(start_index, int) and start_index >= 0 and start_index < len(word):
        raise TypeError("start_index must be a positive int which less than the length of word")
    if length == 0:
        return '', 0
    words = word*(-((-length)//len(word))+1) #word * (ceil division + 1)
    return words[start_index:length+start_index], (length+start_index)%len(word)

def split_exclude_ANSI(text:str, sep:str|list[str]|tuple[str]=""):
    return text.split(sep) if sep else list(text)
    splitted_list = []
    if not type_check(sep, str|list[str]|tuple[str]):
        raise TypeError(f"sep should be either string or list or tuple that contains only strings, not {type(sep)}")
    if isinstance(sep, str):
        pass
    else:
        match_ptr = 0
        last_ptr = 0
        checking = linked_list()
        for idx in range(len(text)):
            if len(checking) > 0:
                for check_idx in range(len(checking)):
                    word = sep[checking[check_idx][0]]
                    if text[idx] == word:
                        checking[check_idx][1] += 1
                        if checking[check_idx][1] == len(word):
                            splitted_list.append(text[last_ptr:idx-len(word)+1])
                            last_ptr = idx+1
                            checking = linked_list()
                    else:
                        checking.remove(check_idx)
            for check_idx in range(len(sep)):
                if text[idx] == sep[check_idx]:
                    checking.append([check_idx, 1])
            if text[idx] == sep[match_ptr]:
                match_ptr += 1
                if match_ptr == len(sep):
                    splitted_list.append(text[last_ptr:idx-len(sep)+1])
                    match_ptr = 0
                    last_ptr = idx+1
        splitted_list.append(text[last_ptr:])
    return splitted_list
                
    

def replace_word(text, target_word, replacement_word, case_sensitive=False):
    """
    Replace occurrences of target_word with replacement_word in text.
    
    Args:
        text: Text to modify
        target_word: Word to replace
        replacement_word: Replacement word
        case_sensitive: Whether to match case
    
    Returns:
        Modified text
    """
    if not text or not target_word:
        return text
    
    words = text.split()
    result = []
    
    for word in words:
        if (case_sensitive and word == target_word) or (not case_sensitive and word.lower() == target_word.lower()):
            result.append(replacement_word)
        else:
            result.append(word)
            
    return ' '.join(result)

def max(*args):
    if len(args) == 0:
        raise TypeError("max expected at least 1 argument, 0 received")
    elif len(args) == 1 and isinstance(args, Iterable):
        args = args[0]
    maximum = args[0]
    for n in args:
        if n > maximum:
            maximum = n
    return maximum

def min(*args):
    if len(args) == 0:
        raise TypeError("min expected at least 1 argument, 0 received")
    elif len(args) == 1 and isinstance(args, Iterable):
        args = args[0]
    minimum = args[0]
    for n in args:
        if n < minimum:
            minimum = n
    return minimum

def all(*args):
    if len(args) == 0:
        raise TypeError("all expected at least 1 argument, 0 received")
    elif len(args) == 1 and isinstance(args, Iterable):
        args = args[0]
    for n in args:
        if not n:
            return False
    return True

def any(*args):
    if len(args) == 0:
        raise TypeError("all expected at least 1 argument, 0 received")
    elif len(args) == 1 and isinstance(args, Iterable):
        args = args[0]
    for n in args:
        if n:
            return True
    return False


class linked_list:
    """A simple linked list implementation."""

    class Node:
        """Node for linked list implementation."""
        def __init__(self, value):
            self.value = value
            self.next: linked_list.Node | None = None

    
    def __init__(self, iterable=()):
        """
        Initialize a linked list.
        
        Args:
            iterable: Initial values for the list
        """
        self.head = None
        for item in iterable:
            self.append(item)
    
    def copy(self):
        """
        Create a copy of the linked list.
        
        Returns:
            A new linked list with the same values
        """
        return linked_list(list(self))
    
    def insert(self, value, index):
        """
        Insert a value at the specified index.
        
        Args:
            value: Value to insert
            index: Position to insert at
        """
        if index == 0:
            new_node = linked_list.Node(value)
            new_node.next = self.head
            self.head = new_node
            return

        current = self.head
        position = 0
        
        while current and position < index - 1:
            current = current.next
            position += 1
            
        if current:
            new_node = linked_list.Node(value)
            new_node.next = current.next
            current.next = new_node
        else:
            # If the index is beyond the end of the list, append
            self.append(value)
    
    def append(self, value):
        """
        Append a value to the end of the list.
        
        Args:
            value: Value to append
        """
        new_node = linked_list.Node(value)
        
        if not self.head:
            self.head = new_node
            return
            
        current = self.head
        while current.next:
            current = current.next
            
        current.next = new_node
    
    def pop(self):
        """
        Remove the first element from the list.
        
        Returns:
            The removed value
        """
        if not self.head:
            return None
            
        value = self.head.value
        self.head = self.head.next
        return value
    
    def deq(self):
        """
        Remove the last element from the list.
        
        Returns:
            The removed value
        """
        if not self.head:
            return None
            
        if not self.head.next:
            value = self.head.value
            self.head = None
            return value
            
        current = self.head
        while current.next and current.next.next:
            current = current.next
            
        value = current.next.value
        current.next = None
        return value
    
    def remove(self, index):
        """
        Remove the element at the specified index.
        
        Args:
            index: Index of element to remove
        
        Returns:
            The removed value
        """
        if not self.head:
            return None
            
        if index == 0:
            return self.pop()
            
        current = self.head
        position = 0
        
        while current.next and position < index - 1:
            current = current.next
            position += 1
            
        if current.next:
            value = current.next.value
            current.next = current.next.next
            return value
        return None
    
    def remove_by_content(self, value):
        """
        Remove the first occurrence of value.
        
        Args:
            value: Value to remove
        
        Returns:
            True if removed, False otherwise
        """
        if not self.head:
            return False
            
        if self.head.value == value:
            self.head = self.head.next
            return True
            
        current = self.head
        while current.next:
            if current.next.value == value:
                current.next = current.next.next
                return True
            current = current.next
            
        return False
    
    def index(self, value):
        """
        Find the index of the first occurrence of value.
        
        Args:
            value: Value to find
        
        Returns:
            Index of value if found, -1 otherwise
        """
        if not self.head:
            return -1
            
        current = self.head
        position = 0
        
        while current:
            if current.value == value:
                return position
            current = current.next
            position += 1
            
        return -1
    
    def __getitem__(self, index):
        """
        Get item at index.
        
        Args:
            index: Index of item
        
        Returns:
            Item at index
        
        Raises:
            IndexError: If index is out of range
        """
        if isinstance(index, int):
            if index < 0:
                index = len(self) + index
                
            if index < 0:
                raise IndexError("Linked List index out of range")
                
            current = self.head
            position = 0
            
            while current and position < index:
                current = current.next
                position += 1
                
            if current:
                return current.value
            raise IndexError("Linked List index out of range")
        elif isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            result = []
            
            current = self.head
            position = 0
            
            while current and position < start:
                current = current.next
                position += 1
                
            while current and position < stop:
                if (position - start) % step == 0:
                    result.append(current.value)
                current = current.next
                position += 1
                
            return result
        else:
            raise TypeError(f"Linked list indices must be integers or slices, not '{type(index).__name__}'")
    
    def __setitem__(self, index, value):
        """
        Set item at index.
        
        Args:
            index: Index of item
            value: New value
        
        Raises:
            IndexError: If index is out of range
        """
        if not isinstance(index, int):
            raise TypeError(f"Linked list indices must be integers, not '{type(index).__name__}'")
            
        if index < 0:
            index = len(self) + index
            
        if index < 0:
            raise IndexError("Linked List index out of range")
            
        current = self.head
        position = 0
        
        while current and position < index:
            current = current.next
            position += 1
            
        if current:
            current.value = value
        else:
            raise IndexError("Linked List index out of range")
    
    def __len__(self):
        """
        Get the length of the list.
        
        Returns:
            Number of elements in the list
        """
        count = 0
        current = self.head
        
        while current:
            count += 1
            current = current.next
            
        return count
    
    def __str__(self):
        """
        Get string representation of the list.
        
        Returns:
            String representation
        """
        if not self.head:
            return "Linked []"
            
        result = ["Linked ["]
        current = self.head
        
        while current:
            result.append(repr(current.value))
            if current.next:
                result.append(" -> ")
            current = current.next
            
        result.append("]")
        return "".join(result)
    
    def __repr__(self):
        """
        Get string representation of the list.
        
        Returns:
            String representation
        """
        return self.__str__()
    
    def __iter__(self):
        """
        Get iterator for the list.
        
        Returns:
            Iterator
        """
        current = self.head
        while current:
            yield current.value
            current = current.next
    
    def __add__(self, other):
        """
        Concatenate two lists.
        
        Args:
            other: List to concatenate
        
        Returns:
            New concatenated list
        """
        result = self.copy()
        
        if isinstance(other, linked_list):
            for item in other:
                result.append(item)
        elif isinstance(other, (list, tuple)):
            for item in other:
                result.append(item)
        else:
            raise TypeError(f"Cannot add object of type '{type(other).__name__}' to linked_list")
            
        return result
    
    def __iadd__(self, other, /):
        """
        Concatenate other list to this list.
        
        Args:
            other: List to concatenate
        
        Returns:
            None
        """
        if isinstance(other, linked_list):
            for item in other:
                self.append(item)
        elif isinstance(other, (list, tuple)):
            for item in other:
                self.append(item)
        else:
            raise TypeError(f"Cannot add object of type '{type(other).__name__}' to linked_list")
