text = "ICT is the technology required for information processing for the creation, manipulation, storage, retrieval and communication of information.  They are of immense value in a world in which there is an “information explosion”, and where knowledge is complex, ever-changing and cross-disciplinary in nature." #43 words

#Preprocess Text
#Convert text to lowercase
text = text.lower()

#Remove punctuation marks
text = "".join(char for char in text if char==" " or ("0"<=char and "9">=char) or ("A"<=char and "Z">=char) or ("a"<=char and "z">=char)).replace("  ", " ")

#Split into Words
text = text.split(" ")

#Sorting
def quick_sort(input_list:list):
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
  return quick_sort(less) + [pivot] + quick_sort(more)

text = quick_sort(text)

#Count Word Frequencies
words = [text[0]]
frequencies = [1]
for n in text[1:]:
  if n == words[-1]:
    frequencies[-1] += 1
  else:
    frequencies.append(1)
    words.append(n)
    
print("frequencies:")
for n in range(len(words)):
  print(f"{words[n]}: {frequencies[n]}")