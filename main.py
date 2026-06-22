from scanning import tokens, lexer
from scanning.lexer import Lexer

while True:
    shell_input = input(">>> ")
    shell_input = shell_input.strip().split()
    command = shell_input[0]
    
    match command:
        case "exec":
            filepath = shell_input[1]

            with open(filepath,'r') as file:
                code = file.read() 
                lexer_obj = Lexer(code)
                tokens = lexer_obj.tokenise()
                
                for tok in tokens:
                    print(tok)


