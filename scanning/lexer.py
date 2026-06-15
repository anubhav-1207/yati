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
        self.tokens = []        

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

    def add(self, token_type: TokenType, lexeme: t.Any, line: int, col: int):
        """Creates a "Token" object"""
        self.tokens.append(Token(token_type, lexeme, line, col))
    
    def tokenise(self):
        """Visits the characters and matches patterns."""
        while self.current_char() and self.current_char() is not None:
            char = self.current_char()

            match char:
                #---Spaces-------------------------------
                case " ":
                    self.advance()
                    self.col += 1 
                
                #---Newlines-----------------------------
                case "\n":
                    self.advance()
                    self.line += 1
                
                #---Multi-Char Tokens---------------------
                #   ** and *
                case "*":
                    if self.peek() == '*':
                        self.add(TokenType.STARSTAR, '**', self.line, self.col)
                        self.advance();self.advance()
                    else:
                        self.add(TokenType.STAR,'*',self.line, self.col)
                        self.advance()
                
                #   == and =
                case "=":
                    if self.peek() == '=':
                        self.add(TokenType.EQEQ,'==',self.line,self.col)
                        self.advance();self.advance()
                    else:
                        self.add(TokenType.EQ,'=',self.line,self.col)
                        self.advance()
                
                #   >= and >
                case ">":
                    if self.peek() == '=':
                        self.add(TokenType.GTE,'>=',self.line,self.col)
                        self.advance();self.advance()
                    else:
                        self.add(TokenType.GT,'>',self.line,self.col)
                        self.advance()

                #   <= and <
                case "<":
                    if self.peek() == '=':
                        self.add(TokenType.LTE,'<=',self.line,self.col)
                        self.advance();self.advance()
                    else:
                        self.add(TokenType.LT,'<',self.line,self.col)
                        self.advance()
                
                #   != and !
                case "!":
                    if self.peek() == '=':
                        self.add(TokenType.NEQ,'!=',self.line,self.col)
                        self.advance();self.advance()
                    else:
                        self.add(TokenType.NOT,'!',self.line,self.col)
                        self.advance()

                #   ! and comments
                case "/":
                    if self.peek() == '/':
                        while self.current_char() and self.current_char() != '\n':
                            self.advance()
                    else:
                        self.add(TokenType.SLASH,'/',self.line,self.col)
                        self.advance()
                        

        
        
        
        
        
        
        
        self.add(TokenType.EOF,'',self.line,self.col)
        return self.tokens

lexer = Lexer("""
! !=
//ignore this
""")
print(lexer.tokenise())