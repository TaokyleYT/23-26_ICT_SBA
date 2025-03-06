
from collections.abc import Sequence, Iterable
import time
import os

def animated_print(txt, delay=0.02, front_effect='', next_line_char_delay=1, end='\n'):
    """
    Print text with animation effect.
    
    Args:
        txt: Text to print
        delay: Delay between characters
        front_effect: Effect to show before text
        next_line_char_delay: Delay for new lines
        end: End character
    """
    if isinstance(txt, str):
        txt_lines = txt.split('\n')
    elif all(isinstance(char, str) for char in txt):
        txt_lines = ''.join(txt).split('\n')
    else:
        raise TypeError("txt must be a str or iterable of str")
        
    if not isinstance(delay, (int, float)):
        raise TypeError("delay must be a number")
    if not isinstance(front_effect, str):
        raise TypeError("front_effect must be a str")
        
    for line in txt_lines:
        for char in line:
            print(char, end='', flush=True)
            time.sleep(delay)
        print(end='\n')
    
    print(end=end, flush=True)

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

class Node:
    """Node for linked list implementation."""
    def __init__(self, value):
        self.value = value
        self.next = None

class linked_list:
    """A simple linked list implementation."""
    
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
            new_node = Node(value)
            new_node.next = self.head
            self.head = new_node
            return

        current = self.head
        position = 0
        
        while current and position < index - 1:
            current = current.next
            position += 1
            
        if current:
            new_node = Node(value)
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
        new_node = Node(value)
        
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
    
    def __iadd__(self, other):
        """
        Concatenate other list to this list.
        
        Args:
            other: List to concatenate
        
        Returns:
            Self
        """
        if isinstance(other, linked_list):
            for item in other:
                self.append(item)
        elif isinstance(other, (list, tuple)):
            for item in other:
                self.append(item)
        else:
            raise TypeError(f"Cannot add object of type '{type(other).__name__}' to linked_list")
            
        return self
