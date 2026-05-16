# SAT Solver for Logic Problems Using Discrete Mathematics

## Theory / Concepts

### What is Boolean Satisfiability (SAT)?

Boolean Satisfiability, usually called SAT, is the problem of deciding whether a propositional logic formula can become true for at least one assignment of truth values. In other words, we try different values for the variables and ask: "Is there any way to make the whole formula true?"

SAT is important in Discrete Mathematics because it connects logic, truth tables, algorithms, and combinatorics.

### What is propositional logic?

Propositional logic is a type of logic that uses statements which are either true or false. These statements are represented by variables such as `P`, `Q`, `R`, `A`, or `B`.

Example:

```text
(P or Q) and !R
```

Here, `P`, `Q`, and `R` are propositions.

### What are Boolean variables?

A Boolean variable is a variable that can only have one of two values:

```text
True
False
```

For example, if `P = True` and `Q = False`, then the formula `P and Q` is false.

### Logical operators

AND (`∧`) means both sides must be true.

```text
P and Q
```

OR (`∨`) means at least one side must be true.

```text
P or Q
```

NOT (`¬`) reverses the truth value.

```text
not P
```

This project accepts these symbols:

| User input | Meaning |
| --- | --- |
| `&`, `and` | AND |
| `|`, `or` | OR |
| `!`, `not` | NOT |
| `(`, `)` | Parentheses |

### What does SATISFIABLE mean?

A formula is **satisfiable** if at least one truth assignment makes the formula true.

Example:

```text
P or Q
```

This is satisfiable because it is true when `P=True`, or when `Q=True`.

### What does UNSATISFIABLE mean?

A formula is **unsatisfiable** if no possible truth assignment can make it true.

Example:

```text
P and !P
```

This is impossible to satisfy because `P` cannot be true and false at the same time.

### Truth tables

A truth table lists every possible combination of truth values for the variables in a formula. Then it shows whether the whole formula is true or false for each row.

For `P` and `Q`, there are `2^2 = 4` assignments:

```text
P Q Result
T T ...
T F ...
F T ...
F F ...
```

## Project Description

This project is a simple SAT Solver made for a university Discrete Mathematics course. The program checks a propositional logic formula by trying all possible truth assignments. If at least one assignment gives `True`, then the formula is satisfiable.

The program uses a brute force method because it is clear and matches the truth table topic from the course.

## Features

- Tkinter GUI
- Formula input from the user
- Supports any number of variables
- Automatically detects variables
- Supports `&`, `|`, `!`, `and`, `or`, `not`
- Generates the full truth table
- Shows satisfying assignments
- Shows final SATISFIABLE or UNSATISFIABLE result
- Counts total assignments and satisfying assignments
- Highlights satisfying rows in the GUI
- Shows execution time
- Dark/light mode toggle
- Clear button
- Random formula generator
- Export truth table to a `.txt` file
- Parentheses checking and friendly syntax errors

## How SAT Solving Works Here

The solver works in these steps:

1. Read the formula typed by the user.
2. Check if parentheses are balanced.
3. Break the formula into tokens like variables, operators, and parentheses.
4. Build a small expression tree.
5. Detect all variables in the formula.
6. Use `itertools.product()` to generate every True/False combination.
7. Evaluate the formula for every combination.
8. If at least one row is true, the formula is SATISFIABLE.

This is not the fastest possible SAT solving method, but it is very good for learning because the truth table is visible.

## Project Structure

```text
sat_solver_project/
|
|-- main.py
|-- solver.py
|-- gui.py
|-- utils.py
|-- README.md
|-- requirements.txt
```

## Installation

Python 3 is required. Tkinter is included with most Python installations.

No external libraries are needed.

## How to Run

Open a terminal inside the project folder and run:

```bash
python main.py
```

If your system uses the Python launcher, this also works:

```bash
py main.py
```

## Example Formulas

```text
(P | Q) & (!P | R) & (!Q | !R)
```

```text
(A or B) and (!A or C)
```

```text
A and !A
```

```text
not A or (B and C)
```

## Example Output

Formula:

```text
(P | Q) & (!P | R) & (!Q | !R)
```

Variables detected:

```text
P, Q, R
```

Truth table:

```text
P Q R Result
T T T False
T T F False
T F T True
T F F False
F T T False
F T F True
F F T False
F F F False
```

Satisfying assignments:

```text
P=True, Q=False, R=True
P=False, Q=True, R=False
```

Final Result:

```text
The formula is SATISFIABLE.
```

## Screenshots

Screenshots can be added here after running the GUI.

```text
[Screenshot of the main GUI]
[Screenshot showing a satisfiable formula]
[Screenshot showing an unsatisfiable formula]
```

## Notes

The program avoids using dangerous `eval()` for the formula. Instead, it parses the expression in a simple way and evaluates the parsed tree.

The formula can contain many variables, but the number of rows grows quickly because a truth table has `2^n` rows for `n` variables.

## Future Improvements

- Add implication (`->`)
- Add biconditional (`<->`)
- Save results as CSV
- Add a better random formula generator
- Add a small help window in the GUI
- Add command line mode besides the GUI
