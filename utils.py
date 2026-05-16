import random

SAMPLE_FORMULAS = [
    "(P | Q) & (!P | R) & (!Q | !R)",
    "(A or B) and (!A or C)",
    "A and !A",
    "(X | Y) and (!X | Z)",
    "not A or (B and C)",
]


def format_bool(value):
    if value:
        return "T"
    return "F"


def long_bool(value):
    if value:
        return "True"
    return "False"


def validate_parentheses(formula):
    balance = 0

    for char in formula:
        if char == "(":
            balance += 1
        elif char == ")":
            balance -= 1

        if balance < 0:
            raise ValueError("There is a closing parenthesis without an opening one.")

    if balance != 0:
        raise ValueError("Parentheses are not balanced.")


def assignment_to_text(assignment):
    parts = []
    for name, value in assignment.items():
        parts.append(f"{name}={long_bool(value)}")
    return ", ".join(parts)


def make_random_formula():
    variables = random.sample(["A", "B", "C", "P", "Q", "R", "X", "Y"], random.randint(2, 4))

    def random_literal():
        var_name = random.choice(variables)
        if random.choice([True, False]):
            return "!" + var_name
        return var_name

    clauses = []
    for _ in range(random.randint(2, 4)):
        left = random_literal()
        right = random_literal()
        or_symbol = random.choice([" | ", " or "])
        clauses.append("(" + left + or_symbol + right + ")")

    and_symbol = random.choice([" & ", " and "])
    return and_symbol.join(clauses)
