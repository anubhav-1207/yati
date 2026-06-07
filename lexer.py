#lexer.py 
#===========================================================================================
#Goes through each character one by one , and emits the corresponding tokens.
#
#This is the first stage of the interpreter.
#===========================================================================================
import typing as t 
from tokens import Token, TokenType, keywords


#---Lexer Class-----------------------------------------------------------------------------
class Lexer:
    def __init__(self,source):
        self.source = source 
        self.pos = 0 # Initialising the pointer.
        self.col = 1
        self.line = 1
        tokens = []        

    def current_char(self):
        """Returns the current character pointer is at."""
        if self.pos < len(self.source):
            return self.source[self.pos]
        else:
            return None

    def advance(self):
        """Consume the current character and move one step forward"""
        char = self.source[self.pos]
        self.pos += 1 
        if self.pos < len(self.source):
            return char
        else:
            return None
    
    def peek(self):
        """Returns the next value without consuming it."""
        if (self.pos + 1) < len(self.source):
            return self.source[self.pos+1]
        else:
            return None

    def add(self):
        """Creates a "Token" object"""
        def __init__(self,token_type: TokenType,lexeme: str,line: int,col: int):
            self.tokens.append(Token(token_type, lexeme, line, col))
    
    def tokenise(self):
        while self.current_char() and self.current_char() is not None:
            char = self.current_char()

            match char:
                case "":
                    self.advance()
                    print(char)
    