from ply import lex

# ------------------
# ANALIZADOR LÉXICO|
# ------------------
# El analizador léxico recibe el código fuente y lo descompone en tokens definidos (términos 
# significativos como palabras clave, reservadas, identificadores, operadores, etc.). 

# Definición de tokens
tokens = (
    # Palabras reservadas
    'PRINCIPAL', 'INCLUIR', 'BIBLIOTECA', 'TAMANIO_DE',
    
    # Estructuras de control y funciones
    'SI', 'PARA', 'RETORNAR',
    
    # Tipos de datos
    'ENTERO', 'VACIO',
    
    # Identificadores y valores
    'IDENTIFICADOR', 'NUMERO', 'CADENA',
    
    # Operadores aritméticos
    'SUMA', 'RESTA', 'PRODUCTO', 'DIVISION', 
    
    # Operadores de asignación y condicionales
    'ASIGNACION', 'MENOR_QUE', 'MAYOR_QUE', 
    
    # Incremento
    'INCREMENTO', 
    
    # Aperturas y cierres de estructuras de control y funciones
    'LLAVE_IZQ', 'LLAVE_DER', 'PARENTESIS_IZQ', 'PARENTESIS_DER','CORCHETE_IZQ', 'CORCHETE_DER',
    
    # Operadores de entrada/salida
    'IMPRIMIR',  
    
    # Puntuación
    'PUNTO_Y_COMA', 'COMA'
)

# Expresiones regulares para tokens simples
t_SUMA = r'\+'
t_RESTA = r'-'
t_PRODUCTO = r'\*'
t_DIVISION = r'/'

t_ASIGNACION = r'='
t_MENOR_QUE = r'<'
t_MAYOR_QUE = r'>'

t_PARENTESIS_IZQ = r'\('
t_PARENTESIS_DER = r'\)'
t_LLAVE_IZQ = r'\{'
t_LLAVE_DER = r'\}'
t_CORCHETE_IZQ = r'\['
t_CORCHETE_DER = r'\]'

t_PUNTO_Y_COMA = r';'
t_COMA = r','

t_INCREMENTO = r'\+\+'

# Expresiones regulares para tokens más complejos
def t_NUMERO(t):
    r'\d+(\.\d+)?'
    return t

def t_CADENA(t):
    r'\"(\\.|[^\\"])*\"'
    return t

def t_BIBLIOTECA(t):
    r'<[a-zA-Z_][a-zA-Z0-9_]*\.h>'
    return t

def t_INCLUIR(t):
    r'\#include'
    return t

# Palabras reservadas
reservadas = {
    'main': 'PRINCIPAL', 'sizeof': 'TAMANIO_DE',
    'if': 'SI', 'for': 'PARA',
    'return': 'RETORNAR', 
    'void': 'VACIO', 'int': 'ENTERO',
    'printf': 'IMPRIMIR',
}

# Identificadores y palabras reservadas
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value, 'IDENTIFICADOR')
    return t

# Manejo de saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Manejo de errores
def t_error(t):
    print(f"Carácter ilegal: '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)

# Construcción del lexer
lexer = lex.lex()

# Función para probar el analizador léxico
def test_analizador_lexico(codigo):
    try:
        lexer.input(codigo)
        print(f"\nEl resultado del análisis léxico es:\n")
        for token in lexer:
            print(f'Token: {token.type}, Valor: {token.value}, Línea: {token.lineno}')
    except Exception as e:
        print(f"Error durante el análisis léxico: {e}")
        
# Código de prueba en C
codigo_a_analizar = '''
#include <stdio.h>

void bubble_sort(int arr[], int n) {
    int temp = 0;
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

int main() {
    int arr[] = {5, 3, 4, 8, 7, 5, 1, 2, 3};
    int n = sizeof(arr) / sizeof(arr[0]);

    bubble_sort(arr, n);

    printf("Arreglo ordenado: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }

    return 0;
}
'''

# Ejecutar el lexer con el código de prueba
test_analizador_lexico(codigo_a_analizar)