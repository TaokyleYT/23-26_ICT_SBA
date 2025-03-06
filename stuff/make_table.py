from class_matrix import Matrix
from sep_line import sep_line
from repeat_str_to_len import repeat_str_to_len

def make_table(input_table: Matrix, 
               line_len_limit: int, 
               same_height: bool = False, 
               alignments: list[int] | None = None, 
               sep_line_char: tuple[str, int] | None = None,
               sep_first_line_char: tuple[str, int] | None = ('-', 1),
               row_spacing: tuple[int, int] = (0, 1), 
               first_row_spacing: tuple[int, int] = (1, 1),
               sep_col_char: str = '|',
               sep_first_col_char: str = '||',
               col_spacing: tuple[int, int] = (1, 1),
               first_col_spacing: tuple[int, int] = (1, 1),
               no_display: bool = False
              ):
    alignments = alignments or [0]*input_table.col_num
    sep_line_char = ('', 0) if sep_line_char is None or sep_line_char[0] == '' else sep_line_char
    sep_first_line_char = ('', 0) if sep_first_line_char is None or sep_first_line_char == '' else sep_first_line_char

    if len(alignments) != input_table.col_num or any((item < 0 or item > 2) for item in alignments):
        raise ValueError(f"alignments must be a list of length {input_table.col_num} and each element must be 0(left), 1(middle) or 2(right)")
    table: Matrix[list[str]] = Matrix() #list[list[list[str]]]
    heights: list[int] = []
    
    for lst in input_table:
        table.append([sep_line(item, line_len_limit) for item in lst])
        heights.append(max(len(item) for item in table[-1]))
        
    widths: list[int] = [max((len(cell[0]) if (len(cell) == 1) else line_len_limit) 
                             for cell in lst) 
    for lst in table.transpose()]
    
    heights = [max(heights) for _ in range(len(heights))] if same_height else heights
    for (row_num, lst) in enumerate(table):
        for (col_num, cell) in enumerate(lst):
            for (i, line) in enumerate(cell):
                if row_num == 0:
                    cell[i] = f"{line: ^{widths[col_num]}}"
                elif alignments[col_num] == 0:
                    cell[i] = f"{line: <{widths[col_num]}}"
                elif alignments[col_num] == 1:
                    cell[i] = f"{line: ^{widths[col_num]}}"
                elif alignments[col_num] == 2:
                    cell[i] = f"{line: >{widths[col_num]}}"
                else:
                    raise AssertionError("NEVER")
                if col_num == 0:
                    cell[i] = ' '*first_col_spacing[0] + cell[i] + ' '*first_col_spacing[1]
                else:
                    cell[i] = ' '*col_spacing[0] + cell[i] + ' '*col_spacing[1]
                

    widths[0] += first_col_spacing[0] + first_col_spacing[1]
    for i in range(1, len(widths)):
        widths[i] += col_spacing[0] + col_spacing[1]

    for (row_num, lst) in enumerate(table):
        for (col_num, cell) in enumerate(lst):
            cell.extend([(' '*widths[col_num]) for _ in range(heights[row_num]-len(cell))])

    table.insert(0, [[' '*widths[col_num]]*first_row_spacing[0] for col_num in range(table.col_num)])
    temp_lst = Matrix()
    temp_for_repeat_str = ('', 0)
    for col_num in range(table.col_num):
        temp_for_repeat_str = repeat_str_to_len(sep_first_line_char[0], widths[col_num], temp_for_repeat_str[1])
        temp_lst.col_append([
            [' '*widths[col_num]]*first_row_spacing[1], 
            [temp_for_repeat_str[0]]*sep_first_line_char[1],
            [' '*widths[col_num]]*row_spacing[0]
        ])
    table.insert_multiple(2, temp_lst)
    # start from ((1+3) +1)
    # loop end, -5 (first and its sep lines), and then * 4 (it will add 3 lines after each item), +6 (put the minus numbers back)
    loop_end = (len(table)-5)*4+6
    for i in range(6, loop_end, 4):
        temp_lst = Matrix()
        temp_for_repeat_str = ('', 0)
        for col_num in range(table.col_num):
            temp_for_repeat_str = repeat_str_to_len(sep_line_char[0], widths[col_num], temp_for_repeat_str[1])
            temp_lst.col_append([
                [' '*widths[col_num]]*row_spacing[1], 
                [temp_for_repeat_str[0]]*sep_line_char[1],
                [' '*widths[col_num]]*row_spacing[0]
            ])
        table.insert_multiple(i, temp_lst)
    
    display_table: list[list[str]] = Matrix.flatten_lst_of_lst([list(item) for item in zip(*lst)] for lst in table)
    for _ in range(row_spacing[0]):
        display_table.pop()
    
    loop_end = (len(display_table[0])-2)*2+2
    for lst in display_table:
        lst.insert(1, sep_first_col_char)
        for i in range(3, loop_end, 2):
            lst.insert(i, sep_col_char)
    display_txt = '\n'.join((''.join(item for item in lst)+sep_col_char) for lst in display_table)
    if not no_display: 
        print(display_txt)
    return display_txt



if __name__ == "__main__":
    setting = [[''] * 7,
           [
               '1', '1', "r", "c", "({name}){no}", "{no}", "_", "||",
               "|", "="
           ], 
           ['2', '2', '2']]
    
    menu: dict[str, tuple[str]] = {
        "I": ("Input Seat Plan File",),
        "O": ("Output Seat Plan File",),
        "0": ("Assign Seat Plan",),
        "1": ("Seat Plan Display",),
        "2": ("Student Name List Display",),
        "3": ("Rearrange Seats",),
        "4": ("Increase or Remove Students",),
        "5": ("Rename Students",),
        "6": ("Find Seat of Student",),
        "S": ("Setting",),
        "q": ("quit",)}
        
    make_table(Matrix([["",
                 "functions", 
                 "discribtion", 
                 "highlight mode"], 
                ["1 ",
                 f"3 ({menu['3'][0]})\n\\3(edit students in seats)", 
                 "for showing the editting seat", 
                 setting[2][0]],
                ["2 ",
                 f"5 ({menu['5'][0]})", 
                 "for showing seat of renaming student", 
                 setting[2][1]], 
                ["3 ",
                 f"6 ({menu['6'][0]})", 
                 "for showing seat of student found", 
                 setting[2][2]]
               ]), 25, alignments=[0,0,0,1], first_row_spacing=(3,1), row_spacing=(2,1), sep_first_line_char=("[]", 1), sep_line_char=("<>", 1))
    