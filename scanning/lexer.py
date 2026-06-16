#lexer.py 
#===========================================================================================
#Goes through each character one by one , and emits the corresponding tokens.
#
#This is the first stage of the interpreter.
#===========================================================================================
import typing as t 
from tokens import Token, TokenType, keywords, ALPHABETS, NUMBERS, SYMBOLS


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
                    self.col += 1 
                
                #---Newlines-----------------------------
                case "\n":
                    self.advance()
                    self.line += 1
                    self.col = 1
                
                #========================================================
                #---Multi-Char Tokens------------------------------------
                #========================================================
                
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

                #   / and comments
                case "/":
                    if self.peek() == '/':
                        while self.current_char() and self.current_char() != '\n':
                            self.advance()
                    else:
                        self.add(TokenType.SLASH,'/',self.line,self.col)
                        self.advance()
                
                #========================================================
                #---Single Character Tokens------------------------------
                #========================================================
                case "+":
                    self.add(TokenType.PLUS,'+',self.line,self.col)
                    self.advance()
                
                case "-":
                    self.add(TokenType.MINUS,'-',self.line,self.col)
                    self.advance()
                
                case '(':
                    self.add(TokenType.LPAREN,'(',self.line,self.col)
                    self.advance()
                
                case ')':
                    self.add(TokenType.RPAREN,')',self.line,self.col)
                    self.advance()

                case '[':
                    self.add(TokenType.LBRACKET,'[',self.line,self.col)
                    self.advance()
                
                case ']':
                    self.add(TokenType.RBRACKET,']',self.line,self.col)
                    self.advance()

                case '{':
                    self.add(TokenType.LBRACE,'{',self.line,self.col)
                    self.advance()

                case '}':
                    self.add(TokenType.RBRACE,'}',self.line,self.col)
                    self.advance()

                
                #========================================================
                #---Reading Words & Numbers----------------
                #========================================================
                
                #---Keywords & Idents-----------------------------
                case c if c in ALPHABETS:
                    result = []
                    result.append(c)
                    self.advance()

                    while self.current_char() is not None and self.current_char() in ALPHABETS:
                        result.append(self.current_char())
                        self.advance()
                    
                    text = "".join(result)

                    if text in keywords:
                        self.add(TokenType.KEYWORD,text,self.line,self.col)
                    
                    elif text in ("True","False"):
                        self.add(TokenType.BOOLEAN,text,self.line,self.col)
                    
                    else:
                        self.add(TokenType.IDENTIFIER,text,self.line,self.col)
                
                #---Numbers-----------------------------------------------
                case c if c in NUMBERS:
                    result = []
                    result.append(c)
                    self.advance()

                    while self.current_char() is not None and self.current_char() in NUMBERS:
                        result.append(self.current_char())
                        self.advance()
                    
                    text = "".join(result)

                    if text.count(".") == 1:
                        if text.startswith("."):
                            decimal = "0"
                            decimal += text
                            self.add(TokenType.FLOAT,decimal,self.line,self.col)
                        elif text.endswith("."):
                            decimal = "0"
                            decimal += text
                            self.add(TokenType.FLOAT,decimal,self.line,self.col)
                        
                        else:
                            self.add(TokenType.FLOAT,text,self.line,self.col)

                    elif text.count(".") == 0:
                        self.add(TokenType.INTEGER,text,self.line,self.col)
                    else:
                        raise Exception("Invalid number lmao")
                
                #---Strings----------------------------
                case c if c in ('"',"'"):
                    c = c 
                    self.advance()

                    string = ''

                    while self.current_char() is not None and self.current_char() != c:
                        string += self.current_char()
                        self.advance()
                    
                    self.advance()
                    self.add(TokenType.STRING,string,self.line,self.col) 

        self.add(TokenType.EOF,'',self.line,self.col)
        return self.tokens

