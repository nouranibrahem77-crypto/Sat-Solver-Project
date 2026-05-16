from dataclasses import dataclass
from itertools import product
from time import perf_counter

from utils import assignment_to_text, format_bool, long_bool, validate_parentheses


@dataclass
class Token:
    kind: str
    value: str


@dataclass
class SolveResult:
    original_formula: str
    variables: list
    truth_rows: list
    satisfying_assignments: list
    total_assignments: int
    satisfying_count: int
    is_satisfiable: bool
    execution_time: float


class FormulaParser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return Token("END", "")

    def move(self):
        token = self.current()
        self.position += 1
        return token

    def parse(self):
        if not self.tokens:
            raise ValueError("The formula is empty.")

        tree = self.parse_or()

        if self.current().kind != "END":
            token = self.current()
            raise ValueError(f"Unexpected part near '{token.value}'. Maybe an operator is missing.")

        return tree

    def parse_or(self):
        left = self.parse_and()

        while self.current().kind == "OP" and self.current().value == "or":
            self.move()
            right = self.parse_and()
            left = ("or", left, right)

        return left

    def parse_and(self):
        left = self.parse_not()

        while self.current().kind == "OP" and self.current().value == "and":
            self.move()
            right = self.parse_not()
            left = ("and", left, right)

        return left

    def parse_not(self):
        if self.current().kind == "OP" and self.current().value == "not":
            self.move()
            return ("not", self.parse_not())

        return self.parse_primary()

    def parse_primary(self):
        token = self.current()

        if token.kind == "VAR":
            self.move()
            return ("var", token.value)

        if token.kind == "LPAREN":
            self.move()
            inside = self.parse_or()

            if self.current().kind != "RPAREN":
                raise ValueError("Missing closing parenthesis.")

            self.move()
            return inside

        if token.kind == "END":
            raise ValueError("The formula ended too early.")

        raise ValueError(f"Unexpected symbol '{token.value}'.")


def tokenize(formula):
    tokens = []
    i = 0

    while i < len(formula):
        char = formula[i]

        if char.isspace():
            i += 1
            continue

        if char == "(":
            tokens.append(Token("LPAREN", char))
            i += 1
        elif char == ")":
            tokens.append(Token("RPAREN", char))
            i += 1
        elif char in ["&", "|", "!"]:
            if char == "&":
                tokens.append(Token("OP", "and"))
            elif char == "|":
                tokens.append(Token("OP", "or"))
            else:
                tokens.append(Token("OP", "not"))
            i += 1
        elif char.isalpha():
            start = i
            while i < len(formula) and (formula[i].isalnum() or formula[i] == "_"):
                i += 1

            word = formula[start:i]
            lower_word = word.lower()

            if lower_word in ["and", "or", "not"]:
                tokens.append(Token("OP", lower_word))
            else:
                tokens.append(Token("VAR", word))
        else:
            raise ValueError(f"Invalid character '{char}' found in the formula.")

    tokens.append(Token("END", ""))
    return tokens


def collect_variables(tree):
    if tree[0] == "var":
        return {tree[1]}

    if tree[0] == "not":
        return collect_variables(tree[1])

    left_vars = collect_variables(tree[1])
    right_vars = collect_variables(tree[2])
    return left_vars.union(right_vars)


def evaluate_tree(tree, assignment):
    node_type = tree[0]

    if node_type == "var":
        return assignment[tree[1]]

    if node_type == "not":
        return not evaluate_tree(tree[1], assignment)

    if node_type == "and":
        return evaluate_tree(tree[1], assignment) and evaluate_tree(tree[2], assignment)

    if node_type == "or":
        return evaluate_tree(tree[1], assignment) or evaluate_tree(tree[2], assignment)
    raise ValueError("Unknown expression type.")


def parse_formula(formula):
    validate_parentheses(formula)
    tokens = tokenize(formula)
    parser = FormulaParser(tokens)
    return parser.parse()


def solve_formula(formula, debug=False):
    start_time = perf_counter()
    formula = formula.strip()

    if formula == "":
        raise ValueError("Please enter a logical formula.")

    tree = parse_formula(formula)
    variables = sorted(list(collect_variables(tree)), key=lambda name: name.upper())

    truth_rows = []
    satisfying_assignments = []

    for values in product([True, False], repeat=len(variables)):
        assignment = dict(zip(variables, values))
        result = evaluate_tree(tree, assignment)

        truth_rows.append({
            "assignment": assignment,
            "result": result,
        })

        if result:
            satisfying_assignments.append(assignment.copy())

        if debug:
            print("[debug] checked:", assignment, "=>", result)

    end_time = perf_counter()

    return SolveResult(
        original_formula=formula,
        variables=variables,
        truth_rows=truth_rows,
        satisfying_assignments=satisfying_assignments,
        total_assignments=len(truth_rows),
        satisfying_count=len(satisfying_assignments),
        is_satisfiable=len(satisfying_assignments) > 0,
        execution_time=end_time - start_time,
    )


def make_text_report(result):
    lines = []

    lines.append("Formula:")
    lines.append(result.original_formula)
    lines.append("")

    lines.append("Variables detected:")
    if result.variables:
        lines.append(", ".join(result.variables))
    else:
        lines.append("(none)")
    lines.append("")

    lines.append("Truth Table:")
    header = " ".join(result.variables + ["Result"])
    lines.append(header)
    lines.append("-" * max(len(header), 20))

    for row in result.truth_rows:
        values = [format_bool(row["assignment"][var]) for var in result.variables]
        values.append(long_bool(row["result"]))
        lines.append(" ".join(values))

    lines.append("")
    lines.append("Satisfying assignments:")

    if result.satisfying_assignments:
        for assignment in result.satisfying_assignments:
            lines.append(assignment_to_text(assignment))
    else:
        lines.append("No satisfying assignment was found.")

    lines.append("")
    lines.append(f"Total assignments: {result.total_assignments}")
    lines.append(f"Satisfying assignments: {result.satisfying_count}")
    lines.append(f"Execution time: {result.execution_time:.6f} seconds")
    lines.append("")

    lines.append("Final Result:")
    if result.is_satisfiable:
        lines.append("The formula is SATISFIABLE.")
    else:
        lines.append("The formula is UNSATISFIABLE.")

    return "\n".join(lines)


if __name__ == "__main__":
    
    test_formula = "(P | Q) & (!P | R) & (!Q | !R)"
    answer = solve_formula(test_formula, debug=True)
    print()
    print(make_text_report(answer))
