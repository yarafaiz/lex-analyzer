# ---------------- Lexical Analyzer for C-Minus ----------------
# Name: Yara Faiz -  ID (200034784)
# --------------------------------------------------------------

import tkinter as tk
from tkinter import ttk, messagebox
from enum import Enum

# Define token types
class TokenType(Enum):
    ID = "Identifier"
    NUM = "Number"
    OP = "Operator"
    KW = "Keyword"
    STR = "String"
    BRACKET = "Bracket"
    SEP = "Separator"
    EOF = "End of File"

# Token class
class Token:
    def __init__(self, kind: TokenType, lexeme: str):
        self.kind = kind
        self.lexeme = lexeme

    def __str__(self):
        return f"{self.kind.value:<15} | {self.lexeme}"

# Scanner class
class CMinusScanner:
    def __init__(self, code: str):
        self.code = code
        self.index = 0
        self.keywords = {"int", "void", "if", "else", "while", "return"}

    def peek(self):
        return self.code[self.index + 1] if self.index + 1 < len(self.code) else ''

    def skip_comment(self):
        self.index += 2
        while self.index + 1 < len(self.code):
            if self.code[self.index] == '*' and self.code[self.index + 1] == '/':
                self.index += 2
                return
            self.index += 1
        raise Exception("Unclosed comment")

    def get_next_token(self):
        while self.index < len(self.code):
            char = self.code[self.index]

            if char.isspace():
                self.index += 1
                continue

            if char == '/' and self.peek() == '*':
                self.skip_comment()
                continue

            if char.isdigit():
                return self.scan_number()

            if char.isalpha():
                return self.scan_identifier()

            if char == '"':
                return self.scan_string()

            if char in "+-*/=%!<>":
                return self.scan_operator()

            if char in "()[]{}":
                self.index += 1
                return Token(TokenType.BRACKET, char)

            if char in ";,":
                self.index += 1
                return Token(TokenType.SEP, char)

            raise Exception(f"Unknown character '{char}' at index {self.index}")

        return Token(TokenType.EOF, "")

    def scan_number(self):
        number = ''
        while self.index < len(self.code) and self.code[self.index].isdigit():
            number += self.code[self.index]
            self.index += 1
        return Token(TokenType.NUM, number)

    def scan_identifier(self):
        ident = ''
        while self.index < len(self.code) and self.code[self.index].isalnum():
            ident += self.code[self.index]
            self.index += 1
        if ident in self.keywords:
            return Token(TokenType.KW, ident)
        return Token(TokenType.ID, ident)

    def scan_string(self):
        self.index += 1
        string = ''
        while self.index < len(self.code) and self.code[self.index] != '"':
            string += self.code[self.index]
            self.index += 1
        if self.index >= len(self.code):
            raise Exception("Unterminated string literal")
        self.index += 1
        return Token(TokenType.STR, string)

    def scan_operator(self):
        op = self.code[self.index]
        self.index += 1
        if self.index < len(self.code):
            double = op + self.code[self.index]
            if double in {"==", "!=", "<=", ">="}:
                self.index += 1
                return Token(TokenType.OP, double)
        return Token(TokenType.OP, op)

# ---------------- GUI ----------------

def run_scanner():
    code = input_text.get("1.0", tk.END).strip()
    result_listbox.delete(0, tk.END)

    if not code:
        status_var.set("Please enter some C-Minus code.")
        return

    try:
        lexer = CMinusScanner(code)
        tokens = []

        while True:
            tok = lexer.get_next_token()
            if tok.kind == TokenType.EOF:
                break
            tokens.append(tok)

        if tokens:
            result_listbox.insert(tk.END, f"{'Token Type':<15} | Lexeme")
            result_listbox.insert(tk.END, "-" * 40)
            for token in tokens:
                result_listbox.insert(tk.END, str(token))

        status_var.set(f"Scanned {len(tokens)} tokens.")

    except Exception as e:
        status_var.set("Error during scanning.")
        messagebox.showerror("Scanner Error", str(e))

# GUI setup
root = tk.Tk()
root.title("Enhanced C-Minus Scanner")
root.geometry("700x500")
root.minsize(600, 400)

# Input section
ttk.Label(root, text="C-Minus Code Input:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
input_text = tk.Text(root, height=10, wrap="word", font=("Consolas", 11))
input_text.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

# Result section
ttk.Label(root, text="Scanner Output:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
result_frame = ttk.Frame(root)
result_frame.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")

result_listbox = tk.Listbox(result_frame, font=("Courier New", 10))
scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=result_listbox.yview)
result_listbox.config(yscrollcommand=scrollbar.set)
result_listbox.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Button and status
ttk.Button(root, text="Scan Code", command=run_scanner).grid(row=4, column=0, pady=10)
status_var = tk.StringVar()
ttk.Label(root, textvariable=status_var, foreground="blue").grid(row=5, column=0, sticky="w", padx=10, pady=5)

# Grid resizing behavior
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)

root.mainloop()
