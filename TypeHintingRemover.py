import ast
import os
import sys

if sys.version_info < (3, 9):
    try:
        import astunparse
    except ImportError:
        print(
            "The 'astunparse' library is required to run this program.\nattempting to install using pip"
        )
        os.system("pip install astunparse")
        print("Please re-run the program")
        exit(1)


class TypeHintRemover(ast.NodeTransformer):

    def visit_FunctionDef(self, node):
        node.returns = None
        if node.args.args:
            for arg in node.args.args:
                arg.annotation = None
        self.generic_visit(node)
        return node

    def visit_Import(self, node):
        node.names = [n for n in node.names if n.name != "typing"]
        return node if node.names else None

    def visit_ImportFrom(self, node):
        return node if node.module != "typing" else None


def remove_type_hints(source):
    parsed_source = ast.parse(source)
    transformed = TypeHintRemover().visit(parsed_source)
    if sys.version_info >= (3, 9):
        # For Python 3.9 and above, use ast.unparse directly
        return ast.unparse(transformed)
    else:
        # For Python 3.8 and below, use astor to generate source code
        return astunparse.unparse(transformed).strip()


def main():
    if not os.path.exists("NoTypeHintPy"):
        os.mkdir("NoTypeHintPy")
    for file in os.listdir("."):
        if not file.endswith(".py") or os.path.samefile(file, __file__) or "TypeHintingRemover" in file:
            continue
        print("Attempting to remove type hints for", file)
        try:
            with open(file, "r", errors="ignore") as sourceFile:
                source = "".join(sourceFile.readlines())
                dest = remove_type_hints(source)
                with open(
                    os.path.join(os.path.dirname(file), f"NoTypeHintPy/{file}"), "w"
                ) as destFile:
                    destFile.write(dest)
                print("Successfully removed type hints for", file, "\n")
        except Exception as e:
            print(f"Error processing {file}: {e}")
            continue
    print("All processed files have been saved in the 'NoTypeHintPy' directory.")


if __name__ == "__main__":
    main()
