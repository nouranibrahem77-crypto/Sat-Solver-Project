import tkinter as tk
from tkinter import filedialog, messagebox

from solver import make_text_report, solve_formula
from utils import assignment_to_text, format_bool, long_bool, make_random_formula


class SatSolverApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("SAT Solver for Logic Problems")
        self.geometry("900x650")
        self.minsize(750, 520)

        self.dark_mode = False
        self.last_result = None

        self.build_widgets()
        self.apply_theme()

    def build_widgets(self):
        self.main_frame = tk.Frame(self, padx=14, pady=12)
        self.main_frame.pack(fill="both", expand=True)

        self.title_label = tk.Label(
            self.main_frame,
            text="SAT Solver for Logic Problems Using Discrete Mathematics",
            font=("Arial", 16, "bold"),
        )
        self.title_label.pack(anchor="w", pady=(0, 10))

        self.input_label = tk.Label(self.main_frame, text="Enter logical formula:")
        self.input_label.pack(anchor="w")

        self.input_box = tk.Text(self.main_frame, height=3, wrap="word", font=("Consolas", 11))
        self.input_box.pack(fill="x", pady=(4, 8))
        self.input_box.insert("1.0", "(P | Q) & (!P | R) & (!Q | !R)")

        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(fill="x", pady=(0, 10))

        self.solve_button = tk.Button(self.button_frame, text="Solve", width=12, command=self.solve_clicked)
        self.solve_button.pack(side="left", padx=(0, 6))

        self.clear_button = tk.Button(self.button_frame, text="Clear", width=12, command=self.clear_clicked)
        self.clear_button.pack(side="left", padx=(0, 6))

        self.random_button = tk.Button(self.button_frame, text="Random Formula", width=16, command=self.random_clicked)
        self.random_button.pack(side="left", padx=(0, 6))

        self.export_button = tk.Button(self.button_frame, text="Export TXT", width=12, command=self.export_clicked)
        self.export_button.pack(side="left", padx=(0, 6))

        self.theme_button = tk.Button(self.button_frame, text="Dark Mode", width=12, command=self.toggle_theme)
        self.theme_button.pack(side="left")

        self.output_label = tk.Label(self.main_frame, text="Output:")
        self.output_label.pack(anchor="w")

        self.output_frame = tk.Frame(self.main_frame)
        self.output_frame.pack(fill="both", expand=True, pady=(4, 0))

        self.output_box = tk.Text(self.output_frame, wrap="none", font=("Consolas", 10))
        self.output_box.pack(side="left", fill="both", expand=True)

        self.scroll_y = tk.Scrollbar(self.output_frame, orient="vertical", command=self.output_box.yview)
        self.scroll_y.pack(side="right", fill="y")
        self.output_box.configure(yscrollcommand=self.scroll_y.set)

        self.scroll_x = tk.Scrollbar(self.main_frame, orient="horizontal", command=self.output_box.xview)
        self.scroll_x.pack(fill="x")
        self.output_box.configure(xscrollcommand=self.scroll_x.set)

    def apply_theme(self):
        if self.dark_mode:
            colors = {
                "bg": "#202124",
                "panel": "#2b2c30",
                "text": "#f1f1f1",
                "entry": "#151619",
                "button": "#3a3b40",
                "button_text": "#ffffff",
                "sat_bg": "#24452d",
                "sat_fg": "#d9ffd9",
                "error": "#ffb0b0",
            }
            self.theme_button.config(text="Light Mode")
        else:
            colors = {
                "bg": "#f4f4f4",
                "panel": "#ffffff",
                "text": "#111111",
                "entry": "#ffffff",
                "button": "#e8e8e8",
                "button_text": "#111111",
                "sat_bg": "#dff4df",
                "sat_fg": "#003d0b",
                "error": "#a40000",
            }
            self.theme_button.config(text="Dark Mode")

        self.configure(bg=colors["bg"])
        self.main_frame.configure(bg=colors["bg"])
        self.button_frame.configure(bg=colors["bg"])
        self.output_frame.configure(bg=colors["bg"])

        labels = [self.title_label, self.input_label, self.output_label]
        for label in labels:
            label.configure(bg=colors["bg"], fg=colors["text"])

        buttons = [
            self.solve_button,
            self.clear_button,
            self.random_button,
            self.export_button,
            self.theme_button,
        ]
        for button in buttons:
            button.configure(bg=colors["button"], fg=colors["button_text"], activebackground=colors["panel"])

        self.input_box.configure(bg=colors["entry"], fg=colors["text"], insertbackground=colors["text"])
        self.output_box.configure(bg=colors["entry"], fg=colors["text"], insertbackground=colors["text"])

        self.output_box.tag_configure("satisfying", background=colors["sat_bg"], foreground=colors["sat_fg"])
        self.output_box.tag_configure("error", foreground=colors["error"])
        self.output_box.tag_configure("heading", font=("Consolas", 10, "bold"))

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def solve_clicked(self):
        formula = self.input_box.get("1.0", "end").strip()
        self.output_box.delete("1.0", "end")

        try:
            # debug=True gives a few useful lines in the terminal while testing.
            result = solve_formula(formula, debug=True)
            self.last_result = result
            self.show_result(result)
        except Exception as error:
            self.last_result = None
            self.output_box.insert("end", "Error while solving formula:\n", "heading")
            self.output_box.insert("end", str(error) + "\n", "error")

    def show_result(self, result):
        self.output_box.insert("end", "Formula:\n", "heading")
        self.output_box.insert("end", result.original_formula + "\n\n")

        self.output_box.insert("end", "Variables detected:\n", "heading")
        self.output_box.insert("end", ", ".join(result.variables) + "\n\n")

        self.output_box.insert("end", "Truth Table:\n", "heading")
        header = " ".join(result.variables + ["Result"])
        self.output_box.insert("end", header + "\n")
        self.output_box.insert("end", "-" * max(len(header), 20) + "\n")

        for row in result.truth_rows:
            line_values = []
            for var in result.variables:
                line_values.append(format_bool(row["assignment"][var]))
            line_values.append(long_bool(row["result"]))
            line = " ".join(line_values) + "\n"

            if row["result"]:
                self.output_box.insert("end", line, "satisfying")
            else:
                self.output_box.insert("end", line)

        self.output_box.insert("end", "\nSatisfying assignments:\n", "heading")
        if result.satisfying_assignments:
            for assignment in result.satisfying_assignments:
                self.output_box.insert("end", assignment_to_text(assignment) + "\n", "satisfying")
        else:
            self.output_box.insert("end", "No satisfying assignment was found.\n")

        self.output_box.insert("end", "\n")
        self.output_box.insert("end", f"Total assignments: {result.total_assignments}\n")
        self.output_box.insert("end", f"Satisfying assignments: {result.satisfying_count}\n")
        self.output_box.insert("end", f"Execution time: {result.execution_time:.6f} seconds\n\n")

        self.output_box.insert("end", "Final Result:\n", "heading")
        if result.is_satisfiable:
            self.output_box.insert("end", "The formula is SATISFIABLE.\n", "satisfying")
        else:
            self.output_box.insert("end", "The formula is UNSATISFIABLE.\n")

    def clear_clicked(self):
        self.input_box.delete("1.0", "end")
        self.output_box.delete("1.0", "end")
        self.last_result = None

    def random_clicked(self):
        formula = make_random_formula()
        self.input_box.delete("1.0", "end")
        self.input_box.insert("1.0", formula)
        print("[debug] random formula:", formula)

    def export_clicked(self):
        if self.last_result is None:
            messagebox.showinfo("Export", "Solve a formula first, then export the truth table.")
            return

        file_path = filedialog.asksaveasfilename(
            title="Save truth table",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )

        if file_path == "":
            return

        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(make_text_report(self.last_result))
            messagebox.showinfo("Export", "Truth table exported successfully.")
        except Exception as error:
            messagebox.showerror("Export Error", str(error))
