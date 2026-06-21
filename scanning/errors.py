class InvalidTokenError(Exception):
    def __init__(self,line: int,col: int, token):
        super().__init__(f"type fatal :: The passed token '{token}' is malformed and not recognized by the lexer\n\t\t\t\t---> line:col {line}:{col}")

class UnterminatedStringLiteral(Exception):
    def __init__(self,line,col):
        super().__init__(f"type nonfatal :: Malformed string literal encountered by lexer\n\t\t\t\t---> line:col {line}:{col}")