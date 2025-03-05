def sep_line(line: str, line_wordlen: int) -> list[str]:
    """
    This function takes a string and a maximum word length as input. 
    It then returns a list of strings, each of which is a line of text, 
    such that no word in any line exceeds the maximum word length.\n
    For example:\n
    sep_line("This is a test.", 5) \n
    >> ["This", "is a", "test."]
    """
    line = line.replace("\n", "\n ")
    temp = line.split(' ') #default will split by space and \n and idk if there are others
    words: list[str] = [(item if (i == len(temp) or '\n' in item) else item+' ') for i, item in enumerate(temp)]
    output_lst = []
    index: int = 0
    while index < len(words):
        if len(words[index]) > line_wordlen:
            output_lst.append(words[index])
            index += 1
            continue
        output_lst.append("")
        for i, word in enumerate(words[index:]):
            if len(output_lst[-1])+len(word) > line_wordlen:
                index += i
                break #break for loop
            if '\n' in word:
                output_lst[-1] += word[:len(word)-1]
                index += i+1
                break
            output_lst[-1] += word
        else:
            break #break while loop
    return output_lst

if __name__ == "__main__":
    print('\n'.join(sep_line("This is a test.", 5)))
    print('-'*5)
    print('\n'.join(sep_line("This is a longer test, with more words.", 10)))
    print('-'*10)
    print('\n'.join(sep_line("This is a test with a really long word.", 15)))
    print('-'*15)
    print('\n'.join(sep_line("This is a really long test, with a lot of words.", 10)))
    print('-'*10)
    temp = ("This is a very long passage to test and see how the function works. "
            "It should be able to break up the sentence into lines that are no longer "
            "than 50 characters. Let's see if it works! ")*10
    print('\n'.join(sep_line(temp, 50)))
    print('-'*50)
    temp = ("This is a very long passage to\ntest\n and see how the function works. "+
        "It should be able to break up the sentence into lines that are no longer "
        "than 50 characters. Let's see if it works! ")*3
    print('\n'.join(sep_line(temp, 50)))
    print('-'*50)