class Variable(str):
    def __init__(self) -> None:
        super().__init__()


class math_expression(str):
    def __init__(self, expression: str) -> None:
        super().__init__()
        self.expression = expression

    def find_all_variable_from_expression(self, variable: Variable):
        pass
        
    @staticmethod
    def simplify(expression: str, *variables: Variable) -> str:
        return ""

if __name__ == "__main__":
    pass
    