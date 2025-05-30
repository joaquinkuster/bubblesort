from ply import yacc
from analizador_lexico import tokens

# ----------------------
# ANALIZADOR SINTÁCTICO|
# ----------------------
# El analizador sintáctico toma los tokens generados por el léxico y verifica si siguen la estructura 
# gramatical definida por un lenguaje (C en este caso), organizándolos en una estructura jerárquica 
# o árbol de sintaxis. Los organiza y valida de acuerdo a las reglas gramaticas y de producción
# definidas del lenguaje.

# Precedencias para los operadores aritméticos
precedence = (
    ('left', 'SUMA', 'RESTA'),
    ('left', 'PRODUCTO', 'DIVISION'),
)

# Reglas de producción

# Programa inicial
def p_programa(p):
    '''
    programa : lista_declarativas lista_funciones
    '''
    p[0] = f"programa → {p[1]}\n{p[2]}"

# Declarativas
def p_lista_declarativas(p):
    '''
    lista_declarativas : declarativa 
                       | declarativa lista_declarativas
    '''
    if len(p) == 3:
        p[0] = f"lista_declarativas → {p[1]} {p[2]}"
    else:
        p[0] = f"lista_declarativas → {p[1]}"
        
def p_declarativa(p):
    '''
    declarativa : inclusion
    '''
    p[0] = f"declarativa → {p[1]}"
    
# Inclusión de biblioteca
def p_inclusion(p):
    '''
    inclusion : INCLUIR BIBLIOTECA
    '''
    p[0] = f"inclusion → {p[1]} {p[2]}"

# Funciones
def p_lista_funciones(p):
    '''
    lista_funciones : definicion_funcion 
                    | definicion_funcion lista_funciones
    '''
    if len(p) == 3:
        p[0] = f"lista_funciones → {p[1]} {p[2]}"
    else:
        p[0] = f"lista_funciones → {p[1]}"

# Definición de funciones 
def p_definicion_funcion(p):
    '''
    definicion_funcion : funcion_principal
                       | funcion_general
    '''
    p[0] = f'{p[1]}'
        
# Función principal
def p_funcion_principal(p):
    '''
    funcion_principal : ENTERO PRINCIPAL PARENTESIS_IZQ lista_parametros PARENTESIS_DER bloque
                      | ENTERO PRINCIPAL PARENTESIS_IZQ PARENTESIS_DER bloque
    '''
    if len(p) == 7:
        p[0] = f"inicio → {p[1]} {p[2]} ( {p[4]} ) {p[6]}"
    else:
        p[0] = f"inicio → {p[1]} {p[2]} ( ) {p[5]}"
        
# Funciones generales
def p_funcion_general(p):
    '''
    funcion_general : tipo IDENTIFICADOR PARENTESIS_IZQ lista_parametros PARENTESIS_DER bloque
                    | tipo IDENTIFICADOR PARENTESIS_IZQ PARENTESIS_DER bloque
    '''
    if len(p) == 7:
        p[0] = f"definicion_funcion → {p[1]} {p[2]} ( {p[4]} ) {p[6]}"
    elif len(p) == 6:
        p[0] = f"definicion_funcion → {p[1]} {p[2]} ( ) {p[5]}"

# Parámetros de la función
def p_lista_parametros(p):
    '''
    lista_parametros : parametro COMA lista_parametros
                     | parametro
                     | VACIO
    '''
    if len(p) == 4:
        p[0] = f"lista_parametros → {p[1]} , {p[3]}"
    else:
        p[0] = f"lista_parametros → {p[1]}"

def p_parametro(p):
    '''
    parametro : tipo IDENTIFICADOR
              | tipo IDENTIFICADOR CORCHETE_IZQ CORCHETE_DER
    '''
    if len(p) == 3:
        p[0] = f"parametro → {p[1]} {p[2]}"
    else:
        p[0] = f"parametro → {p[1]} {p[2]} [ ]"

# Bloques de código
def p_bloque(p):
    '''
    bloque : LLAVE_IZQ lista_instrucciones LLAVE_DER 
           | LLAVE_IZQ LLAVE_DER
    '''
    if len(p) == 4:
        p[0] = f"bloque → {{ {p[2]} }}"
    else:
        p[0] = "bloque → { }"

# Instrucciones
def p_lista_instrucciones(p):
    '''
    lista_instrucciones : instruccion 
                        | instruccion lista_instrucciones
    '''
    if len(p) == 3:
        p[0] = f"lista_instrucciones → {p[1]}\n{p[2]}"
    else:
        p[0] = f"lista_instrucciones → {p[1]}"

def p_instruccion(p):
    '''
    instruccion : declaracion
                | sentencia
                | estructura_de_control
    '''
    p[0] = f"instruccion → {p[1]}"

# Declaraciones
def p_declaracion(p):
    '''
    declaracion : declaracion_variable PUNTO_Y_COMA
    '''
    p[0] = f"declaracion → {p[1]} ;"

# Declaraciones de variables
def p_declaracion_variable(p):
    '''
    declaracion_variable : tipo lista_identificadores
    '''
    p[0] = f"declaracion_variable → {p[1]} {p[2]}"

def p_lista_identificadores(p):
    '''
    lista_identificadores : IDENTIFICADOR
                          | IDENTIFICADOR CORCHETE_IZQ CORCHETE_DER ASIGNACION elementos_array
                          | IDENTIFICADOR ASIGNACION expresion
                          | IDENTIFICADOR COMA lista_identificadores
                          | IDENTIFICADOR ASIGNACION expresion COMA lista_identificadores 
    '''
    if len(p) == 2:
        p[0] = f"lista_identificadores → {p[1]}"
    elif len(p) == 4:
        p[0] = f"lista_identificadores → {p[1]} {p[2]} {p[3]}"
    elif len(p) == 6:
        p[0] = f"lista_identificadores → {p[1]} {p[2]} {p[3]} {p[4]} {p[5]}"
        
# Elementos que conforman un array
def p_elementos_array(p):
    '''
    elementos_array : LLAVE_IZQ lista_valores LLAVE_DER
    '''
    p[0] = f"elementos_array → {p[1]} {p[2]} {p[3]}"
    
def p_lista_valores(p):
    '''
    lista_valores : NUMERO
                  | NUMERO COMA lista_valores
    '''
    if len(p) == 2:
        p[0] = f'lista_valores → {p[1]}'
    else:
        p[0] = f'lista_valores → {p[1]} , {p[3]}'

# Sentencias
def p_sentencia(p):
    '''
    sentencia : asignacion PUNTO_Y_COMA
              | llamado_a_funcion PUNTO_Y_COMA
              | retorno PUNTO_Y_COMA
    '''
    p[0] = f"sentencia → {p[1]} ;"

# Asignaciones
def p_asignacion(p):
    '''
    asignacion : IDENTIFICADOR ASIGNACION expresion
               | IDENTIFICADOR CORCHETE_IZQ expresion CORCHETE_DER ASIGNACION expresion
               | IDENTIFICADOR INCREMENTO
    '''
    if len(p) == 7:
        p[0] = f"asignacion → {p[1]} [ {p[3]} ] = {p[6]}"
    elif len(p) == 4:
        p[0] = f"asignacion → {p[1]} = {p[3]}"
    elif len(p) == 3:
        p[0] = f"asignacion → {p[1]} {p[2]}"

# Condiciones
def p_condicion(p):
    '''
    condicion : expresion MENOR_QUE expresion
              | expresion MAYOR_QUE expresion
    '''
    if len(p) == 4:
        p[0] = f"condicion → {p[1]} {p[2]} {p[3]}"

# Tipos de datos
def p_tipo(p):
    '''
    tipo : ENTERO
         | VACIO
    '''
    p[0] = f"tipo → {p[1]}"

# Expresiones y operaciones aritméticas
def p_expresion(p):
    '''
    expresion : expresion SUMA expresion
              | expresion RESTA expresion
              | expresion PRODUCTO expresion
              | expresion DIVISION expresion
              | PARENTESIS_IZQ expresion PARENTESIS_DER
              | TAMANIO_DE PARENTESIS_IZQ expresion PARENTESIS_DER
              | NUMERO
              | IDENTIFICADOR
              | IDENTIFICADOR CORCHETE_IZQ expresion CORCHETE_DER
              | llamado_a_funcion
    '''
    if len(p) == 2:
        p[0] = f"expresion → {p[1]}"
    elif len(p) == 4:
        if p[1] == '(':
            p[0] = f"expresion → ( {p[2]} )"
        else:
            p[0] = f"expresion → {p[1]} {p[2]} {p[3]}"
    else:
        p[0] = f'expresion → {p[1]} {p[2]} {p[3]} {p[4]}'
        
# Llamados a funciones
def p_llamado_a_funcion(p):
    '''
    llamado_a_funcion : IDENTIFICADOR PARENTESIS_IZQ lista_argumentos PARENTESIS_DER
                      | IMPRIMIR PARENTESIS_IZQ lista_argumentos PARENTESIS_DER
    '''
    p[0] = f"llamado_a_funcion → {p[1]} ( {p[3]} )"

# Argumentos de la función
def p_lista_argumentos(p):
    '''
    lista_argumentos : argumento COMA lista_argumentos
                     | argumento
                     | VACIO
    '''
    if len(p) == 4:
        p[0] = f"lista_argumentos → {p[1]} , {p[3]}"
    else:
        p[0] = f"lista_argumentos → {p[1]}"

def p_argumento(p):
    '''
    argumento : expresion
              | CADENA
    '''
    p[0] = f"argumento → {p[1]}"
    
# Retornos
def p_retorno(p):
    '''
    retorno : RETORNAR expresion
            | RETORNAR
    '''
    if len(p) == 3:
        p[0] = f"retorno → {p[1]} {p[2]}"
    else:
        p[0] = f"retorno → {p[1]}"

# Estructuras de control
def p_estructura_de_control(p):
    '''
    estructura_de_control : seleccion
                          | iteracion
    '''
    p[0] = f"estructura_de_control → {p[1]}"

# Estructuras de control de selección
def p_seleccion(p):
    '''
    seleccion : SI PARENTESIS_IZQ condicion PARENTESIS_DER bloque
    '''
    if len(p) == 6:
        p[0] = f"seleccion → if ( {p[3]} ) {p[5]}"

# Estructuras de control de iteración
def p_iteracion(p):
    '''
    iteracion : PARA PARENTESIS_IZQ declaracion_variable PUNTO_Y_COMA condicion PUNTO_Y_COMA asignacion PARENTESIS_DER bloque
    '''
    if len(p) == 10:
        p[0] = f"iteracion → for ( {p[3]} ; {p[5]} ; {p[7]} ) {p[9]}"

# Manejo de errores en la sintaxis
def p_error(p):
    if p:
        print(f"Error de sintaxis en la entrada. Token inesperado: {p.value} en la línea {p.lineno}")
        print(f"Contexto alrededor del error: {p.lexer.lexdata[p.lexpos-20:p.lexpos+20]}")  # Muestra el contexto del error
    else:
        print("Error de sintaxis en la entrada. Final inesperado.")

# Construcción del parser
parser = yacc.yacc(debug=True)

# Función para probar el analizador sintáctico
def test_analizador_sintactico(codigo):
    try:
        res_produccion = parser.parse(codigo)
        if res_produccion:
            print(f"\nLa sintaxis es correcta. El resultado del análisis sintáctico es:\n\n{res_produccion}")
        else:
            print("La sintaxis no es correcta. El análisis sintáctico no tuvo éxito.")
    except Exception as e:
        print(f"Error durante el análisis sintáctico: {e}")

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

# Ejecutar el parser con el código de prueba
test_analizador_sintactico(codigo_a_analizar)