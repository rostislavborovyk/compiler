from typing import List, Type

from my_parser.AST import AST, StringAST, DecimalAST, BinOpAST, UnOpAST, AssignExpAST, StatementsListAST, IdAST, \
    CondExpAST
from exceptions.my_exceptions import InvalidSyntaxException, EOF
from lexer.my_token import Token


class Parser:
    """
    func_expr: DEF WORD L_BRACKET R_BRACKET COLON SLASH_N statement_list
    statement_list: statement | statement SLASH_N SLASH_T* statement_list
    statement: assignment_statement | RETURN top_level_exp | conditional_statement
    assignment_statement: ID ("=" | "*=") top_level_exp
    conditional_statement:
    IF top_level_exp COLON SLASH_N statement_list SLASH_T* ELSE COLON SLASH_N statement_list

    ========================== arithmetical expressions ===========================
    top_level_exp: exp_or
    exp_or: exp (OR exp)* | exp
    exp: term ((MINUS | PLUS) term)* | term
    term: factor ((DIV | MUL) factor)* | factor
    factor: L_BRACKET top_level_exp R_BRACKET | unary_op | number | STRING | ID
    number: DECIMAL | BINARY
    unary_op: MINUS factor
    """

    def __init__(self, tokens_list):
        self.tokens_list: List[Token] = tokens_list
        self.pos = 0
        # set current token to the first token taken from the input
        self.current_token = self.tokens_list[self.pos]

    def parse(self) -> Type[AST]:
        return self._program()

    def _program(self) -> Type[AST]:
        nesting = 0

        node = self._func_expr(nesting)

        # self._set_next_token()
        while self.current_token != EOF and self.current_token.tok_type == Token.SLASH_N:
            while self.current_token != EOF and self.current_token.tok_type == Token.SLASH_T:
                self._check(Token.SLASH_T)
            self._check(Token.SLASH_N)
        # if self.current_token != EOF:
        #     raise InvalidSyntaxException("To much tokens for main function")

        return node

    def _func_expr(self, nesting: int) -> Type[AST]:
        """
        main_func_expr: DEF WORD L_BRACKET R_BRACKET COLON SLASH_N statement_list
        """
        self._check_indent(nesting)
        self._check(Token.BUILTIN_WORD, Token.BUILTIN_WORDS["DEF"])
        self._check(Token.ID)
        self._check(Token.L_BRACKET)
        self._check(Token.R_BRACKET)
        self._check(Token.COLON)
        self._check(Token.SLASH_N)
        # self._check(Token.SLASH_T)

        node = self._statement_list(nesting + 1)

        return node

    def _statement_list(self, nesting: int) -> Type[AST]:
        """
        statement_list: statement | statement SLASH_N SLASH_T* statement_list
        """

        self._check_indent(nesting)
        statements = [self._statement(nesting)]
        if not self._checkEOF():
            while self._is_specific_token(Token.SLASH_T):
                self._check(Token.SLASH_T)
            if self._is_specific_token(Token.SLASH_N):
                self._check(Token.SLASH_N)

        # todo set here check end of block
        if self._end_of_block(nesting):
            return StatementsListAST(statements)

        while not self._checkEOF():
            # handle new line
            # if self.current_token.tok_type == Token.SLASH_N:
            while self._is_specific_token(Token.SLASH_N):
                while self._is_specific_token(Token.SLASH_T):
                    self._check(Token.SLASH_T)
                self._check(Token.SLASH_N)
            if self._checkEOF():
                break
            self._check_indent(nesting)
            if self._checkEOF():
                break
            if self._is_statement():
                statements.append(self._statement(nesting))
                if self._end_of_block(nesting):
                    if self._is_specific_token(Token.SLASH_N):
                        self._check(Token.SLASH_N)
                    break
        return StatementsListAST(statements)

    def _statement(self, nesting: int) -> Type[AST]:
        """
        statement: assignment_statement | RETURN top_level_exp | conditional_statement
        """
        node = None
        if self._is_specific_token(Token.BUILTIN_WORD, Token.BUILTIN_WORDS["RETURN"]):
            self._check(Token.BUILTIN_WORD, Token.BUILTIN_WORDS["RETURN"])
            node = self._top_level_exp()
        elif self._is_specific_token(Token.BUILTIN_WORD, Token.BUILTIN_WORDS["IF"]):
            node = self._conditional_statement(nesting)
        elif self._is_specific_token(Token.ID):  # todo set regexp to value to check var validity
            node = self._assignment_statement()

        if node is None:
            raise InvalidSyntaxException("Not matches with any statement")

        return node

    def _assignment_statement(self) -> Type[AST]:
        """
        assignment_statement: ID ("=" | "*=") top_level_exp
        """
        var_id = self.current_token
        self._check(Token.ID)

        if self._is_specific_token(Token.ASSIGN, Token.ASSIGNS["ASSIGN"]):
            self._check(Token.ASSIGN, Token.ASSIGNS["ASSIGN"])
            exp = self._top_level_exp()
        elif self._is_specific_token(Token.ASSIGN, Token.ASSIGNS["ASSIGN_MUL"]):
            token = self.current_token
            self._check(Token.ASSIGN, Token.ASSIGNS["ASSIGN_MUL"])
            exp = BinOpAST(IdAST(var_id.value), Token("*", Token.OPERATION), self._top_level_exp())
        else:
            raise InvalidSyntaxException("Wrong token in factor expression")

        return AssignExpAST(var_id, exp)

    def _conditional_statement(self, nesting: int) -> Type[AST]:
        """
        conditional_statement:
        IF top_level_exp COLON SLASH_N statement_list SLASH_T* ELSE COLON SLASH_N statement_list
        """
        self._check(Token.BUILTIN_WORD, Token.BUILTIN_WORDS["IF"])
        cond_exp = self._top_level_exp()
        self._check(Token.COLON)
        self._check(Token.SLASH_N)
        node_if = self._statement_list(nesting + 1)
        self._check_indent(nesting)
        self._check(Token.BUILTIN_WORD, Token.BUILTIN_WORDS["ELSE"])
        self._check(Token.COLON)
        self._check(Token.SLASH_N)
        node_else = self._statement_list(nesting + 1)

        return CondExpAST(cond_exp, node_if, node_else)

    def _top_level_exp(self) -> Type[AST]:
        return self._exp_or()

    def _exp_or(self) -> Type[AST]:
        """
        exp_or: exp (OR exp)* | exp
        """

        if self.current_token == EOF:
            raise InvalidSyntaxException("End of file")

        node = None

        node = self._expression()
        token = self.current_token
        while self.current_token != EOF \
                and self.current_token.tok_type == Token.OPERATION \
                and self.current_token.value in (Token.OPERATIONS["OR"],):
            if token.value == Token.OPERATIONS["OR"]:
                self._check(Token.OPERATION, Token.OPERATIONS["OR"])

            node = BinOpAST(node, token, self._expression())
            token = self.current_token

        if node is None:
            raise InvalidSyntaxException(
                f"Wrong token {self.current_token.value} "
                f"in row={self.current_token.pos[0]}, pos={self.current_token.pos[1]} "
                f"in exp_or"
            )

        return node

    def _expression(self) -> Type[AST]:
        """
        exp: term ((MINUS | PLUS) term)* | term
        """

        if self.current_token == EOF:
            raise InvalidSyntaxException("End of file")

        node = None

        node = self._term()
        token = self.current_token
        while self.current_token != EOF \
                and self.current_token.tok_type == Token.OPERATION \
                and self.current_token.value in (
                Token.OPERATIONS["MINUS"], Token.OPERATIONS["PLUS"]):
            if token.value == Token.OPERATIONS["MINUS"]:
                self._check(Token.OPERATION, Token.OPERATIONS["MINUS"])
            elif token.value == Token.OPERATIONS["PLUS"]:
                self._check(Token.OPERATION, Token.OPERATIONS["PLUS"])
            node = BinOpAST(node, token, self._term())
            token = self.current_token

        if node is None:
            raise InvalidSyntaxException(
                f"Wrong token {self.current_token.value} "
                f"in row={self.current_token.pos[0]}, pos={self.current_token.pos[1]} "
                f"in expression"
            )

        return node

    def _term(self) -> Type[AST]:
        """
        term: factor ((DIV | MUL) factor)* | factor
        """
        if self.current_token == EOF:
            raise InvalidSyntaxException("End of file")

        # node = None

        node = self._factor()
        token = self.current_token
        while self.current_token != EOF \
                and self.current_token.tok_type == Token.OPERATION \
                and self.current_token.value in (
                Token.OPERATIONS["DIV"], Token.OPERATIONS["MUL"]):
            if token.value == Token.OPERATIONS["DIV"]:
                self._check(Token.OPERATION, Token.OPERATIONS["DIV"])
            elif token.value == Token.OPERATIONS["MUL"]:
                self._check(Token.OPERATION, Token.OPERATIONS["MUL"])
            node = BinOpAST(node, token, self._factor())
            token = self.current_token

        if node is None:
            raise InvalidSyntaxException(
                f"Wrong token {self.current_token.value} "
                f"in row={self.current_token.pos[0]}, pos={self.current_token.pos[1]} "
                "in term expression"
            )

        return node

    def _factor(self) -> Type[AST]:
        """
        factor: L_BRACKET top_level_exp R_BRACKET | unary_op | number | STRING | ID
        """
        if self.current_token == EOF:
            raise InvalidSyntaxException("End of file")

        node = None

        token = self.current_token

        if token.tok_type == Token.L_BRACKET:
            self._check(Token.L_BRACKET)
            node = self._top_level_exp()
            self._check(Token.R_BRACKET)

        if token.tok_type == Token.OPERATION and token.value == Token.OPERATIONS["MINUS"]:
            self._check(Token.OPERATION, Token.OPERATIONS["MINUS"])
            node = UnOpAST(token, self._factor())

        elif token.tok_type == Token.NUMBER_DECIMAL:  # todo maybe handle binary num too
            self._check(Token.NUMBER_DECIMAL)
            node = DecimalAST(token)

        elif token.tok_type == Token.STRING:
            self._check(Token.STRING)
            node = StringAST(self.current_token)

        elif token.tok_type == Token.ID:
            self._check(Token.ID)
            node = IdAST(token.value)

        if node is None:
            raise InvalidSyntaxException("Wrong token in factor expression")

        return node

    def _set_next_token(self) -> None:
        self.pos += 1
        if self.pos < len(self.tokens_list):
            self.current_token = self.tokens_list[self.pos]
        else:
            self.current_token = EOF

    def _checkEOF(self):
        if self.current_token == EOF:
            return True
        return False

    def _check(self, tok_type, value=None) -> None:
        """
        Checks if cur_token of corresponding type, if so checks if value corresponds and sets the next token
        """
        if self.current_token == EOF:
            raise InvalidSyntaxException("End of file")
        elif not self._is_specific_token(tok_type, value):
            raise InvalidSyntaxException(
                    f"Token {self.current_token.value} "
                    f"in row={self.current_token.pos[0]}, pos={self.current_token.pos[1]} "
                    f"should not be here"
                )
        else:
            self._set_next_token()

    def _is_specific_token(self, tok_type, value=None) -> bool:
        if self.current_token == EOF:
            return False
        if self.current_token.tok_type == tok_type:
            if value is not None and self.current_token.value == value:
                return True
            elif value is not None and self.current_token.value != value:
                return False
            return True
        else:
            return False

    def _check_indent(self, nesting: int):
        for i in range(nesting):
            self._check(Token.SLASH_T)

    def _is_statement(self) -> bool:
        if self._is_specific_token(Token.BUILTIN_WORD, Token.BUILTIN_WORDS["RETURN"]) \
                or self._is_specific_token(Token.ID) \
                or self._is_specific_token(Token.BUILTIN_WORD, Token.BUILTIN_WORDS["IF"]):
            return True
        return False

    def _end_of_block(self, nesting):
        if self.current_token == EOF:
            return True
        pos = self.pos
        token = self.tokens_list[pos]
        # if token.tok_type != Token.SLASH_N:
        #     return True

        # pos += 1
        # token = self.tokens_list[pos]
        if token.tok_type == Token.SLASH_N:
            pos += 1
            token = self.tokens_list[pos]

        for i in range(nesting):
            if token.tok_type != Token.SLASH_T:
                return True
            pos += 1
            token = self.tokens_list[pos]
        return False

