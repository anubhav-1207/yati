from colorama import Fore, init 
from scanning.lexer import Lexer
from scanning.tokens import *

init(autoreset=True)

def test_simple_assignment():
    code = "const x = 5"
    lexer = Lexer(code)
    tokens = lexer.tokenise()

    try:
        assert len(tokens) == 5
        assert tokens[0].token_type == TokenType.KEYWORD
        assert tokens[1].token_type == TokenType.IDENTIFIER
        assert tokens[2].token_type == TokenType.EQ
        assert tokens[3].token_type == TokenType.INTEGER
        assert tokens[4].token_type == TokenType.EOF
        print(Fore.YELLOW+"[+] " + Fore.GREEN + "Test Case 1 - Passed")
    
    except Exception as e:
        print(Fore.YELLOW + "[!] " + Fore.RED + "Test Case 1 - Failed")


test_simple_assignment()