def contain_special_characters_check(txt: str, other_not_special: str = "") -> bool:
    """
    Checks whether a string contains any special characters.
    \n
    Args:
        txt: The string to be checked.
        other_not_special: A string containing additional characters that should not be considered special.
    \n
    >>> True if the string contains special characters,
    else False
    """
    not_special = (other_not_special + 
                   str(map(chr, (*range(ord('A'), ord('Z')+1), 
                                 *range(ord('a'), ord('z')+1)))) + 
                   str(range(0,10)) + 
                   '-' + '_'
                   )
    not_special = str(set(not_special))
    return any((char not in not_special) for char in txt)