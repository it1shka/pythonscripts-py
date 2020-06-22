from re import match

################# LEXER #################

class Lexer:
    def __init__(self, code):
        self.code = code
        self.pos = -1
        self.char = None
    def get_tokens(self):
        tokens = []
        while self.move():
            c = self.char
            if c in (' ', '\n', '\t'):
                pass
            elif c in ('(', ')'):
                tokens.append((c, ''))
            elif c == "'":
                tokens.append(('string', self.make_string()))
            elif match('[.0-9]', c):
                tokens.append(('number', self.make_number()))
            elif match('[_a-zA-Z]', c):
                tokens.append(('id', self.make_id()))
            else:
                raise Exception('Syntax Error: {}'.format(c))
        return tokens
    def move(self):
        self.pos += 1
        if self.pos >= len(self.code):
            return False
        self.char = self.code[self.pos]
        return True
    def make_string(self):
        string = ''
        while self.move() and self.char != "'":
            string += self.char
        return string
    def make_number(self):
        dots = int(self.char == '.')
        num = self.char
        while self.move() and match('[.0-9]',self.char):
            if self.char == '.':
                dots += 1
                if dots > 1:
                    raise Exception('Two dots in one number')
            num+=self.char
        self.pos -= 1
        if dots == 0:
            return int(num)
        else:
            return float(num)
    def make_id(self):
        newid = self.char
        while self.move() and match('[_a-zA-Z]', self.char):
            newid += self.char
        self.pos -= 1
        return newid

################# PARSER #################

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = -1
        self.token = None
    def make_function(self):
        if not self.move():
            raise Exception('Function must be ended with ")" ')
        if self.token[0] != 'id':
            raise Exception('Function must have an id')
        func_id = self.token[1]
        func_args = []
        while True:
            if not self.move():
                raise Exception('Function must be ended with ")" ')
            if self.token[0] == ')':
                break
            if self.token[0] in ('string', 'number', 'id'):
                func_args.append(self.token)
            elif self.token[0] == '(':
                func_args.append(self.make_function())
        return (func_id, func_args)

    def get_ast(self):
        if not self.move():
            return None
        if self.token[0] != '(':
            raise Exception('Function call must start from "(" not {} '.format(self.token))
        if self.tokens[self.pos + 1][1] != 'main':
            raise Exception('Script must be inside of "main" function')
        ast = self.make_function()
        if self.move():
            raise Exception('There is something outside "main" function at the end of your script')
        return ast
    def move(self):
        self.pos += 1
        if self.pos >= len(self.tokens):
            return False
        self.token = self.tokens[self.pos]
        return True

################# EXECUTOR #################

def run(function):
    if function[0] not in functions.keys():
        raise Exception('There is no function named {}'.format(function[0]))

    #return functions[function[0]](function[1])

    func_name, args_count = functions[function[0]]
    if args_count != None:
        if args_count != len(function[1]):
            raise Exception('Wrong amount of args in function {}'.format(function[0]))
    return func_name(function[1])

def get_var(name):
    if name not in variables.keys():
        raise Exception('There is no variable named {}'.format(tvalue))
    return variables[name]

def run_args(args):
    new_args = []
    for each in args:
        ttype, tvalue = each
        if ttype in ('string', 'number'):
            new_args.append(each)
        elif ttype == 'id':
            new_args.append(get_var(tvalue))
        else:
            new_args.append(run(each))
    return new_args
            

def main(funcs):
    for each in funcs:
        run(each)

def write(args):
    args = run_args(args)
    for each in args:
        print(each[1], end='')

def endl(args):
    print()

def add(args):
    args = run_args(args)
    ans = 0
    return_type = 'number'
    for each in args:
        ttype, tvalue = each
        if ttype == 'number' and return_type == 'number':
            ans += tvalue
        else:
            if ttype == 'string' and return_type =='number':
                ans = str(ans)
                return_type = 'string'
                ans += tvalue
            else:
                ans += tvalue
    return (return_type, ans)


class Executor:
    def __init__(self, ast):
        self.ast = ast
    def execute(self):
        if ast == None:
            return
        run(ast)

variables = {}

functions = {
    'main' : (main, None),

    'write' : (write, None),
    'endl' : (endl, 0),
    'add' : (add, None)
}

################# TOOLS #################

while True:
    string_input = input('\n>>>')
    try:
        lexer = Lexer(string_input)
        tokens = lexer.get_tokens()
        parser = Parser(tokens)
        ast = parser.get_ast()
        executor = Executor(ast)
        executor.execute()
    except Exception as e:
        print(str(e))