# tokens.py 
#=========================================================
# Design Philosophy:
#   - clean code 
#   - avoid unnecessary shortcuts
#   - use comments
#   - use docstrings
#=========================================================

import typing as t 
from enum import Enum, auto 

#---------------------------------------------------------
class TokenType(Enum):
    #---Literals-----------------------------
    INTEGER = auto()
    FLOAT = auto()
    BOOLEAN = auto()
    STRING = auto()
    NULL = auto()
    IDENTIFIER = auto()
    KEYWORD = auto()
    
    #---One Character Tokens-----------------
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    DOT = auto()
    COMMA = auto()
    COLON = auto()
    SEMI_COLON = auto()
    EQ = auto()
    GT = auto()
    LT = auto()
    BANG = auto()

    #---Multi Character Tokens---------------
    EQEQ = auto()
    NEQ = auto()
    STARSTAR = auto()
    GTE = auto()
    LTE = auto()
    BANGEQ = auto()

    #---OPERATORS----------------------------
    AND = auto()
    OR = auto()
    NOT = auto()

    EOF = auto()


#---------------------------------------------------------
keywords = (
    'str','int','bool','float',
    'stdout','stdin',
    'while','for',
    'if','else','elif',
    'break','return'
)

#---------------------------------------------------------
class Token:
    def __init__(self, token_type: TokenType, lexeme: str,line: int,col: int):
        self.token_type = token_type
        self.lexeme = lexeme
        self.line = line 
        self.col = col 
    
    def __repr__(self):
        return f"TOKEN({self.token_type}, {self.lexeme}, {self.line}:{self.col})"
#---------------------------------------------------------