"""
TO PREVENT UNEXPECTED ERRORS WHILE PARSING AND UNPARSING CODES,
PLEASE RUN THIS IN AN UP-TO-DATE PYTHON VERSION
"""

import ast
import os
import sys

if sys.version_info < (3, 9):
    print("\x1b[33mLow python version detected (<3.9), some parsings and unparsings may fail\nRunning this program with a higher python version might resolve this issue\x1b[m\n")
    try:
        import astunparse
    except ImportError:
        print("The 'astunparse' library is required to run this program.\nattempting to install using pip")
        os.system("pip install astunparse")
        print("Please re-run the program\n\n(if this notification still appears, maybe you need to manually pip install astunparse)")
        exit(1)


class TypeHintRemover(ast.NodeTransformer):

    def visit_FunctionDef(self, node):
        node.returns = None
        if node.args.args:
            for arg in node.args.args:
                arg.annotation = None
        self.generic_visit(node)
        return node
    
    def visit_AnnAssign(self, node):
        Assign = ast.Assign(targets=[node.target],
                            value=node.value,
                            lineno=node.lineno,
                            col_offset=node.col_offset,
                            end_lineno=node.end_lineno,
                            end_col_offset=node.end_col_offset)
        self.generic_visit(node)
        return node
    


def remove_type_hints(source):
    parsed_source = ast.parse(source)
    transformed = TypeHintRemover().visit(parsed_source)
    if sys.version_info >= (3, 9):
        # For Python 3.9 and above, use ast.unparse directly
        return ast.unparse(transformed)
    else:
        # For Python 3.8 and below, use astunparse to generate source code
        return astunparse.unparse(transformed).strip()


def main():
    if not os.path.exists("NoTypeHintPy"):
        os.mkdir("NoTypeHintPy")
    for file in os.listdir("."):
        if not file.endswith(".py") or os.path.samefile(file, __file__) or "TypeHintingRemover" in file:
            continue
        print("Attempting to remove type hints for", file)
        try:
            with open(file, "r", encoding="utf-8") as sourceFile:
                source = "".join(sourceFile.readlines())
                dest = remove_type_hints(source)
                with open(
                    os.path.join(os.path.dirname(file), f"NoTypeHintPy/{file}"), "w", encoding="utf-8"
                ) as destFile:
                    destFile.write(dest)
                print("\x1b[32mSuccessfully removed type hints for", file, "\x1b[m\n")
        except Exception as e:
            print(f"\x1b[31mError processing {file}: {e}\x1b[m\n")
            continue
    print("All processed files have been saved in the 'NoTypeHintPy' directory.")


if __name__ == "__main__":
    main()
