text = "ICT is the technology required for information processing for the creation, manipulation, storage, retrieval and communication of information.  They are of immense value in a world in which there is an “information explosion”, and where knowledge is complex, ever-changing and cross-disciplinary in nature." #43 words
#Count words

def word_count():
   word = len("".join(char for char in text if char==" " or ("0"<=char and "9">=char) or ("A"<=char and "Z">=char) or ("a"<=char and "z">=char)).replace("  ", " ").split(" "))
   print(word)

#Main menu
while True:
   print("Main Menu")
   print("1. Word Counting")
   print("2. XXX")
   print("0. EXIT")
   choice = int(input("Enter your choice: "))
   if choice == 1:
      word_count()
   elif choice == 0:
      print("Good bye")
      break
exit(0)