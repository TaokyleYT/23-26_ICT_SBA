from typing import Any, Generic, Iterable, SupportsIndex, TypeVar

T = TypeVar('T')

class Matrix(list, Generic[T]):

    def __init__(self, lst:Iterable|None=None):
        if lst is None:
            super().__init__()
            self.col_num = 0
        else:
            lst = list(lst)
            if not all(len(lst[i]) == len(lst[0]) for i in range(1, len(lst))):
                raise ValueError("All numbers of columns must be the same.")

            super().__init__(list(item) for item in lst)
            self.col_num = len(self[0]) if len(self) > 0 else 0

        self.row_num = len(self)

    def transpose(self):
        """
        Returns a new Matrix with rows and columns reversed.

        Returns:
            Matrix: A new Matrix with rows and columns reversed.
        """
        return Matrix([self[r][c] for r in range(self.row_num)]
                      for c in range(self.col_num))

    def dcopy(self):
        return Matrix(lst.copy() for lst in self)

    def flatten(self):
        return [item for lst in self for item in lst]

    @staticmethod
    def flatten_lst_of_lst(lst_of_lst:Iterable[Iterable]):
        return [item for lst in lst_of_lst for item in lst]
        
    def update_attr(self) -> None:
        self.row_num = len(self)
        self.col_num = len(self[0])

    def __typ_val_check_when_self_len_increase(self, value, method_name: str) -> None:
        if not isinstance(value, list):
            raise TypeError(f"\n***err when doing '{method_name}' method of Matrix instance."+
                            f"\n***  value '{value}'"
                            "\n***  is not in type <list>")
        if len(value) != self.col_num and self.row_num != 0:
            raise ValueError(f"\n***err when doing '{method_name}' method of Matrix instance."+
                             f"\n***  value '{value}'"
                             f"\n***  not having the same length as Matrix instance.col_num({self.col_num})")
        return

    def __check_same_length(self, values: Iterable[list], method_name: str):
        values = list(values)
        length = len(values[0])
        for i in range(1, len(values)):
            if len(values[i]) != length:
                raise ValueError(f"\n***err when doing '{method_name}' method of Matrix instance."+
                                 f"\n***  values '{values}'"+
                                 "\n***  are having items of different lengths")
                
    def __supports_index_check(self, index, method_name: str) -> None:
        if not isinstance(index, SupportsIndex):
            raise TypeError(f"\n***err when doing '{method_name}' method of Matrix instance."+
                            f"\n***  index '{index}'"+
                            "\n***  is not in type <SupportsIndex>")
        return
        
    def append(self, value) -> None:
        self.__typ_val_check_when_self_len_increase(value, "append")
        super().append(value)
        self.update_attr()

    def col_append(self, values:Iterable|type) -> None:
        if isinstance(values, type):
            values = [values()]*self.row_num
        elif not isinstance(values, Iterable):
            raise TypeError("\n***err when doing 'col_append' method of Matrix instance."+
                            f"\n***  col_append argument values '{values}'"+
                            "\n***  not in type <type> or <Iterable>")
            
        values = list(values)
        
        if self.row_num == 0:
            self.extend([[] for _ in range(len(values))]) #build list of (empty list with different id)
            
        elif len(values) != self.row_num:
                raise ValueError("\n***err when doing 'col_append' method of Matrix instance."+
                                 f"\n***  col_append argument values '{values}'"+
                                 f"\n***  not having the same length as Matrix instance.row_num({self.row_num})")

        for i, lst in enumerate(self):
            lst.append(values[i])
        self.update_attr()
        return

    def insert(self, index: SupportsIndex, value) -> None:
        self.__typ_val_check_when_self_len_increase(value, "insert")
        self.__supports_index_check(index, "insert")
        super().insert(index, value)
        self.update_attr()

    def pop(self, index: SupportsIndex = -1) -> Any:
        self.__supports_index_check(index, "pop")
        self.row_num -= 1
        return super().pop(index)
        
    def extend(self, value: Iterable[list])-> None:
        self.__check_same_length(value, "extend")
        for item in value:
            self.__typ_val_check_when_self_len_increase(item, "extend")
        super().extend(value)
        self.update_attr()

    def insert_multiple(self, index: SupportsIndex, value: Iterable[list]) -> None:
        for item in value:
            self.__typ_val_check_when_self_len_increase(item, "insert_multiple")
        self.__check_same_length(value, "insert_multiple")
        self.__supports_index_check(index, "insert_multiple")
        self[index:index] = list(value)
        self.update_attr()
        
if __name__ == "__main__":
    a = Matrix([[1, 2], [2, 3]])
    
    #get self test
    print(f"\n{'SELF':.<100}")
    print(a)
    print(f"\n{'__getitem__ TEST':.<100}")
    print(a[0])
    
    #attr
    print(f"\n{'ATTRIBUTE TEST':.<100}")
    print(a.row_num)
    print(a.col_num)
    
    #transpose
    print(f"\n{'TRANSPOSE TEST':.<100}")
    t = a.transpose()
    print(f"{t = }\n{t.row_num = }\n{t.col_num = }")
    
    #copy
    print(f"\n{'DEEP COPY TEST':.<100}")
    b = a.dcopy()
    print(f"{a = }\n{id(a) = }, {id(a[0]) = }, {id(a[1]) = }\n"+
          f"{b = }\n{id(b) = }, {id(b[0]) = }, {id(b[1]) = }")
    
    a = Matrix([[1, 2], [2, 3]])
    
    #
    print(f"\n{'FLATTEN TEST':.<100}")
    print(f"{a.flatten() = }")
    
    a = Matrix([[1, 2], [2, 3]])
    
    #
    print(f"\n{'APPEND VALUE ERR TEST':.<100}", end='')
    try:
        a.append([1])
    except ValueError as e:
        print(e)
    #
    print(f"\n{'APPEND TYPE ERR TEST':.<100}", end='')
    try:
        a.append(1)
    except TypeError as e:
        print(e)
    
    #
    print(f"\n{'APPEND VALUE TEST':.<100}")
    a.append([8,7])
    print(f"{a = }\n{a.row_num = }\n{a.col_num = }")
    
    a = Matrix([[1, 2], [2, 3]])
    
    #
    print(f"\n{'COLUMN APPEND VALUE ERR TEST':.<100}", end='')
    try:
        a.col_append(['col test str1', 'col test str2', 'col test str3'])
    except ValueError as e:
        print(e)
        
    #
    print(f"\n{'COLUMN APPEND TYPE ERR TEST':.<100}", end='')
    try:
        a.col_append(5)
    except TypeError as e:
        print(e)
    
    #
    print(f"\n{'COLUMN APPEND TYPE ARG TEST':.<100}")
    a.col_append(int)
    print(f"{a = }\n{a.row_num = }\n{a.col_num = }")
    
    a = Matrix([[1, 2], [2, 3]])
    
    #
    print(f"\n{'COLUMN APPEND LIST ARG TEST1':.<100}")
    a.col_append([['append arg=list test str1'], 'append arg=list test str2'])
    print(f"{a = }\n{a.row_num = }\n{a.col_num = }")
    
    a = Matrix()

    #
    print(f"\n{'COLUMN APPEND LIST ARG TEST2':.<100}")
    print("a = Matirx()")
    a.col_append([['append arg=list test str1'], 'append arg=list test str2'])
    print(f"{a = }\n{a.row_num = }\n{a.col_num = }")

    a = Matrix([[1, 2], [2, 3]])
    
    #
    print(f"\n{'INSERT VALUE TEST':.<100}")
    a.insert(0, ['insert test str1', 'insert test str2'])
    print(f"{a = }\n{a.row_num = }\n{a.col_num = }")
    
    a = Matrix([[1, 2], [2, 3]])

    #
    print(f"\n{'INSERT VALUE ERR TEST':.<100}", end='')
    try:
        a.insert(0, ['insert test str1', 'insert test str2', 'insert test str3'])
    except ValueError as e:
        print(e)

    #
    print(f"\n{'INSERT TYPE ERR TEST 1':.<100}", end='')
    try:
        a.insert(0, 5)
    except TypeError as e:
        print(e)

    #
    print(f"\n{'INSERT TYPE ERR TEST 2':.<100}", end='')
    try:
        a.insert('', ['insert test str1', 'insert test str2'])
    except TypeError as e:
        print(e)

    #
    print(f"\n{'POP VALUE TEST':.<100}")
    a.pop(0)
    print(f"{a = }\n{a.row_num = }\n{a.col_num = }")
        
    #
    print(f"\n{'POP TYPE ERR TEST':.<100}", end='')
    try:
        a.pop('')
    except TypeError as e:
        print(e)

    #
    print(f"\n{'EXTEND VALUE TEST':.<100}")
    a.extend((['extend00', 'extend01'], 
              ['extend10', 'extend11'], 
              ['extend20', 'extend22']))
    print(f"{a = }\n{a.row_num = }\n{a.col_num = }")

    a = Matrix([[1, 2], [2, 3]])
    
    #
    print(f"\n{'EXTEND VALUE ERR TEST':.<100}", end='')
    try:
        a.extend((['extend00', 'extend01', 'extend02'], 
                  ['extend10', 'extend11', 'extend12'], 
                  ['extend20', 'extend22', 'extend22']))
    except ValueError as e:
        print(e)

    #
    print(f"\n{'INSERT MULTIPLE VALUE TEST':.<100}")
    a.insert_multiple(1, (['insert00', 'insert01'], ['insert10', 'insert11']))
    print(f"{a = }\n{a.row_num = }\n{a.col_num = }")

    a = Matrix([[1, 2], [2, 3]])
    
    #
    print(f"\n{'INSERT MULTIPLE VALUE ERR TEST1':.<100}", end='')
    try:
        a.insert_multiple(1, (['insert00', 'insert01', 'insert02'], ['insert10', 'insert11', 'insert12']))
    except ValueError as e:
        print(e)

    #
        print(f"\n{'INSERT MULTIPLE VALUE ERR TEST2':.<100}", end='')
    try:
        a.insert_multiple(1, (['insert00', 'insert01'], ['insert10', 'insert11', 'insert12']))
    except ValueError as e:
        print(e)

    print(f"\n{'INSERT MULTIPLE TYPE ERR TEST':.<100}", end='')
    try:
        a.insert_multiple(1, ("haha", "haha2"))
    except TypeError as e:
        print(e)

    print("\n--Test Finished--")