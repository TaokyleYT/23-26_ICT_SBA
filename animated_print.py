from collections.abc import Iterable
from helpers import linked_list as list
import time, os


def animated_print(txt: Iterable[str],
                   delay: float = 0.02,
                   front_effect: str = '',
                   next_line_char_delay: int = 1,
                   end: str = '\n'):
    if all(isinstance(char, str) for char in txt):
        if all(len(char) == 1 for char in txt):
            txt_lst = list(''.join(txt).split('\n'))
            #print(txt_lst)
        else:
            txt_lst = list(txt)
    else:
        raise TypeError("txt must be a str or iterable of str")
    if not isinstance(delay, (int, float)):
        raise TypeError("delay must be a number")
    if not isinstance(front_effect, str):
        raise TypeError("front_effect must be a str")

    term_size = os.get_terminal_size()
    max_wordlen = max([len(line) for line in txt_lst])
    print('\n' * (len(txt_lst)), end='')
    for i in range(max_wordlen + next_line_char_delay * (len(txt_lst))):
        print("\x1b[A"*(len(txt_lst)-1), end='')
        time.sleep(delay)
        for j, line in enumerate(txt_lst):
            temp_for_line_delay = j * next_line_char_delay + 1
            print(' '*len(front_effect)+"\x1b[D"*len(front_effect), end='')
            if (i - temp_for_line_delay >= 0 
                and i - temp_for_line_delay < len(line)):
                print("\x1b[" + str(temp_for_line_delay) + "D" +
                      line[i - temp_for_line_delay] +
                      front_effect + "\x1b[D"*len(front_effect) +
                      "\x1b[" + str(temp_for_line_delay) + "C" + "\b\x1b[1B",
                      end='',
                      flush=True)
            else:
                print("\x1b[1B", end='', flush=True)
        print("\x1b[1A\x1b[1C", end='', flush=True)
    time.sleep(delay)
    print("\x1b[" + str(next_line_char_delay * len(txt_lst)) + "D", end=end, flush=True)
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
