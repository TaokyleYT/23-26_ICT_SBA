from collections.abc import Sequence


def quick_sort(input_list:Sequence, ascending:bool=True):
  #base case (when list have 1 or 0 item its sorted)
  if len(input_list) < 2:
      return input_list

  pivot = input_list[0] #first pivot
  less = []
  more = []

  #divide into 3 parts
  for item in input_list[1:]:
      if item < pivot:
          less.append(item)
      else:
          more.append(item)

  #recurse + conquer + return
  return (list(quick_sort(less)) + [pivot] + list(quick_sort(more)))[::1 if ascending else -1]

def binary_search(input_list:list, value, /):
    start = 0
    end = len(input_list)
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
    if stop > len(input_list):
        stop = len(input_list)
    for n in range(start, stop):
        if input_list[n] == value:
            return n
    return -1

def is_sorted(input_list:list, default=1):
    """check if input list is sorted, if input list is shorter than 2 values (both sorted in ascending and decending order), default will be returned instead"""
    ascending = True
    decending = True
    if len(input_list) < 2:
        return default
    for n in range(len(input_list)-1):
        if input_list[n] > input_list[n+1]:
            ascending = False
        elif input_list[n] < input_list[n+1]:
            decending = False
        if not (ascending or decending):
            break
    return ascending-decending

def repeat_str_to_len(word: str, length: int, start_index=0) -> tuple[str, int]:
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

def replace_word(text, target_word, replacement_word):
    if not text or not target_word:
        return text

    words = text.split()
    target_word = target_word.lower()

    for i, word in enumerate(words):
        if word.lower() == target_word:
            words[i] = replacement_word

    return ' '.join(words)


def list_insert(input_list:list, index:int, object, /):
    input_list.append(input_list[-1])
    for n in range(len(input_list)-1, index, -1):
        input_list[n+1] = input_list[n]
    input_list[index] = object


class linked_list:
    class node:
        def __init__(self, data):
            self.data = data
            self.next: linked_list.node|None = None

    def __init__(self, iterable=()):
        self.head = None
        for n in iterable:
            self.append(n)

    
    def insert(self, data, index):
        if index == 0:
            new_node = self.node(data)
            new_node.next = self.head
            self.head = new_node
            return

        position = 0
        current_node = self.head
        while current_node is not None and position + 1 != index:
            position += 1
            current_node = current_node.next

        if current_node is not None:
            new_node = self.node(data)
            new_node.next = current_node.next
            current_node.next = new_node
        else:
            print("Index not present")

    
    def append(self, data):
        new_node = self.node(data)
        if self.head is None:
            self.head = new_node
            return

        current_node = self.head
        while current_node.next:
            current_node = current_node.next

        current_node.next = new_node



    def pop(self):
        if self.head is None:
            return

        self.head = self.head.next


    def deq(self):
        """dequeue? idk it removes the last element from list, I got the name deq from ICT textbook"""
        if self.head is None:
            return


        if self.head.next is None:
            self.head = None
            return

        current_node = self.head
        while current_node.next and current_node.next.next:
            current_node = current_node.next

        content = current_node.next.data
        current_node.next = None
        
        return content

    
    def remove(self, index):
        if self.head is None:
            return

        if index == 0:
            self.pop()
            return

        current_node = self.head
        position = 0
        while current_node is not None and current_node.next is not None and position + 1 != index:
            position += 1
            current_node = current_node.next

        if current_node is not None and current_node.next is not None:
            current_node.next = current_node.next.next
        else:
            print("Index not present")


    def remove_by_content(self, data):
        current_node = self.head

        if current_node is not None and current_node.data == data:
            self.pop()
            return


        while current_node is not None and current_node.next is not None:
            if current_node.next.data == data:
                current_node.next = current_node.next.next
                return
            current_node = current_node.next


        print("Node with the given data not found")

    def index(self, index):
        current_node = self.head
        current_idx = 0

        if current_node is not None and current_node.data == data:
            return 0
        while current_node is not None and current_node.next is not None:
            if current_node.next.data == data:
                return current_idx
            current_node = current_node.next
            current_idx += 1

    def sort(self, /):
        self = linked_list(quick_sort(self))

    
    def __getitem__(self, index, /):
        if index < 0:
            index = len(self) + index
        current_node = self.head
        for n in range(index):
            if not current_node.next:
                raise IndexError("Linked List index out of range")
            current_node = current_node.next
        

    def __setitem__(self, key, value, /):
        current_node = self.head
        position = 0
        while current_node is not None and position != key:
            position += 1
            current_node = current_node.next

        if current_node is not None:
            current_node.data = value
        else:
            raise IndexError("Linked List index out of range")

    
    def __len__(self):
        size = 0
        current_node = self.head
        while current_node:
            size += 1
            current_node = current_node.next
        return size

    def __str__(self):
        if not self.head:
            return "[]"
        content = f"[{str(self.head.data)}"
        current_node = self.head.next
        while current_node:
            content += f" -> {repr(current_node.data)}"
            current_node = current_node.next
        content += "]"
        return content

    def __iter__(self, /):
        current_node = self.head
        while current_node:
            yield current_node.data
            current_node = current_node.next

