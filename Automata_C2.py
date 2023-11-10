import tkinter as tk
from tkinter import ttk, messagebox
import ply.lex as lex
import ply.yacc as yacc

# Define reserved words
reserved = {
    'int': 'INT',
    'case': 'CASE',
    'switch': 'SWITCH',
    'if': 'IF',
    'return': 'RETURN',
   'string': 'STRING',
    'texto': 'TEXT',
    'else': 'ELSE',
    'funt': 'FUNT',
    'opcion': 'OPCION',
    'break': 'BREAK',
    'for': 'FOR'
}

tokens = [
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'SUM',
    'REST',
    'DIV',
    'MUL',
    'SEMI',
    'NUMBER',
    'ASSIGN',
    'ID',
    'GT',
    'LT',
    'DOUBLEPOT',
    'DOUBLESTRING'
] + list(reserved.values())

t_GT = r'>'
t_SUM = r'\+'
t_REST = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_LT = r'<'
t_DOUBLESTRING = r'"[^"]*"'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMI = r';'
t_ASSIGN = r'='
t_DOUBLEPOT = r':'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t\n'

def t_error(t):
    error_table.insert('', 'end', values=(f"Illegal character '{t.value[0]}'",))
    t.lexer.skip(1)

lexer = lex.lex()

def p_init(p):
    '''init : funcion
            | declarations
            | ciclo
            | selectivo
            | if'''
#condicional
def p_if(p):
    '''if : IF LPAREN condition RPAREN LBRACE TEXT RBRACE
                | IF LPAREN condition RPAREN LBRACE TEXT RBRACE ELSE LPAREN condition RPAREN LBRACE TEXT RBRACE'''
    
def p_condition(p):
    '''condition : expression LT NUMBER
                 | expression GT NUMBER
                 | expression GT ASSIGN NUMBER
                 | expression LT ASSIGN NUMBER'''
                 
def p_expression(p):
    '''expression : ID
                  | NUMBER'''

#variable               
def p_declarations(p):
    '''declarations : INT ID DOUBLEPOT NUMBER
                    | INT ID'''

#funcion 
def p_funcion(p):
    '''funcion : FUNT ID LPAREN ID RPAREN LBRACE TEXT RETURN rtr  RBRACE'''
    
def p_rtr(p):
    '''rtr : LPAREN ID RPAREN
                 | expression GT expression
                 | expression GT expression GT expression'''
                 
#selectivo              
def p_selectivo(p):
    '''selectivo : SWITCH LPAREN OPCION RPAREN LBRACE option RBRACE
                 | SWITCH LPAREN OPCION RPAREN LBRACE option option RBRACE'''
    
def p_option(p):
    '''option : CASE NUMBER DOUBLEPOT TEXT BREAK SEMI'''
    
#Ciclo
def p_ciclo(p):
    '''ciclo : FOR LPAREN INT ID ASSIGN NUMBER SEMI ID GT NUMBER SEMI ID SUM NUMBER RPAREN LBRACE TEXT RBRACE
             | FOR LPAREN INT ID ASSIGN NUMBER SEMI ID GT NUMBER SEMI ID REST NUMBER RPAREN LBRACE TEXT RBRACE
             | FOR LPAREN INT ID ASSIGN NUMBER SEMI ID GT NUMBER SEMI ID MUL NUMBER RPAREN LBRACE TEXT RBRACE
             | FOR LPAREN INT ID ASSIGN NUMBER SEMI ID GT NUMBER SEMI ID DIV NUMBER RPAREN LBRACE TEXT RBRACE'''
                  
def p_error(p):
    if p:
        error_table.insert('', 'end', values=(f"Error de sintaxis en token '{p.value}'",))
    else:
        error_table.insert('', 'end', values=("Error de sintaxis en EOF",))

parser = yacc.yacc()

symbol_table = set()

def check_code():
    for i in token_table.get_children():
        token_table.delete(i)
    for i in error_table.get_children():
        error_table.delete(i)

    code = txt.get("1.0", tk.END).strip()
    if not code:
        messagebox.showinfo('Resultado', 'No hay código para verificar.')
        return

    symbol_table.clear()

    lexer.input(code)

    for token in lexer:
        if token.type == 'DOUBLESTRING':
            value = token.value[1:-1]
        else:
            value = token.value
        token_table.insert('', 'end', values=(token.type, value))

    result = parser.parse(code, lexer=lexer)

    if not error_table.get_children():
        messagebox.showinfo('Resultado', 'La sintaxis y el análisis semántico son correctos.')
    else:
        messagebox.showerror('Resultado', 'Se encontraron errores de sintaxis o análisis semántico.')

root = tk.Tk()
root.title("Analizador Léxico, Sintáctico y Semántico")
root.configure(bg='green')  # Fondo verde para la ventana principal

codigo = '''for (int hijo = 8; hijo >7; hijo + 1) { texto}'''
txt = tk.Text(root, width=25, height=10)
txt.pack(side='left', padx=10, pady=10)
txt.insert(tk.END, codigo)

btn = tk.Button(root, text="analizar", command=check_code)
btn.pack(side='left', padx=10)

token_frame = tk.Frame(root, bg='green')  # Fondo verde para el frame de token_table
token_frame.pack(side='left', padx=10, pady=10)

token_table = ttk.Treeview(token_frame, columns=('Type', 'Value'), show='headings')
token_table.heading('Type', text='tokens')
token_table.heading('Value', text='valor')
token_table.pack()

error_frame = tk.Frame(root, bg='green')  # Fondo verde para el frame de error_table
error_frame.pack(side='left', padx=10, pady=10)

error_table = ttk.Treeview(error_frame, columns=('Error',), show='headings')
error_table.heading('Error', text='lexico y semantico')
error_table.column('Error', width=200)  
error_table.pack()

root.mainloop()
