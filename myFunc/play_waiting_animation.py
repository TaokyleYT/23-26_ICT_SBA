import time
from typing import Literal

def play_waiting_animation(symbol: str, 
                           wait_time: float, 
                           interval: float = 0.5, 
                           pave_str: str = '', 
                           arrangement_mode: Literal[0, 1, 2] = 2, 
                           direction: Literal[0, 1] = 1):
    remaining_time = wait_time%interval
    number_of_symbol = int(wait_time//interval+(remaining_time>0))
    if direction != 0 and direction != 1:
        raise TypeError("direction must be Literal[0, 1]")
    if direction not in (0, 1, 2):
        raise TypeError("arrangement_mode must be Literal[0, 1, 2]")

    if pave_str == '':
        pave_str = ' '*(number_of_symbol*len(symbol)+3)
    if arrangement_mode == 0:
        print(symbol*number_of_symbol + 
              pave_str[number_of_symbol*len(symbol):] +
              ('\r' 
               if direction else 
               ('\x1b[D'*(len(pave_str)-(number_of_symbol-1)*len(symbol)))), 
              end='', flush=True)
        pave_covered = pave_str[:number_of_symbol*len(symbol)]
    elif arrangement_mode == 1:
        temp = (len(pave_str)-number_of_symbol*len(symbol))//2
        print(pave_str[:temp] +
              symbol*number_of_symbol + 
              pave_str[number_of_symbol*len(symbol)+temp:] +
              (('\r'+'\x1b[C'*temp)
               if direction else 
               ('\x1b[D'*(len(pave_str)-(number_of_symbol-1)*len(symbol)-temp))
              ),
              end='', flush=True)
        pave_covered = pave_str[temp:number_of_symbol*len(symbol)+temp]
    elif arrangement_mode == 2:
        print(pave_str[:(len(pave_str)-number_of_symbol*len(symbol))] +
              symbol*number_of_symbol +
              (('\x1b[D'*(number_of_symbol*len(symbol)))
               if direction else
               '\b'),
              end='', flush=True)
        pave_covered = pave_str[(len(pave_str)-number_of_symbol*len(symbol)):]
    else:
        raise AssertionError("NEVER")

    if direction == 0:
        for i in range(number_of_symbol-1, (0 if remaining_time>0 else -1), -1):
            time.sleep(interval)
            print(pave_covered[i*len(symbol):(i+1)*len(symbol)]+'\x1b[D'*2*len(symbol), end='', flush=True)
        if remaining_time:
            time.sleep(remaining_time)
            print(pave_covered[:len(symbol)], end='', flush=True)
    else:
        for i in range(number_of_symbol-(1 if remaining_time>0 else 0)):
            time.sleep(interval)
            print(pave_covered[i*len(symbol):(i+1)*len(symbol)], end='', flush=True)
        if remaining_time:
            time.sleep(remaining_time)
            print(pave_covered[len(pave_covered)-len(symbol):], end='', flush=True)
    print('\r'+'\x1b[C'*len(pave_str))
    return

if __name__ == "__main__":
    play_waiting_animation(">", 2, pave_str="[()]"*16, interval=0.05)
    time.sleep(1)
    play_waiting_animation(">", 3, pave_str="[()]"*16, interval=1, direction=0, arrangement_mode=1)
    time.sleep(1)
    play_waiting_animation(">>", 3, pave_str=".':;"*5, interval=1, direction=1, arrangement_mode=2)