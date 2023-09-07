from typing import Generator


comparative_operators = {"=", "<", ">", "!"}
operators = {"+", "-", "*", "/", "^", "(", ")"}.union(comparative_operators)


class ProverError(Exception):
    pass


def parse_expr(expression: str) -> tuple[str, set[str]]:
    variables: set[str] = set()
    expr: list[str] = list(expression.replace(" ", ""))

    # Parsing variables
    for ind, char in enumerate(expr):
        if char.isalpha():
            variables.add(char)
            expr[ind] = "({" + char + "})"

    # Pythonize expression
    for ind, char in enumerate(expr):
        if char:
            if ind-1 > -1 and expr[ind-1]:
                if char[0] in ("{", "(") and expr[ind-1][-1] not in operators:
                    expr[ind] = "*" + char
                if char[0] == "=" and expr[ind-1][-1] not in comparative_operators:
                    expr[ind] = "=="
            if ind+1 < len(expr) and expr[ind+1]:
                if char[-1] in ("}", ")") and expr[ind+1][0] not in operators:
                    expr[ind] += "*"
                if char[-1] == "(" and expr[ind + 1][0] == ")":
                    expr[ind] = expr[ind + 1] = ""

    final_expr = "".join(expr).replace("^", "**").replace(")(", ")*(")
    return final_expr, variables


def parse_ranges(string: str) -> dict[str, range]:
    variables = string.strip().split(" ")
    variables = [v for v in variables if v]

    ranges = {}

    for var in variables:
        name = var[0]
        if var[1] == "=":
            start = int(var[2:])
            value = range(start, start+1)
        elif var[1] == "@":
            start, stop = map(int, var[2:].split(";"))
            value = range(start, stop)
        else:
            raise ProverError(f"Invalid operator \"{name[1]}\"")

        ranges[name] = value

    return ranges


def iterate(variable_ranges: dict[str, range],
            _variable_values: dict[str, int] | None = None) -> Generator:
    if _variable_values is None:
        _variable_values = {}

    if len(_variable_values) == len(variable_ranges):
        yield _variable_values
        return

    current_variable_name = None
    var_range = None
    for var_name, var_range in variable_ranges.items():
        if var_name not in _variable_values:
            current_variable_name = var_name
            break

    if current_variable_name is not None:
        for value in var_range:
            _variable_values[current_variable_name] = value
            yield from iterate(variable_ranges, _variable_values)
            del _variable_values[current_variable_name]


def eval_(expr: str) -> bool:
    try:
        return bool(eval(expr, {}, {}))
    except SyntaxError:
        raise ProverError("Invalid expression syntax")


def evaluate(expression: str,
             variables: set[str],
             ranges: dict[str, range]) -> tuple[bool, dict[str, int]]:
    if not variables <= ranges.keys():
        raise ProverError("No value or range specified for some of the variables")

    for vars_ in iterate(ranges):
        if not eval_(expression.format(**vars_)):
            return False, vars_
    return True, {}


def prove(cmd: str) -> tuple[bool, dict[str, int]]:
    parts = cmd.split("$")
    if len(parts) == 2:
        first_part, second_part = parts
        expression, variables = parse_expr(first_part)
        try:
            ranges = parse_ranges(second_part)
        except IndexError:
            raise ProverError("Invalid range syntax")
        return evaluate(expression, variables, ranges)
    else:
        expression, variables = parse_expr(parts[0])
        if variables:
            raise ProverError("Variables range is not specified")
        return eval_(expression), {}
