# coding=utf-8
"""
CS 364 Programming Languages
Author: Vela Dimitrova Mineva
Date: 03/28/2015
"""
import sys

import errors
import tokens


class Program(object):
    """
    A Class that represents the program.
    """
    env = {}
    decls = {}

    # Number of leading spaces added at each level
    INDENT_SIZE = 4

    def __init__(self, decls, level):
        # decls is a dictionary of the form { 'identifier': 'type_name' }
        Program.decls = decls
        self.level = level

        # Add each declaration to the environment
        for declaration in decls:
            Program.env[declaration] = None

    def add_statements(self, statements):
        """
        A method that adds statements to the Program object
        :param statements:
        :return: None
        """
        self.stmts = statements

    def __str__(self):
        """
        Return the string representation of a Program object.
        :return: type - string
        """
        # Spaces takes care of the proper indentation
        spaces = Program.INDENT_SIZE * self.level * ' '

        # Add main method code and opening brace to string
        string = "int main() {"
        # Add declarations to string
        for d in Program.decls:
            string += "\n{0}{1} {2};".format(spaces, Program.decls[d], d)
        # Add statements to string
        for statement in self.stmts:
            string += statement.__str__()
        # Add final closing brace
        string += "\n}"

        return string

    def eval(self):
        """
        A method that evaluates all statements in the Program object.
        If a CliteTypeError or a CliteRuntimeError exception is caught,
        the corresponding error message is printed and the program is terminated.
        :return None
        """
        try:
            for statement in self.stmts:
                statement.eval()
        except errors.CliteTypeError as e:
            print(e)
            sys.exit(0)
        except errors.CliteRuntimeError as e:
            print(e)
            sys.exit(0)


# ######### Statements #############

class Statement(object):
    """
    A base class that represents a statement.
    """
    pass


class IfStatement(Statement):
    """
    A class that represents an IfStatement object.
    Inherits the Statement base class.
    """

    def __init__(self, expression, if_stmt, else_stmt, level):
        super().__init__()
        self.expression = expression
        self.if_statement = if_stmt
        self.else_statement = else_stmt
        self.level = level

    def __str__(self):
        """
        Return the string representation of an IfStatement object.
        :return: type - string
        """
        spaces = Program.INDENT_SIZE * self.level * ' '
        string = "\n{0}if ({1}){2}".format(spaces, self.expression.__str__(),
                                           self.if_statement.__str__())
        if self.else_statement:
            string += "\n{0}else{1}".format(spaces,
                                            self.else_statement.__str__())
        return string

    def eval(self):
        """
        A method that returns an evaluated statement if the expression in
        the if expression is evaluated to true; if the if expression is
        evaluated to false and there is an else, the evaluated else
        statement is returned.
        :return Statement Object
        """
        evaluated_expression = self.expression.eval()
        if evaluated_expression:
            return self.if_statement.eval()
        elif self.else_statement:
            return self.else_statement.eval()


class WhileStatement(Statement):
    """
    A class that represents a WhileStatement object.
    Inherits the Statement base class.
    """

    def __init__(self, expression, statement, level):
        super().__init__()
        self.expression = expression
        self.statement = statement
        self.level = level

    def __str__(self):
        """
        Return the string representation of a WhileStatement object.
        :return: type - string
        """
        spaces = Program.INDENT_SIZE * self.level * ' '
        string = "\n{0}while ({1}){2}".\
            format(spaces, self.expression.__str__(),
                   self.statement.__str__())
        return string

    def eval(self):
        """
        A method that evaluated the statement in the while blog until
        the while expression is evaluated to true.
        :return None
        """
        while self.expression.eval():
            self.statement.eval()


class PrintStatement(Statement):
    """
    A class that represents a PrintStatement object.
    Inherits the Statement base class.
    """

    def __init__(self, expression, level):
        super().__init__()
        self.expression = expression
        self.level = level

    def __str__(self):
        """
        Return the string representation of a PrintStatement object.
        :return: type - string
        """
        spaces = Program.INDENT_SIZE * self.level * ' '
        string = "\n{0}print({1});".\
            format(spaces, self.expression.__str__())
        return string

    def eval(self):
        """
        A method that prints the evaluated expression in the
        PrintStatement object
        :return: None
        """
        print(self.expression.eval())
        return None


class Assignment(Statement):
    """
    A class that represents an Assignment statement.
    Inherits the Statement base class.
    """

    def __init__(self, identifier, expr, level):
        super().__init__()
        self.identifier = identifier
        self.expr = expr
        self.level = level

    def __str__(self):
        """
        Return the string representation of an Assignment object
        :return: type - string
        """
        spaces = Program.INDENT_SIZE * self.level * ' '
        return "\n{0}{1} = {2};".format(spaces, self.identifier, self.expr)

    def eval(self):
        """
        A method that evaluates an identifier to its corresponding value
        :return a value of the identifier's type
        """
        Program.env[self.identifier] = self.expr.eval()
        return Program.env[self.identifier]


class Semicolon(Statement):
    """
    A class that represents a Semicolon statement.
    Inherits the Statement base class.
    """

    def __init__(self, level):
        super().__init__()
        self.level = level

    def __str__(self):
        """
        Return the string representation of a Semicolon object
        :return: type - string
        """
        spaces = Program.INDENT_SIZE * self.level * ' '
        return "\n{0};".format(spaces)

    @staticmethod
    def eval():
        """
        A semicolon is evaluated to None.
        :return None
        """
        return


class Block(Statement):
    """
    A class that represents a block.
    Inherits the Statement base class.
    """

    def __init__(self, statements, level):
        super().__init__()
        self.statements = statements
        self.level = level

    def __str__(self):
        """
        Return the string representation of a Block object
        :return: type - string
        """
        spaces = Program.INDENT_SIZE * (self.level - 1) * ' '
        block = " {"
        for statement in self.statements:
            block += statement.__str__()
        block += "\n" + spaces + "}"
        return block

    def eval(self):
        """
        A method that evaluates all statements in the program
        :return None
        """
        for statement in self.statements:
            statement.eval()


# ######## Expressions ############

class Expression(object):
    """
    A base class that represents an expression.
    """
    pass


class BinaryExpression(Expression):
    """
    A base class that represents a binary expression.
    Inherits the Expression base class.
    """

    def __init__(self, left, right, line_number=-1):
        super().__init__()
        self.left = left
        self.right = right
        self.line_number = line_number

    def str(self, operator):
        """
        Given an operator, return the string representation
        of a BinaryExpression object.
        :param operator: A Clite operator
        :return: type - string
        """
        return "{0} {1} {2}".format(self.left.__str__(), operator,
                                    self.right.__str__())

    def type(self):
        """
        A method that returns the type of Clite value of a Binary Expression
        :return: string
        """
        left_type = self.left.type()
        right_type = self.right.type()

        if left_type == "bool" or right_type == "bool":
            raise errors.CliteTypeError("Incompatible types")
        if left_type == "float" and right_type == "int":
            return "float"
        elif left_type == "int" and right_type == "float":
            return "float"
        else:
            return left_type

    def validate_boolean_expression(self):
        """
        A method that checks if a binary expression
        is a valid boolean expression
        :return True if no the expression is valid
        :raise CliteTypeError if the expression is not valid
        """
        left_type = self.left.type()
        right_type = self.right.type()
        if left_type != tokens.BOOL or right_type != tokens.BOOL:
            raise errors.CliteTypeError(line=self.line_number,
                                        type1=left_type, type2=right_type)
        return True

    def validate_numerical_expression(self):
        """
        A method that checks if a binary expression
        is a valid numerical expression
        :return True if no the expression is valid
        :raise CliteTypeError if the expression is not valid
        """
        left_type = self.left.type()
        right_type = self.right.type()
        if left_type not in tokens.NUMERICALS or \
           right_type not in tokens.NUMERICALS:
            raise errors.CliteTypeError(line=self.line_number,
                                        type1=left_type, type2=right_type)
        return True

    def validate_type_compatibility(self):
        """
        A method that checks if the operands of a binary expression are
        compatible and raises a CliteTypeError if they are not
        :return True if the operands are compatible
        :raise CliteTypeError is raised if operands are not compatible
        """
        left_type = self.left.type()
        right_type = self.right.type()
        if left_type != right_type and (left_type not in tokens.NUMERICALS or
                                        right_type not in tokens.NUMERICALS):
            raise errors.CliteTypeError(line=self.line_number,
                                        type1=left_type, type2=right_type)
        return True


class Conjunction(BinaryExpression):
    """
    A class that represents a conjunction expression.
    Inherits the Expression base class.
    """

    def __str__(self):
        """
        Return the string representation of a Conjunction object
        :return: type - string
        """
        super().str(tokens.OR)

    def eval(self):
        """
        A method that evaluates a Conjunction expression if the
        expression is valid
        :return an evaluated boolean expression; type - bool
        :raise CliteTypeError raised when an operation is applied to an
               object of inappropriate type
        """
        self.validate_boolean_expression()
        return self.left.eval() or self.right.eval()


class Equality(BinaryExpression):
    """
    A class that represents an equality relation expression.
    Inherits the Expression base class.
    """

    def __str__(self):
        """
        Return the string representation of an Equality object
        :return: type - string
        """
        return super().str(tokens.AND)

    def eval(self):
        """
        A method that evaluates an Equality expression if the
        expression is valid
        :return an evaluated boolean expression; type - bool
        :raise CliteTypeError raised when an operation is applied to an
               object of inappropriate type
        """
        self.validate_boolean_expression()
        return self.left.eval() and self.right.eval()


class BinaryEqualOpExpression(BinaryExpression):
    """
    A class that represents a binary equal operation expression.
    Inherits the BinaryExpression base class.
    """

    def __str__(self):
        """
        Return the string representation of a BinaryEqualOpExpression object
        :return: type - string
        """
        return super().str(tokens.EQUAL_EQ)

    def eval(self):
        """
        A method that evaluates a BinaryEqualOpExpression if the
        expression is valid
        :return an evaluated boolean expression; type - bool
        :raise CliteTypeError raised when an operation is applied to an
               object of inappropriate type
        """
        self.validate_type_compatibility()
        return self.left.eval() == self.right.eval()


class BinaryNotEqualOpExpression(BinaryExpression):
    """
    A class that represents a binary not equal operation expression.
    Inherits the BinaryExpression base class.
    """

    def __str__(self):
        """
        Return the string representation of a BinaryNotEqualOpExpression object
        :return: type - string
        """
        return super().str(tokens.NOT_EQUAL)

    def eval(self):
        """
        A method that evaluates a BinaryNotEqualOpExpression
        :return an evaluated boolean expression; type - bool
        :raise CliteTypeError raised when an operation is applied to an
               object of inappropriate type
        """
        self.validate_type_compatibility()
        return self.left.eval() != self.right.eval()


class BinaryLessExpression(BinaryExpression):
    """
    A class that represents a binary less relation expression.
    Inherits the BinaryExpression base class.
    """

    def __str__(self):
        """
        Return the string representation of a BinaryLessExpression object
        :return: type - string
        """
        return super().str(tokens.LESS)

    def eval(self):
        """
        A method that evaluates a BinaryLessExpression
        :return an evaluated boolean expression; type - bool
        :raise CliteTypeError raised when an operation is applied to an
               object of inappropriate type
        """
        self.validate_numerical_expression()
        return self.left.eval() < self.right.eval()


class BinaryLessEqualExpression(BinaryExpression):
    """
    A class that represents a binary less or equal relation expression.
    Inherits the BinaryExpression base class.
    """

    def __str__(self):
        """
        Return the string representation of a BinaryLessEqualExpression object
        :return: type - string
        """
        return super().str(tokens.LESS_EQ)

    def eval(self):
        """
        A method that evaluates a BinaryLessEqualExpression
        :return an evaluated boolean expression; type - bool
        :raise CliteTypeError raised when an operation is applied to an
               object of inappropriate type
        """
        self.validate_numerical_expression()
        return self.left.eval() <= self.right.eval()


class BinaryGreaterExpression(BinaryExpression):
    """
    A class that represents a binary greater relation expression.
    Inherits the BinaryExpression base class.
    """

    def __str__(self):
        """
        Return the string representation of a BinaryGreaterExpression object
        :return: type - string
        """
        return super().str(tokens.GREATER)

    def eval(self):
        """
        A method that evaluates a BinaryGreaterExpression
        :return an evaluated boolean expression; type - bool
        :raise CliteTypeError raised when an operation is applied to an
               object of inappropriate type
        """
        self.validate_numerical_expression()
        return self.left.eval() > self.right.eval()


class BinaryGreaterEqualExpression(BinaryExpression):
    """
    A class that represents a binary greater or equal relation expression.
    Inherits the BinaryExpression base class.
    """

    def __str__(self):
        """
        Return the string representation of a BinaryGreaterEqualExpression object
        :return: type - string
        """
        return super().str(tokens.GREATER_EQ)

    def eval(self):
        """
        A method that evaluates a BinaryGreaterEqualExpression
        :return an evaluated boolean expression; type - bool
        :raise CliteTypeError raised when an operation is applied to an
               object of inappropriate type
        """
        self.validate_numerical_expression()
        return self.left.eval() >= self.right.eval()


class BinaryAddOpExpression(BinaryExpression):
    """
    A base class that represents a binary addition operation expression.
    Inherits the BinaryExpression base class.
    """


class BinaryPlusExpression(BinaryAddOpExpression):
    """
    A class that represents a binary addition operation expression.
    Inherits the BinaryAddOpExpression base class.
    """

    def __str__(self):
        """
        Return the string representation of a BinaryPlusExpression object
        :return: type - string
        """
        return "({0} {1} {2})".format(self.left.__str__(), tokens.PLUS,
                                      self.right.__str__())

    def eval(self):
        """
        A method that evaluates a binary plus expression
        :return an evaluated expression of the same type as the terms
        :raise CliteTypeError raised when an operation is applied to an
               object of inappropriate type
        """
        self.validate_numerical_expression()
        return self.left.eval() + self.right.eval()


class BinaryMinusExpression(BinaryAddOpExpression):
    """
    A class that represents a binary addition operation expression.
    Inherits the BinaryAddOpExpression base class.
    """

    def __str__(self):
        """
        Return the string representation of a BinaryMinusExpression object
        :return: type - string
        """
        return "({0} {1} {2})".format(self.left.__str__(), tokens.MINUS,
                                      self.right.__str__())

    def eval(self):
        """
        A method that evaluates a binary minus expression
        :return an evaluated expression of the same type as the terms
        :raise CliteTypeError raised when an operation is applied to an
               object of inappropriate type
        """
        self.validate_numerical_expression()
        return self.left.eval() - self.right.eval()


class BinaryTimesExpression(BinaryExpression):
    """
    A class that represents a binary times operation expression.
    Inherits the BinaryExpression base class.
    """

    def __str__(self):
        """
        Return the string representation of a BinaryTimesExpression object
        :return: type - string
        """
        return super().str(tokens.TIMES)

    def eval(self):
        """
        A method that evaluates a binary times expression
        :return an evaluated expression of the same type as the terms
        :raise CliteTypeError raised when an operation is applied to an
               object of inappropriate type
        """
        self.validate_numerical_expression()
        return self.left.eval() * self.right.eval()


class BinaryDivideExpression(BinaryExpression):
    """
    A class that represents a binary divide operation expression.
    Inherits the BinaryExpression base class.
    """

    def __str__(self):
        """
        Return the string representation of a BinaryDivideExpression object
        :return: type - string
        """
        return super().str(tokens.DIVIDE)

    def eval(self):
        """
        A method that evaluates a binary division expression
        :return an evaluated expression of the same type as the terms
        :raise CliteTypeError raised when an operation is applied to an
               object of inappropriate type
        """
        self.validate_numerical_expression()
        return self.left.eval() / self.right.eval()


class BinaryModExpression(BinaryExpression):
    """
    A class that represents a binary mod operation expression.
    Inherits the BinaryExpression base class.
    """

    def __str__(self):
        """
        Return the string representation of a BinaryModExpression object
        :return: type - string
        """
        return super().str(tokens.MOD)

    def eval(self):
        """
        A method that evaluates a binary mod expression
        :return an evaluated expression of the same type as the terms
        :raise CliteTypeError raised when an operation is applied to an
               object of inappropriate type
        """
        self.validate_numerical_expression()
        return self.left.eval() % self.right.eval()


class BinaryExpExpression(BinaryExpression):
    """
    A class that represents a binary exponentiation operation expression.
    Inherits the BinaryExpression base class.
    """

    def __str__(self):
        """
        Return the string representation of a BinaryExponentiationExpression object
        :return: type - string
        """
        return "({0} {1} {2})".format(self.left.__str__(), tokens.EXPONENT,
                                      self.right.__str__())

    def eval(self):
        """
        A method that evaluates a binary exponentiation expression
        :return an evaluated expression of the same type as the terms
        :raise CliteTypeError raised when an operation is applied to an
               object of inappropriate type
        """
        self.validate_numerical_expression()
        return self.left.eval() ** self.right.eval()


class Factor(Expression):
    """
    A class that represents a factor where Factor -> [ UnaryOp ] Primary.
    Inherits the Expression base class
    """

    def __init__(self, primary, unary_operator, line_number):
        self.primary = primary
        self.unary_operator = unary_operator
        self.line_number = line_number

    def __str__(self):
        """
        Return the string representation of a Factor object
        :return: type - string
        """
        string = ''
        if self.unary_operator:
            string = self.unary_operator
        string += self.primary.__str__()
        return string

    def type(self):
        """
        A method that returns the type of a Clite Factor object
        :return: type - string
        """
        return self.primary.type()

    def eval(self):
        """
        A method that evaluates a Factor expressions and
        returns the result of the corresponding type
        :return: type - int, float or boolean
        :raise CliteRuntimeError when unary operator is
               applied to an incompatible type
        """
        if not self.unary_operator:
            return self.primary.eval()

        primary_type = self.primary.type()

        if (self.unary_operator != tokens.NOT and primary_type == tokens.BOOL) or\
           (self.unary_operator == tokens.NOT and primary_type != tokens.BOOL):
            message = "The operator {0} is undefined for the argument type(s) {1}".\
                format(self.unary_operator, primary_type)
            raise errors.CliteRuntimeError(message, self.line_number)

        elif self.unary_operator == tokens.NOT and primary_type == tokens.BOOL:
            return not self.primary.eval()

        else:
            return - self.primary.eval()


class Primary(Expression):
    """
    A base class that represents a Primary expression
    Inherits the Expression class
    """
    pass


class IdentifierExpression(Primary):
    """
    A class that represents an identifier.
    Inherits the Primary base class.
    """

    def __init__(self, identifier, line_number):
        super().__init__()
        self.identifier = identifier
        self.line_number = line_number

    def __str__(self):
        """
        Return the string representation of an IdentifierExpression
        :return: type - string
        """
        return self.identifier

    def type(self):
        """
        A method that returns the type of a Clite IdentifierExpression
        :return: type - string
        """
        return Program.decls[self.identifier]

    def eval(self):
        """
        A method that evaluates an IdentifierExpression object and
        returns the result of the corresponding type
        :return: type - int
        :raise CliteRuntimeError when identifier is not defined
        """
        if Program.env[self.identifier] is None:
            raise errors.CliteRuntimeError(self.identifier + " not defined!",
                                           self.line_number)
        return Program.env[self.identifier]


class Number(Primary):
    """
    A base class that represents a Primary expression
    Inherits the Primary class. Evaluates to a number
    """
    pass


class IntLitExpression(Number):
    """
    A class that represents an integer literal expression.
    Inherits the Primary base class.
    """

    def __init__(self, intlit, line_number):
        super().__init__()
        self.intlit = intlit
        self.line_number = line_number

    def __str__(self):
        """
        Return the string representation of an IntLitExpression
        :return: type - string
        """
        return str(self.intlit)

    @staticmethod
    def type():
        """
        A method that returns the type of Clite value of a string
        :return: type - string
        """
        return "int"

    def eval(self):
        """
        A method that evaluates an IntLitExpression object and
        returns the result of type int. If the past argument throws a
        ValueError when trying to convert it to an integer,
        the program is terminated.
        :return: type - int
        :raise ValueError is raised when an inappropriate value is passed
        """
        try:
            number = int(self.intlit)
        except ValueError:
            print("Invalid literal for an integer with "
                  "base 10 at line {}!".format(self.line_number))
            sys.exit(0)
        else:
            return number


class RealNumberExpression(Number):
    """
    A class that represents a real number expression.
    Inherits the Primary base class
    """

    def __init__(self, real_number, line_number):
        super().__init__()
        self.real_number = real_number
        self.line_number = line_number

    def __str__(self):
        """
        Return the string representation of a RealNumberExpression
        :return: type - string
        """
        return str(self.real_number)

    @staticmethod
    def type():
        """
        A method that returns the type of Clite value of a string
        :return: type - string
        """
        return "float"

    def eval(self):
        """
        A method that evaluates a RealNumberExpression object and
        returns the result of type float. If the past argument throws a
        ValueError when trying to convert it to a float,
        the program is terminated.
        :return: type - float
        :raise ValueError is raised when an inappropriate value is passed
        """
        try:
            number = float(self.real_number)
        except ValueError:
            print("Invalid literal for a float at line {}!".
                  format(self.line_number))
            sys.exit(0)
        else:
            return number


class BooleanExpression(Primary):
    """
    A base class that represents a boolean expression.
    Inherits the Primary base class
    """

    def __init__(self, bool_value):
        super().__init__()
        self.bool = bool_value

    def __str__(self):
        """
        Return the string representation of a BooleanExpression
        :return: type - string
        """
        return str(self.bool)

    @staticmethod
    def type():
        """
        A method that returns the type of a Clite BooleanExpression
        :return: type - string
        """
        return "bool"


class TrueExpression(BooleanExpression):
    """
    A Class that represents an expression evaluated to true.
    Inherits the BooleanExpression base class.
    """

    @staticmethod
    def eval():
        """
        A method that evaluates a FalseExpression object and
        returns the result of type boolean
        :return: type - boolean
        """
        return True


class FalseExpression(BooleanExpression):
    """
    A Class that represents an expression evaluated to false.
    Inherits the BooleanExpression base class.
    """

    @staticmethod
    def eval():
        """
        A method that evaluates a FalseExpression object and
        returns the result of type boolean
        :return: type - boolean
        """
        return False