"""
TO PREVENT UNEXPECTED ERRORS WHILE PARSING AND UNPARSING CODES,
PLEASE RUN THIS IN A HIGH PYTHON VERSION (preferably 3.10+)
"""

import ast
import os
import sys

LowVer = False

if sys.version_info < (3, 9):
    print("\x1b[33mLow python version detected (<3.9), some parsings and unparsings may fail\nRunning this program with a higher python version might resolve this issue\x1b[m\n")
    LowVer = True
    try:
        import astunparse
    except ImportError:
        print("The 'astunparse' library is required to run this program.\nattempting to install using pip")
        os.system("pip install astunparse")
        print("Please re-run the program\n\n(if this notification still appears, maybe you need to manually pip install astunparse)")
        exit(1)


class LowVerAdapter(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        node.returns = None
        if hasattr(node.args, "posonlyargs"):
            node.args.posonlyargs = []
        if node.args.args:
            for arg in node.args.args:
                arg.annotation = None
        if node.args.kwonlyargs:
            for arg in node.args.kwonlyargs:
                arg.annotation = None
        if node.args.vararg:
            node.args.vararg.annotation = None
        if node.args.kwarg:
            node.args.kwarg.annotation = None
        self.generic_visit(node)
        return node

    def visit_AnnAssign(self, node):
        new_node = ast.Assign(
            targets=[node.target],
            value=node.value if node.value is not None else ast.NameConstant(None),
            lineno=node.lineno,
            col_offset=node.col_offset,
            end_lineno=getattr(node, "end_lineno", None),
            end_col_offset=getattr(node, "end_col_offset", None),
        )
        self.generic_visit(new_node)
        return new_node

    def visit_IfExp(self, node):
        node.test = self.visit(node.test)
        node.body = self.visit(node.body)
        node.orelse = self.visit(node.orelse)
        return node

    def visit_FormattedValue(self, node):
        node.value = self.visit(node.value)
        if node.format_spec:
            node.format_spec = self.visit(node.format_spec)
        return node

    def visit_JoinedStr(self, node):
        parts = []
        args = []

        def get_format_spec_str(format_spec_node):
            if format_spec_node is None:
                return ''
            spec_parts = []
            for val in format_spec_node.values:
                if isinstance(val, ast.Constant) and isinstance(val.value, str):
                    spec_parts.append(val.value)
                elif LowVer and isinstance(val, ast.Str):
                    spec_parts.append(val.s)
                else:
                    spec_parts.append("{}")
            return ''.join(spec_parts)

        for value in node.values:
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                parts.append(value.value.replace("{", "{{").replace("}", "}}"))
            elif LowVer and isinstance(value, ast.Str):
                parts.append(value.s.replace("{", "{{").replace("}", "}}"))
            elif isinstance(value, ast.FormattedValue):
                transformed_value = self.visit(value.value)
                fmt_spec = get_format_spec_str(value.format_spec)
                parts.append(f"{{{fmt_spec}}}")
                args.append(transformed_value)
            else:
                parts.append("{}")
                args.append(value)

        if LowVer:
            new_str = ast.Str(''.join(parts))
        else:
            new_str = ast.Constant(''.join(parts))

        format_call = ast.Call(
            func=ast.Attribute(
                value=new_str,
                attr='format',
                ctx=ast.Load(),
            ),
            args=args,
            keywords=[],
        )
        return ast.copy_location(format_call, node)
    
    def visit_Call(self, node):
        self.generic_visit(node)
        return node
    
    def visit_List(self, node): # Replace generalized unpacking. Since all unpackings are in the form of `[*"string"]`, this works. This method is NOT general, and is tailored to the code in this project
        self.generic_visit(node)
        if len(node.elts) == 1 and isinstance(node.elts[0], ast.Starred):
            val = node.elts[0].value
            if isinstance(val, ast.JoinedStr):
                new_elts = []
                for piece in val.values:
                    if isinstance(piece, ast.Constant) and isinstance(piece.value, str):
                        new_elts.extend([ast.Constant(value=ch, kind=None) for ch in piece.value])
                    elif isinstance(piece, ast.FormattedValue):
                        inner_val = piece.value
                        if not isinstance(inner_val, ast.IfExp):
                            new_elts.append(piece)
                            continue
                        body_val = inner_val.body
                        orelse_val = inner_val.orelse
                        test = inner_val.test
                        if not ((isinstance(body_val, ast.Constant) and isinstance(body_val.value, str)
                                and isinstance(orelse_val, ast.Constant) and isinstance(orelse_val.value, str))):
                            new_elts.append(piece)
                            continue
                        body_str = body_val.value
                        orelse_str = orelse_val.value
                        max_len = max(len(body_str), len(orelse_str))
                        for i in range(max_len):
                            b_char = ast.Constant(value=body_str[i] if i < len(body_str) else '', kind=None)
                            o_char = ast.Constant(value=orelse_str[i] if i < len(orelse_str) else '', kind=None)
                            test_node = ast.copy_location(test, test)
                            new_elts.append(ast.IfExp(test=test_node, body=b_char, orelse=o_char))
                    else:
                        new_elts.append(piece)
                new_node = ast.List(elts=new_elts, ctx=node.ctx)
                ast.copy_location(new_node, node)
                ast.fix_missing_locations(new_node)
                return new_node

        new_elts = []
        for elt in node.elts:
            if isinstance(elt, ast.Starred):
                val = elt.value
                if isinstance(val, ast.Constant) and isinstance(val.value, str):
                    new_elts.extend([ast.Constant(value=ch, kind=None) for ch in val.value])
                else:
                    new_elts.append(elt)
            else:
                new_elts.append(elt)
        node.elts = new_elts
        return node

    def visit_If(self, node): # Replace warlus. Since all warlus are in the form of `if (x := y)`, this works. This method is NOT general, and is tailored to the code in this project
        self.generic_visit(node)
        
        assigns = []

        def replace_namedexpr(expr):
            if isinstance(expr, ast.NamedExpr):
                assigns.append(
                    ast.Assign(
                        targets=[expr.target],
                        value=expr.value,
                        lineno=expr.lineno,
                        col_offset=expr.col_offset
                    )
                )
                return expr.target
            else:
                for field, old_value in ast.iter_fields(expr):
                    if isinstance(old_value, ast.AST):
                        new_node = replace_namedexpr(old_value)
                        setattr(expr, field, new_node)
                    elif isinstance(old_value, list):
                        new_list = []
                        for item in old_value:
                            if isinstance(item, ast.AST):
                                new_item = replace_namedexpr(item)
                                new_list.append(new_item)
                            else:
                                new_list.append(item)
                        setattr(expr, field, new_list)
                return expr

        node.test = replace_namedexpr(node.test)

        for assign in assigns:
            ast.fix_missing_locations(assign)
        ast.fix_missing_locations(node)

        if assigns:
            return assigns + [node]
        else:
            return node

def remove_high_py_ver_stuff(source):
    parsed_source = ast.parse(source)
    transformed = LowVerAdapter().visit(parsed_source)
    ast.fix_missing_locations(transformed)

    if LowVer:
        return astunparse.unparse(transformed).strip()
    else:
        return ast.unparse(transformed)

def main():
    if not os.path.exists("LowVerPy"):
        os.mkdir("LowVerPy")
    for file in os.listdir("."):
        if not file.endswith(".py") or os.path.samefile(file, __file__) or "LowVerPyAdapter" in file:
            continue
        print("Attempting to parse", file)
        try:
            with open(file, "r", encoding="utf-8") as sourceFile:
                source = "".join(sourceFile.readlines())
                dest = remove_high_py_ver_stuff(source)
                with open(
                    os.path.join(os.path.dirname(file), f"LowVerPy/{file}"), "w", encoding="utf-8"
                ) as destFile:
                    destFile.write(dest)
                print("\x1b[32mSuccessfully parsed", file, "\x1b[m\n")
        except Exception as e:
            print(f"\x1b[31mError processing {file}: {e}\x1b[m\n")
            continue
    print("All processed files have been saved in the 'LowVerPy' directory.")


if __name__ == "__main__":
    main()