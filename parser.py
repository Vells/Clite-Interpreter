# coding=utf-8
"""
CS 364 Programming Languages
Author: Vela Dimitrova Mineva
Date: 03/28/2015
"""
import os
import sys

import lexer
import tokens
import errors
import ast


class Parser(object):
    """
    Parser class encapsulates all parsing functions.
    There is one public function called parse().
    """

    # Positions of the indicated token features
    # in the tuple returned by lexer
    CODE = 0
    TYPE = 1
    VALUE = 2
    LINE = 3

    def __init__(self, filename):
        try:
            self.check_validity(filename)
        except IOError as error:
            print(error, end="")
            sys.exit(1)
        self.filename = filename
        self.vellexer = lexer.Lexer(filename)
        try:
            self.lex = self.vellexer.token_generator()
        except errors.CliteUnrecognizedTokenError as error:
            print(error, end="")
            sys.exit(1)
        # Retrieve the first token in the file
        self.curr_tok = self.lex.__next__()

    @staticmethod
    def check_validity(filename):
        """
        A function that checks if the given filename is a valid path
        to a file and raises an IOError if it is not.
        :param filename: type(filename) is a string; len(filename) > 0
        :return: None (on a valid filename)
        :raise IOError
        """
        if not os.path.exists(filename):
            raise IOError("The file {0} does not exist!\n".format(filename))
        elif not os.path.isfile(filename):
            raise IOError("Could not open {0}!\n".format(filename))
        return

    def parse(self):
        """
        Parse a Clite file
        :return: An ast.Program object
        :raise CliteSyntaxError if an unexpected token is seen
        """
        program = self.program()

        if self.curr_tok[self.CODE] != tokens.END_OF_FILE[self.CODE]:
            raise errors.CliteSyntaxError("Extra symbols in input.", self.curr_tok[self.LINE])

        return program

    def program(self):
        """
        Program -> int  main '(' ')' '{' Declarations Statements '}'
        :return: An ast.Program object
        :raise CliteSyntaxError if an unexpected token is seen
        """
        # Indicates the level of indentation
        level = 1

        self.match_main()
        self.decls = self.declarations()
        # Create a program object with declarations and a level
        program = ast.Program(self.decls, level)
        # Process statements and add them to the program object
        self.stmts = self.statements(level)
        program.add_statements(self.stmts)

        # Match final closing brace
        if self.curr_tok[self.CODE] != tokens.SINGLE_TOKENS[tokens.RBRACE][self.CODE]:
            raise errors.CliteSyntaxError("Missing final closing brace '}'!",
                                          self.curr_tok[self.LINE])
        # Consume closing brace
        self.curr_tok = self.lex.__next__()

        return program

    def match_main(self):
        """
        A method that matches the top of the program, i.e. int main '(' ')' '{'
        :return: None
        :raise CliteSyntaxError if an unexpected token is seen
        """
        # Match 'int'
        if self.curr_tok[self.CODE] != tokens.KEYWORDS[tokens.INT]:
            raise errors.CliteSyntaxError("Undefined reference to 'main'! Missing return type 'int'!",
                                          self.curr_tok[self.LINE])
        # Consume 'int'
        self.curr_tok = self.lex.__next__()
        # Match main
        if self.curr_tok[self.CODE] != tokens.KEYWORDS[tokens.MAIN]:
            raise errors.CliteSyntaxError("Undefined reference to 'main'! Missing 'main'!",
                                          self.curr_tok[self.LINE])
        # Consume 'main'
        self.curr_tok = self.lex.__next__()
        # Match left opening parenthesis
        if self.curr_tok[self.CODE] != tokens.SINGLE_TOKENS[tokens.LPAREN][self.CODE]:
            raise errors.CliteSyntaxError("Missing opening parenthesis",
                                          self.curr_tok[self.LINE])
        # Consume left opening parenthesis
        self.curr_tok = self.lex.__next__()
        # Match right closing parenthesis
        if self.curr_tok[self.CODE] != tokens.SINGLE_TOKENS[tokens.RPAREN][self.CODE]:
            raise errors.CliteSyntaxError("Missing closing parenthesis!",
                                          self.curr_tok[self.LINE])
        # Consume right closing parenthesis
        self.curr_tok = self.lex.__next__()
        # Match left opening brace
        if self.curr_tok[self.CODE] != tokens.SINGLE_TOKENS[tokens.LBRACE][self.CODE]:
            raise errors.CliteSyntaxError("Missing opening brace '{'!",
                                          self.curr_tok[self.LINE])
        # Consume left opening brace
        self.curr_tok = self.lex.__next__()
        return

    def declarations(self):
        """
        Declarations -> { Declaration }
        :return: A dictionary of declared values, { identifier: type}
        :raise CliteSyntaxError if an unexpected token is seen
        """
        declaration_dict = {}

        while self.curr_tok[self.CODE] in tokens.TYPES:
            declaration = self.declaration()
            identifier = declaration[0][self.VALUE]
            type_name = declaration[1][self.VALUE]

            # Raise an error if trying to declare an already declared identifier
            if identifier in declaration_dict:
                raise errors.CliteSyntaxError('Identifier already declared',
                                              self.curr_tok[self.LINE])
            declaration_dict[identifier] = type_name

        return declaration_dict

    def declaration(self):
        """
        Declaration -> Type Identifier ';'
        :return: A tuple in the form (identifier, type)
        :raise: CliteSyntaxError if an unexpected token is seen
        """
        temp_type = self.curr_tok
        self.curr_tok = self.lex.__next__()

        if self.curr_tok[self.CODE] != tokens.ID[self.CODE]:
            raise errors.CliteSyntaxError("Identifier expected", self.curr_tok[self.LINE])

        temp_identifier = self.curr_tok
        # Consume identifier
        self.curr_tok = self.lex.__next__()

        # Match a semicolon
        if self.curr_tok[self.CODE] != tokens.SINGLE_TOKENS[tokens.SEMICOLON][self.CODE]:
            raise errors.CliteSyntaxError("Semicolon expected", self.curr_tok[self.LINE])
        # Consume semicolon
        self.curr_tok = self.lex.__next__()

        return temp_identifier, temp_type

    def statements(self, level):
        """
        Statements -> { Statement }
        :param level: indicates level of statements in block; type(level) - int
        :return:
        :raise CliteSyntaxError if an unexpected token is seen
        """
        first_set = {
            tokens.SINGLE_TOKENS[tokens.SEMICOLON][self.CODE],
            tokens.SINGLE_TOKENS[tokens.LBRACE][self.CODE],
            tokens.ID[self.CODE], tokens.KEYWORDS[tokens.IF],
            tokens.KEYWORDS[tokens.WHILE], tokens.KEYWORDS[tokens.ELSE],
            tokens.KEYWORDS[tokens.PRINT]
        }
        statements = []

        while self.curr_tok[0] in first_set:
            # Do not consume the token yet
            statements.append(self.statement(level))

        return statements

    def statement(self, level):
        """
        Statement ->  ';' | Block | Assignment | IfStatement
                        | WhileStatement | PrintStatement
        :param level: indicates level of statement; type(level) - int
        :return: None
        :raise CliteSyntaxError if an unexpected token is seen
        """
        if self.curr_tok[self.CODE] == tokens.SINGLE_TOKENS[tokens.SEMICOLON][self.CODE]:
            self.curr_tok = self.lex.__next__()
            return ast.Semicolon(level)
        elif self.curr_tok[self.CODE] == tokens.SINGLE_TOKENS[tokens.LBRACE][self.CODE]:
            return self.block(level)
        elif self.curr_tok[self.CODE] == tokens.ID[self.CODE]:
            return self.assignment(level)
        elif self.curr_tok[self.CODE] == tokens.KEYWORDS[tokens.IF]:
            return self.if_statement(level)
        elif self.curr_tok[self.CODE] == tokens.KEYWORDS[tokens.WHILE]:
            return self.while_statement(level)
        elif self.curr_tok[self.CODE] == tokens.KEYWORDS[tokens.PRINT]:
            return self.print_statement(level)
        else:
            raise errors.CliteSyntaxError("Statement expected!", self.curr_tok[self.LINE])

    def block(self, level):
        """
        Block -> '{' Statements '}'
        :param level: indicates level of statements in block; type(level) - int
        :return: An ast.Block object
        :raise CliteSyntaxError if an unexpected token is seen
        """
        # Consume the opening brace identifying the start of a block
        self.curr_tok = self.lex.__next__()

        statements = self.statements(level)

        # Match right closing brace
        if self.curr_tok[self.CODE] != tokens.SINGLE_TOKENS[tokens.RBRACE][self.CODE]:
            raise errors.CliteSyntaxError("'}' expected!", self.curr_tok[self.LINE])
        # Consume right closing brace
        self.curr_tok = self.lex.__next__()

        return ast.Block(statements, level)

    def if_statement(self, level):
        """
        IfStatement -> if '(' Expression ')' Statement [ else Statement ]
        :param level: indicates level of statements; type(level) - int
        :return: An ast.IfStatement object
        :raise CliteSyntaxError if an unexpected token is seen
        """
        # Consume the keyword if identifying the start of an if statement
        self.curr_tok = self.lex.__next__()

        # Match left opening left parenthesis
        if self.curr_tok[self.CODE] != tokens.SINGLE_TOKENS[tokens.LPAREN][0]:
            raise errors.CliteSyntaxError("'(' expected!", self.curr_tok[self.LINE])
        # Consume opening left parenthesis
        self.curr_tok = self.lex.__next__()

        expression = self.expression()

        # Match right closing left parenthesis
        if self.curr_tok[self.CODE] != tokens.SINGLE_TOKENS[tokens.RPAREN][0]:
            raise errors.CliteSyntaxError("')' expected!", self.curr_tok[self.LINE])
        # Consume closing right parenthesis
        self.curr_tok = self.lex.__next__()

        if_stmt = self.statement(level + 1)
        else_stmt = None

        # If there is an 'else', consume it
        if self.curr_tok[self.CODE] == tokens.KEYWORDS[tokens.ELSE]:
            self.curr_tok = self.lex.__next__()
            else_stmt = self.statement(level + 1)

        return ast.IfStatement(expression, if_stmt, else_stmt, level)

    def while_statement(self, level):
        """
        WhileStatement -> while '(' Expression ')' Statement
        :param level: indicates level of statements; type(level) - int
        :return: ast.WhileStatement object
        :raise CliteSyntaxError if an unexpected token is seen
        """
        # Consume the keyword if identifying the start of a while statement
        self.curr_tok = self.lex.__next__()

        # Match left parenthesis
        if self.curr_tok[self.CODE] != tokens.SINGLE_TOKENS[tokens.LPAREN][0]:
            raise errors.CliteSyntaxError("'(' expected!", self.curr_tok[self.LINE])
        # Consume left parenthesis
        self.curr_tok = self.lex.__next__()

        expression = self.expression()

        # Match right parenthesis
        if self.curr_tok[self.CODE] != tokens.SINGLE_TOKENS[tokens.RPAREN][0]:
            raise errors.CliteSyntaxError("')' expected!", self.curr_tok[self.LINE])
        # Consume right parenthesis
        self.curr_tok = self.lex.__next__()

        statement = self.statement(level + 1)

        return ast.WhileStatement(expression, statement, level)

    def print_statement(self, level):
        """
        PrintStatement -> print '(' Expression ')' ';'
        :param level: indicates level of statement; type(level) - int
        :return: An ast.PrintStatement object
        :raise CliteSyntaxError if an unexpected token is seen
        """
        # Consume the keyword if identifying the start of a print statement
        self.curr_tok = self.lex.__next__()

        # Match left opening parenthesis
        if self.curr_tok[self.CODE] != tokens.SINGLE_TOKENS[tokens.LPAREN][0]:
            raise errors.CliteSyntaxError("'(' expected!", self.curr_tok[self.LINE])
        # Consume left opening parenthesis
        self.curr_tok = self.lex.__next__()

        expression = self.expression()

        # Match right closing parenthesis
        if self.curr_tok[self.CODE] != tokens.SINGLE_TOKENS[tokens.RPAREN][0]:
            raise errors.CliteSyntaxError("')' expected!", self.curr_tok[self.LINE])
        # Consume closing right parenthesis
        self.curr_tok = self.lex.__next__()

        # Match semicolon
        if self.curr_tok[self.CODE] != tokens.SINGLE_TOKENS[tokens.SEMICOLON][0]:
            raise errors.CliteSyntaxError("';' expected!", self.curr_tok[self.LINE])
        # Consume semicolon
        self.curr_tok = self.lex.__next__()

        return ast.PrintStatement(expression, level)

    def assignment(self, level):
        """
        Assignment -> Identifier '=' Expression ';'
        :param level: indicates level of assignment; type(level) - int
        :return: An ast.Assignment object
        :raise CliteSyntaxError if an unexpected token is seen
        """
        # Save and consume identifier
        identifier = self.curr_tok
        self.curr_tok = self.lex.__next__()

        # Match equal sign
        if self.curr_tok[self.CODE] != tokens.SINGLE_TOKENS[tokens.ASSIGN][0]:
            raise errors.CliteSyntaxError("An assignment statement expected!",
                                          self.curr_tok[self.LINE])
        # Consume equal sign
        self.curr_tok = self.lex.__next__()

        expr = self.expression()

        # Match semicolon
        if self.curr_tok[self.CODE] != tokens.SINGLE_TOKENS[tokens.SEMICOLON][0]:
            raise errors.CliteSyntaxError("Semicolon expected!",
                                          self.curr_tok[self.LINE])
        # Consume semicolon
        self.curr_tok = self.lex.__next__()

        # Check if the identifier is declared
        if identifier[2] not in self.decls:
            raise errors.CliteSyntaxError("Identifier is not declared!",
                                          self.curr_tok[self.LINE])

        return ast.Assignment(identifier[2], expr, level)

    def expression(self):
        """
        Expression -> Conjunction { '||' Conjunction }
        :return: A ast.Conjunction object
        """
        left_tree = self.conjunction()

        while self.curr_tok[self.VALUE] == tokens.OR:
            self.curr_tok = self.lex.__next__()
            line_number = self.curr_tok[self.LINE]
            right_tree = self.conjunction()
            left_tree = ast.Conjunction(left_tree, right_tree, line_number)

        return left_tree

    def conjunction(self):
        """
        Conjunction -> Equality { '&&' Equality }
        :return: An ast.Equality object
        """
        left_tree = self.equality()

        while self.curr_tok[self.VALUE] == tokens.AND:
            self.curr_tok = self.lex.__next__()
            line_number = self.curr_tok[self.LINE]
            right_tree = self.equality()
            left_tree = ast.Equality(left_tree, right_tree, line_number)

        return left_tree

    def equality(self):
        """
        Equality -> Relation [ EquOp Relation]
        :return: An ast.BinaryEqualOpExpression or an ast.BinaryNotEqualOpExpression
        :raise CliteSyntaxError if an unexpected token is seen
        """
        left_tree = self.relation

        equality_operators = [tokens.EQUAL_EQ, tokens.NOT_EQUAL]
        # Match equality operator
        if self.curr_tok[self.VALUE] in equality_operators:
            operator = self.curr_tok[self.VALUE]
            self.curr_tok = self.lex.__next__()
            line = self.curr_tok[self.LINE]
            right_tree = self.relation

            if operator == tokens.EQUAL_EQ:
                left_tree = ast.BinaryEqualOpExpression(left_tree, right_tree, line)
            elif operator == tokens.NOT_EQUAL:
                left_tree = ast.BinaryNotEqualOpExpression(left_tree, right_tree, line)
            else:
                raise errors.CliteSyntaxError("Unexpected operator '{0}' given!".
                                              format(operator), self.curr_tok[self.LINE])
        return left_tree

    @property
    def relation(self):
        """
        Relation -> Addition [ RelOp Relation]
        :return: A ast.BinaryExpression object
        :raise CliteSyntaxError if an unexpected token is seen
        """
        left_tree = self.addition()

        relation_operators = [tokens.LESS, tokens.LESS_EQ, tokens.GREATER, tokens.GREATER_EQ]
        # Match relation operator
        if self.curr_tok[self.VALUE] in relation_operators:
            operator = self.curr_tok[self.VALUE]
            self.curr_tok = self.lex.__next__()
            line = self.curr_tok[self.LINE]
            right_tree = self.addition()

            if operator == tokens.LESS:
                left_tree = ast.BinaryLessExpression(left_tree, right_tree, line)
            elif operator == tokens.LESS_EQ:
                left_tree = ast.BinaryLessEqualExpression(left_tree, right_tree, line)
            elif operator == tokens.GREATER:
                left_tree = ast.BinaryGreaterExpression(left_tree, right_tree, line)
            elif operator == tokens.GREATER_EQ:
                left_tree = ast.BinaryGreaterEqualExpression(left_tree, right_tree, line)
            else:
                raise errors.CliteSyntaxError("Unexpected operator '{0}' given!".
                                              format(operator), self.curr_tok[self.LINE])

        return left_tree

    def addition(self):
        """
        Addition -> Term { AddOp Term }
        :return: An ast.BinaryPlusExpression or an ast.BinaryMinusExpression
        :raise CliteSyntaxError if an unexpected token is seen
        """
        left_tree = self.term()

        while self.curr_tok[self.VALUE] == tokens.PLUS or \
                self.curr_tok[self.VALUE] == tokens.MINUS:
            operator = self.curr_tok[self.VALUE]
            self.curr_tok = self.lex.__next__()
            line = self.curr_tok[self.LINE]
            right_tree = self.term()

            if operator == tokens.PLUS:
                left_tree = ast.BinaryPlusExpression(left_tree, right_tree, line)
            elif operator == tokens.MINUS:
                left_tree = ast.BinaryMinusExpression(left_tree, right_tree, line)
            else:
                raise errors.CliteSyntaxError("Unexpected operator '{0}' given!".
                                              format(operator), self.curr_tok[self.LINE])
        return left_tree

    def term(self):
        """
        Term -> RaisedFactor { MulOp RaisedFactor }
        :return: An ast.BinaryExpression object
        :raise CliteSyntaxError if an unexpected token is seen
        """
        left_tree = self.raised_factor()

        mul_operations = [tokens.TIMES, tokens.DIVIDE, tokens.MOD]

        while self.curr_tok[self.VALUE] in mul_operations:
            operator = self.curr_tok[self.VALUE]
            self.curr_tok = self.lex.__next__()
            line = self.curr_tok[self.LINE]
            right_tree = self.raised_factor()

            if operator == tokens.TIMES:
                left_tree = ast.BinaryTimesExpression(left_tree, right_tree, line)
            elif operator == tokens.DIVIDE:
                left_tree = ast.BinaryDivideExpression(left_tree, right_tree, line)
            elif operator == tokens.MOD:
                left_tree = ast.BinaryModExpression(left_tree, right_tree, line)
            else:
                raise errors.CliteSyntaxError("Unexpected operator '{0}' given!".
                                              format(operator), line)
        return left_tree

    def raised_factor(self):
        """
        RaisedFactor -> Factor { '**' Factor }
        :return: An ast.BinaryExpression object
        :raise CliteSyntaxError if an unexpected token is seen
        """
        left_tree = self.factor()

        while self.curr_tok[self.VALUE] == tokens.EXPONENT:
            self.curr_tok = self.lex.__next__()
            line_number = self.curr_tok[self.LINE]
            right_tree = self.factor()
            left_tree = ast.BinaryExpExpression(left_tree, right_tree,
                                                line_number)
        return left_tree

    def factor(self):
        """
        Factor -> [ UnaryOp ] Primary
        :return: An ast. Factor object
        """
        unary_operators = [tokens.MINUS, tokens.NOT]
        unary_operator = None

        # Match unary operator if seen
        if self.curr_tok[self.VALUE] in unary_operators:
            unary_operator = self.curr_tok[self.VALUE]
            self.curr_tok = self.lex.__next__()

        primary = self.primary()
        line_number = self.curr_tok[self.LINE]

        return ast.Factor(primary, unary_operator, line_number)

    def primary(self):
        """
        Primary -> Identifier | IntLit | FloatLit | '(' Expression ')' | 'true' | 'false'
        :return: An ast.Expression object
        :raise CliteSyntaxError if an unexpected token is seen
        """
        line_number = self.curr_tok[self.LINE]
        # Match an identifier
        if self.curr_tok[self.CODE] == tokens.ID[0]:
            identifier = self.curr_tok[2]
            # Raise an error if the identifier is not declared
            if identifier not in self.decls:
                raise errors.CliteSyntaxError("Identifier '{0}' not declared!".format(identifier),
                                              self.curr_tok[self.LINE])
            # Consume identifier
            self.curr_tok = self.lex.__next__()
            return ast.IdentifierExpression(identifier, line_number)

        # Or match an integer literal
        elif self.curr_tok[self.CODE] == tokens.INTLIT[0]:
            int_lit = self.curr_tok[self.VALUE]
            self.curr_tok = self.lex.__next__()
            return ast.IntLitExpression(int_lit, line_number)

        # Or match a real number
        elif self.curr_tok[self.CODE] == tokens.REAL_NUMBER[0]:
            real_number = self.curr_tok[self.VALUE]
            self.curr_tok = self.lex.__next__()
            return ast.RealNumberExpression(real_number, line_number)

        # Or match a 'true'
        elif self.curr_tok[self.CODE] == tokens.KEYWORDS[tokens.TRUE]:
            true_expr = self.curr_tok[self.VALUE]
            self.curr_tok = self.lex.__next__()
            return ast.TrueExpression(true_expr)

        # Or match a 'false'
        elif self.curr_tok[self.CODE] == tokens.KEYWORDS[tokens.FALSE]:
            false_expr = self.curr_tok[self.VALUE]
            self.curr_tok = self.lex.__next__()
            return ast.FalseExpression(false_expr)

        # Or match a left opening parenthesis
        elif self.curr_tok[self.CODE] == tokens.SINGLE_TOKENS[tokens.LPAREN][0]:
            self.curr_tok = self.lex.__next__()
            # at this point there is an expression in self.curr_tok
            syntax_tree = self.expression()

            if self.curr_tok[self.CODE] == tokens.SINGLE_TOKENS[tokens.RPAREN][0]:
                self.curr_tok = self.lex.__next__()
                return syntax_tree
            else:
                raise errors.CliteSyntaxError("Missing right parenthesis!",
                                              self.curr_tok[self.LINE])
        # Or raise a CliteSyntaxError
        else:
            raise errors.CliteSyntaxError("Unexpected symbol {0}!".format(self.curr_tok[self.VALUE]),
                                          self.curr_tok[self.LINE])