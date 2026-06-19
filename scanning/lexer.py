#lexer.py 
#===========================================================================================
#Goes through each character one by one , and emits the corresponding tokens.
#
#This is the first stage of the interpreter.
#===========================================================================================
import typing as t 
from .tokens import Token, TokenType, keywords, ALPHABETS, NUMBERS, SYMBOLS


#---Lexer Class-----------------------------------------------------------------------------
class Lexer:
    def __init__(self,source):
        self.source = source 
        self.pos = 0 # Initialising the pointer.
        self.col = 1
        self.line = 1
        self.tokens = []        


    #---Helper Methods----------------------------------------------------------------------
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
        self.col += 1 
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
    


    
    #---Tokenising Method---------------------------------------------------------------------
    def tokenise(self):
        """Visits the characters and matches patterns."""
        while self.current_char() and self.current_char() is not None:
            char = self.current_char()

            match char:
                #---Spaces-------------------------------
                case " ":
                    self.advance()
                
                #---Newlines-----------------------------
                case "\n":
                    self.advance()
                    self.line += 1
                    self.col = 1
                
                #========================================================
                #---Multi-Char Tokens------------------------------------
                #========================================================
                
                #=============================!!!!!!!!!!!!!!!!!!======================================
                #self.col is stored in 'column' to append the starting column of the token 
                #=====================================================================================
                
                
                #   ** and *
                case "*":
                    column = self.col
                    if self.peek() == '*':
                        self.add(TokenType.STARSTAR, '**', self.line, column)
                        self.advance();self.advance()
                    else:
                        self.add(TokenType.STAR,'*',self.line, column)
                        self.advance()
                
                #   == and =
                case "=":
                    column = self.col
                    if self.peek() == '=':
                        self.add(TokenType.EQEQ,'==',self.line,column)
                        self.advance();self.advance()
                    else:
                        self.add(TokenType.EQ,'=',self.line,column)
                        self.advance()
                
                #   >= and >
                case ">":
                    column = self.col
                    if self.peek() == '=':
                        self.add(TokenType.GTE,'>=',self.line,column)
                        self.advance();self.advance()
                    else:
                        self.add(TokenType.GT,'>',self.line,column)
                        self.advance()

                #   <= and <
                case "<":
                    column = self.col
                    if self.peek() == '=':
                        self.add(TokenType.LTE,'<=',self.line,column)
                        self.advance();self.advance()
                    else:
                        self.add(TokenType.LT,'<',self.line,column)
                        self.advance()
                
                #   != and !
                case "!":
                    column = self.col
                    if self.peek() == '=':
                        self.add(TokenType.NEQ,'!=',self.line,column)
                        self.advance();self.advance()
                    else:
                        self.add(TokenType.NOT,'!',self.line,column)
                        self.advance()

                #   / and comments
                case "/":
                    column = self.col
                    if self.peek() == '/':
                        while self.current_char() and self.current_char() != '\n':
                            self.advance()
                    else:
                        self.add(TokenType.SLASH,'/',self.line,column)
                        self.advance()
                
                #========================================================
                #---Single Character Tokens------------------------------
                #========================================================
                case "+":
                    column = self.col
                    self.add(TokenType.PLUS,'+',self.line,column)
                    self.advance()
                
                case "-":
                    column = self.col
                    self.add(TokenType.MINUS,'-',self.line,column)
                    self.advance()
                
                case '(':
                    column = self.col
                    self.add(TokenType.LPAREN,'(',self.line,column)
                    self.advance()
                
                case ')':
                    column = self.col
                    self.add(TokenType.RPAREN,')',self.line,column)
                    self.advance()

                case '[':
                    column = self.col
                    self.add(TokenType.LBRACKET,'[',self.line,column)
                    self.advance()
                
                case ']':
                    column = self.col
                    self.add(TokenType.RBRACKET,']',self.line,column)
                    self.advance()

                case '{':
                    column = self.col
                    self.add(TokenType.LBRACE,'{',self.line,column)
                    self.advance()

                case '}':
                    column = self.col
                    self.add(TokenType.RBRACE,'}',self.line,column)
                    self.advance()

                
                #========================================================
                #---Reading Words & Numbers----------------------
                #========================================================
                
                #---Keywords & Idents-----------------------------
                case c if c in ALPHABETS:
                    
                    column = self.col
                    result = []
                    
                    # consume first letter
                    result.append(c)
                    self.advance()

                    while self.current_char() is not None and self.current_char() in ALPHABETS:
                        result.append(self.current_char())
                        self.advance()
                    
                    # array -> string
                    text = "".join(result)

                    if text in keywords:
                        self.add(TokenType.KEYWORD,text,self.line,column)
                    
                    # Boolean Operators
                    elif text in ("True","False"):
                        self.add(TokenType.BOOLEAN,text,self.line,column)
                    
                    else:
                        self.add(TokenType.IDENTIFIER,text,self.line,column)
                
                #---Numbers-----------------------------------------------
                case c if c in NUMBERS:
                    column = self.col
                    result = []
                    
                    # consume first letter
                    result.append(c)
                    self.advance()

                    while self.current_char() is not None and self.current_char() in NUMBERS:
                        result.append(self.current_char())
                        self.advance()
                    
                    # array -> string
                    text = "".join(result)


                    if text.count(".") == 1:
                        # To make .123 -> 0.123
                        if text.startswith("."):
                            decimal = "0"
                            decimal += text
                            self.add(TokenType.FLOAT,decimal,self.line,column)
                        
                        # To make 123. -> 123.0
                        elif text.endswith("."):
                            decimal = "0"
                            decimal += text
                            self.add(TokenType.FLOAT,decimal,self.line,column)
                        
                        else:
                            self.add(TokenType.FLOAT,text,self.line,column)

                    elif text.count(".") == 0:
                        self.add(TokenType.INTEGER,text,self.line,column)
                    else:
                        raise Exception("Invalid number lmao")
                
                #---Strings----------------------------
                case c if c in ('"',"'"):
                    
                    # skip the ' or "
                    self.advance()
                    column = self.col

                    string = ''

                    while self.current_char() is not None and self.current_char() != c:
                        string += self.current_char()
                        self.advance()
                    
                    self.advance()
                    self.add(TokenType.STRING,string,self.line,column) 

        # Adding an EOF token to signify END OF FILE
        self.add(TokenType.EOF,'',self.line,self.col)
        return self.tokens