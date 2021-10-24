#Trabajo grupal python de ecuaciones 3x3
#integrantes: Nahuel Diaz, Ronald Hilari, Nehuen Laje, Jonathan Alvarez Flores, Xoan Altaleff.
import sys

#menu(): Muestra un menú para ingresar un sistema 3x3.
def menu():
    print('¿Qué quieres hacer?\n\t1- Resolver un sistema de ecuaciones lineales 3x3.\n\t2- Salir del menu.')
    try:
        a= int(input())
    except ValueError:
        sys.exit('Entrada inválida')
    if (a== 1):
        global input_matrix
        input_matrix= [input_handler(input('Ingresar la primera ecuación\n')), input_handler(input('Ingresar la segunda ecuación\n')), input_handler(input('Ingresar la tercera ecuación\n'))]
        type_checker(input_matrix)
        return
    elif (a == 2):
        print('\tSaliendo del menu...')
        sys.exit()
    else:
        sys.exit('Entrada inválida')
    

#input_handler(): Convierte el sistema de una cadena a una matriz (lista 2d). También previene errores de entrada.
def input_handler(str):
    x= lambda a: float(a)
    try:
        if (str.find(',')== -1):
            equation= list(map(x, str.split(' ')))
            if (len(equation) != 4):
                sys.exit('Entrada inválida')
            return equation
        else:
            equation= list(map(x, str.replace(' ', '').split(',')))
            if (len(equation) != 4):
                sys.exit('Entrada inválida')
            return equation
    except ValueError:
        sys.exit('Entrada inválida')

# type_checker(): Determina el tipo de sistema en función de si las ecuaciones y sus resultados son múltiplos.
def type_checker(M):
    e1_e2_constants_multiples, e2_e3_constants_multiples, e3_e1_constants_multiples, e1_e2_results_multiples, e2_e3_results_multiples, e3_e1_results_multiples= multiples_identifier(M)
    #elimina ecuaciones que son múltiplos
    if (e1_e2_constants_multiples):
        print('La primera y la segunda ecuación son múltiplos')
        if (not e1_e2_results_multiples):
            inconsistent_handler()
            return
        else:
            M[0]= None
    if (e2_e3_constants_multiples):
        print('La segunda y la tercera ecuación son múltiplos')
        if (not e2_e3_results_multiples):
            inconsistent_handler()
            return
        else:
            M[1]= None
    if (e3_e1_constants_multiples):
        print('La primera y la tercera ecuación son múltiplos')
        if (not e3_e1_results_multiples):
            inconsistent_handler()
            return
        else:
            M[2]= None
    done= False
    while not done:
        try:
            M.remove(None)
        except ValueError:
            done= True
    if (not M or len(M)==1):
        print("Todas las ecuaciones del sistema son múltiples o nulas, los sistemas no se pueden calcular.")
        return

    #Aplica rref.
    result= reduced_row_echelon_form(M)
    try:
        if (result[2][2]==1):
            determined_handler(result)
            return
        if (result[2][3]!=0):
            inconsistent_handler()
            return
    except IndexError:
        pass
    underdetermined_handler(result)
    return


#multiples_identifier(): Determina si un par de ecuaciones son múltiplos.
def multiples_identifier(M):
    #Establece una serie de comprobaciones que se evaluarán o no según el denominador (si 0 no evalúa).
    check= [['M[0][0] / M[1][0]', 'M[0][1] / M[1][1]', 'M[0][2] / M[1][2]'],['M[1][0] / M[2][0]', 'M[1][1] / M[2][1]', 'M[1][2] / M[2][2]'],['M[2][0] / M[0][0]', 'M[2][1] / M[0][1]', 'M[2][2] / M[0][2]']]
    #Supone que no hay múltiplos
    e1_e2_constants_multiples= False
    e2_e3_constants_multiples= False
    e3_e1_constants_multiples= False
    #e inicializa vars para uso futuro.
    e1_e2_results_multiples= None
    e2_e3_results_multiples= None
    e3_e1_results_multiples= None
    #Prueba si las constantes del sistema son adecuadas para la división. Si no es así, elimina el check correspondiente. Si un denominador es 0, pero el numerador correspondiente no lo es; no se hace ninguna verificación (no son múltiplos).
    for i in range(3):
        #checks for M[1]
        if (check[0] and M[1][i]==0):
            if (M[0][i]==0):
                check[0][i]= ''
            else:
                check[0]= False
        #checks for M[2]
        if (check[1] and M[2][i]==0):
            if (M[1][i]==0):
                check[1][i]= ''
            else:
                check[1]= False
        #checks for M[0]
        if (check[2] and M[0][i]==0):
            if (M[2][i]==0):
                check[2][i]= ''
            else:
                check[2]= False

    #Manejar los resultados del sistema que son cero.
    if (M[1][3]==0):
        if (M[0][3]==0):
            e1_e2_results_multiples= True
        else:
            e1_e2_results_multiples= False
    if (M[2][3]==0):
        if (M[1][3]==0):
            e2_e3_results_multiples= True
        else:
            e2_e3_results_multiples= False
    if (M[0][3]==0):
        if (M[2][3]==0):
            e3_e1_results_multiples= True
        else:
            e3_e1_results_multiples= False
    #Constructor de declaraciones.
    if (check[0]):
        #Elimina las entradas falsas.
        done= False
        while not done:
            try:
                check[0].remove('')
            except ValueError:
                done= True

        #Construye la condición para las constantes del sistema.
        check0_length= len(check[0])
        if (check0_length == 1 or check0_length == 0):
            e1_e2_constants_multiples= True
        elif (check0_length == 2):
            e1_e2_constants_multiples= eval(f'{check[0][0]} == {check[0][1]}')
        elif (check0_length == 3):
            e1_e2_constants_multiples= eval(f'{check[0][0]} == {check[0][1]} == {check[0][2]}')
        #Construye la condición para los resultados del sistema.
        if (e1_e2_results_multiples == None):
            if (check0_length == 0):
                e1_e2_results_multiples= False
            else:
                e1_e2_results_multiples= eval(f'{check[0][0]} == M[0][3]/M[1][3]')
    if (check[1]):
        #Elimina las entradas falsas.
        done= False
        while not done:
            try:
                check[1].remove('')
            except ValueError:
                done= True
        #Construye la condición para las constantes del sistema.
        check1_length= len(check[1])
        if (check1_length == 1 or check1_length == 0):
            e2_e3_constants_multiples= True    
        elif (check1_length == 2):
            e2_e3_constants_multiples= eval(f'{check[1][0]} == {check[1][1]}')
        elif (check1_length == 3):
            e2_e3_constants_multiples= eval(f'{check[1][0]} == {check[1][1]} == {check[1][2]}')
        #Construye la condición para los resultados del sistema.
        if (e2_e3_results_multiples == None):
            if (check1_length == 0):
                e2_e3_results_multiples= False
            else:
                e2_e3_results_multiples= eval(f'{check[1][0]} == M[1][3]/M[2][3]')
    if (check[2]):
        #eliminar entradas falsas.
        done= False
        while not done:
            try:
                check[2].remove('')
            except ValueError:
                done= True
        #Construye la condición para las constantes del sistema.
        check2_length= len(check[2])
        if (check2_length == 1 or check2_length == 0):
            e3_e1_constants_multiples= True    
        elif (check2_length == 2):
            e3_e1_constants_multiples= eval(f'{check[2][0]} == {check[2][1]}')
        elif (check2_length == 3):
            e3_e1_constants_multiples= eval(f'{check[2][0]} == {check[2][1]} == {check[2][2]}')
        #Construye la condición para los resultados del sistema.
        if (e3_e1_results_multiples == None):
            if (check2_length == 0):
                e3_e1_results_multiples= False
            else:
                e3_e1_results_multiples= eval(f'{check[2][0]} == M[2][3]/M[0][3]')
    
    return [e1_e2_constants_multiples, e2_e3_constants_multiples, e3_e1_constants_multiples, e1_e2_results_multiples, e2_e3_results_multiples, e3_e1_results_multiples]


def reduced_row_echelon_form(M):
    lead = 0
    row_count = len(M)
    column_count = len(M[0])
    for r in range(row_count):
        if lead >= column_count:
            return None
        i = r
        while M[i][lead] == 0:
            i += 1
            if i == row_count:
                i = r
                lead += 1
                if column_count == lead:
                    return None
        M[i],M[r] = M[r],M[i]
        lv = M[r][lead]
        M[r] = [ mrx / float(lv) for mrx in M[r]]
        for i in range(row_count):
            if i != r:
                lv = M[i][lead]
                M[i] = [ iv - lv*rv for rv,iv in zip(M[r],M[i])]
        lead += 1
    return M

def inconsistent_handler():
    print('El sistema es incompatible\n')
    return

def determined_handler(M):
    print("El sistema es determinado")
    print(f"S: \nx={round(M[0][3], 3)}\ny={round(M[1][3], 3)}\nz={round(M[2][3], 3)}")
    return

def underdetermined_handler(M):
    print('El sistema es indeterminado')
    #redondea los números de la matriz guardándolos en otra matriz para luego reemplazarlos en la ecuación
    rounded_M = []

    for arr in M:
        rounded_arr = []
        for number in arr:
            rounded_arr.append(round(number, 3))
        rounded_M.append(rounded_arr)
    #función lambda para corregir los casos en los que un número negativo se quedó con 2 signos negativos convirtiéndolo en un número positivo como debería ser
    minus = lambda num: f"+{abs(num)}" if num < 0 or num==0 else f"-{abs(num)}"
    #imprimiendo la ecuación
    print(f"S: x=λ\n   y=({rounded_M[1][3]}{minus(rounded_M[1][2])}·(({rounded_M[0][3]}{minus(rounded_M[0][0])}·λ)/{rounded_M[0][2]}))/{rounded_M[1][1]}\n   z=({rounded_M[0][3]}{minus(rounded_M[0][0])}·λ)/{rounded_M[0][2]}")
    
    print("¿Quieres calcular para lambda?\n\t1- Si\n\t2- No")
    try:
        a= int(input())
    except ValueError:
        sys.exit('Entrada inválida')
    if (a == 1):
        print("Ingresar un valor para lambda")
        λ = float(input())
        #ecuaciones
        equation_for_z=(M[0][3]-M[0][0]*λ)/(M[0][2])
        equation_for_y=(M[1][3]-M[1][2])*(equation_for_z)/M[1][1]

        print(f"Dada λ={λ}\nS:  x={λ}\n    y={round(equation_for_y, 3)}\n    z={round(equation_for_z, 3)}")
    if (a == 2):
        return

print('Solucionador de ecuaciones lineales 3x3')
while True:
    menu()