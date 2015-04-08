# coding=utf-8
"""
CS 364 Programming Languages
Author: Vela Dimitrova Mineva
Date: 03/06/2015
"""


def generate_code():
    """
    A type code generator
    :return: None
    """
    index = 1
    while True:
        yield index
        index += 1


code = generate_code().__next__

# All CLite tokens
UNRECOGNIZED_TOKEN = (code(), "UNRECOGNIZED TOKEN")
INTLIT = (code(), "Integer literal", "^\d+$")
REAL_NUMBER = (code(), "Real number", "(^\d+\.\d+$)")
ID = (code(), "Identifier", "^(_|[a-zA-Z])\w*$")
KEYWORD = "Keyword"

NOT = "!"
MINUS = "-"
PLUS = "+"
TIMES = "*"
DIVIDE = "/"
MOD = "%"
ASSIGN = "="
LPAREN = "("
RPAREN = ")"
LBRACE = "{"
RBRACE = "}"
LESS = "<"
GREATER = ">"
COMMA = ","
SEMICOLON = ";"
OR = "||"
AND = "&&"
NOT_EQUAL = "!="
EQUAL_EQ = "=="
GREATER_EQ = ">="
LESS_EQ = "<="
EXPONENT = "**"

MAIN = "main"
BOOL = "bool"
TRUE = "true"
FALSE = "false"
IF = "if"
ELSE = "else"
INT = "int"
FLOAT = "float"
CHAR = "char"
WHILE = "while"
PRINT = "print"

# Clite keywords
KEYWORDS = {
    MAIN: code(), BOOL: code(), TRUE: code(), FALSE: code(), IF: code(),
    ELSE: code(), INT: code(), FLOAT: code(), CHAR: code(), WHILE: code(), PRINT: code()
}

# Clite one-character tokens
SINGLE_TOKENS = {
    SEMICOLON: (code(), "Semicolon"), COMMA: (code(), "Comma"), LBRACE: (code(), "Left brace"),
    RBRACE: (code(), "Right brace"), LPAREN: (code(), "Left paren"), RPAREN: (code(), "Right paren"),
    LESS: (code(), "Less"), GREATER: (code(), "Greater"), ASSIGN: (code(), "Assignment"),
    PLUS: (code(), "Plus"), MINUS: (code(), "Minus"), TIMES: (code(), "Multiplication"),
    DIVIDE: (code(), "Division"), NOT: (code(), "Not"), MOD: (code(), "Mod")
}

# Clite more-than-one character tokens
COMPLEX_TOKENS = {
    OR: (code(), "Logical OR"), AND: (code(), "Logical AND"),  NOT_EQUAL: (code(), "Not equal"),
    EQUAL_EQ: (code(), "equal-equal"), GREATER_EQ: (code(), "Greater-equal"),
    LESS_EQ: (code(), "Less-equal"), EXPONENT: (code(), "Exponential-operator")
}

# Clite type codes
TYPES = [KEYWORDS[INT], KEYWORDS[BOOL], KEYWORDS[FLOAT], KEYWORDS[CHAR]]

# Clite numerical types
NUMERICALS = [INT, FLOAT]

# Other codes
END_OF_FILE = 0, "End of file"