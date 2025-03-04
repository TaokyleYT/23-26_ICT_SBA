def quick_sort(input_list:list, ascending:bool=True):
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
  return (quick_sort(less) + [pivot] + quick_sort(more))[::1 if ascending else -1]

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
