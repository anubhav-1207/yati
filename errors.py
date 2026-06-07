class LexerError(Exception):
    def __init__(self,line: int,col: int,message: str):
        super().__init__(f"Lexer error")