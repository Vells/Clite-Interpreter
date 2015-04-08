# coding=utf-8
"""
CS 364 Programming Languages
Author: Vela Dimitrova Mineva
Date: 03/28/2015
"""


class CliteUnrecognizedTokenError(Exception):
    """
    CliteUnrecognizedTokenError is raised when the parser encounters
    unrecognized token while processing the file. The associated value
    is a string indicating what precisely went wrong.
    """

    def __init__(self, token, line_number):
        super().__init__()
        self.token = token
        self.line_number = line_number

    def __str__(self):
        return "CliteUnrecognizedTokenError at line {0}:" \
               " Unrecognized token'{1}'!".format(self.line_number, self.token)


class CliteSyntaxError(Exception):
    """
    A Class that represents a syntax error in Clite.
    A CliteSyntaxError is raised when the parser encounters
    a syntax error. The associated value is a string indicating
    what precisely went wrong.
    """

    def __init__(self, msg, line_number=-1):
        super().__init__()
        self.msg = msg
        self.line_number = line_number

    def __str__(self):
        if self.line_number == -1:
            return self.msg
        else:
            return "SyntaxError at line {0}: {1}".format(self.line_number, self.msg)


class CliteRuntimeError(Exception):
    """
    A Class that represents a runtime error in Clite.
    It is raised when an invalid operation is attempted.
    The associated value is a string indicating
    what precisely went wrong.
    """

    def __init__(self, msg, line=-1):
        super().__init__()
        self.msg = msg
        self.line_number = line

    def __str__(self):
        if self.line_number == -1:
            return self.msg
        else:
            return "RunTimeError at line {0}: {1}".\
                format(self.line_number, self.msg)


class CliteTypeError(CliteRuntimeError):
    """
    A Class that represents a type error in Clite.
    It is raised when an operation is applied to an object
    of inappropriate type. The associated value is a string
    indicating what precisely went wrong.
    """

    def __init__(self, msg="", line=-1, type1=None, type2=None):
        super().__init__(msg, line)
        self.first_type = type1
        self.second_type = type2

    def __str__(self):
        if not self.msg and self.first_type and self.second_type:
            self.msg = "Unsupported operand type(s): {} and {}!".\
                format(self.first_type, self.second_type)
        if self.line_number == -1:
            return self.msg
        else:
            return "TypeError at line {0}: {1}".\
                format(self.line_number, self.msg)