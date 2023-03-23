# Situación Problema 1: “No sólo de los lenguajes populares vive un ITC”: aprendiendo ágilmente un pequeño lenguaje
# Juan Daniel Rodríguez Oropeza A01411625
# 20 de Marzo de 2022

import re # Librería para usar expresiones regulares
import numpy as np # Librería para usar elementos matemáticos un poco más complejos.
# Librería que funciona cuando al darle un input matemático de una onda sonora, la reproducirá tranformándola en una onda acústica.
import sounddevice as sd 
#import sys

# 1. Análisis de Léxico (entrada: texto; salida: lexemas y tokens)
# 2. Análisis de Sintaxis (entrada: lista de tokens; salida: nada (todo bien) error (avisa que hay error de sintaxis))
# 3. Ejecutor de Música (entrada: lista de lexemas de notas, se deslgosa y parametriza; salida: sonido)


# Parte 1: Analizador de léxico
# Tokenizar, converitr tu codigo de entrada en claves
def Tokenizador(linea): # Recibe a la linea
    #sharp = r"(#+)"
    #flat = r"(b+)"
    
    #accidental = sharp + r"|" + flat
    
    #letter = r"(A|B|C|D|E|F|G)"
    
    # Los identificadores en Regex no pueden estar más de una vez.
    #notename = r"(?P<NOTENAME>(A|B|C|D|E|F|G)(#+|b+)*)"
    
    #octave = r"-2|-1|0|1|2|3|4|5|6|7|8"
    #rest = r"R"
    
    #pitch = r"(?P<PITCH>((A|B|C|D|E|F|G)(#+|b+)*)(-2|-1|0|1|2|3|4|5|6|7|8)|(R))"
    
    #tval = r"w|h|q|e|s|t|f"
    
    #dot = r"\.+"
    #let = r"t|3|5|7|9"
    
    #tmod = dot + r"|" + let
    #tmod = r"(?P<TMOD>" + dot + r"|" + let + r")"

    # En caso de que haya que concatenar dos variables regex, una seguida de la otra, lo mejor es escribir manualmente la expresión
    #duration = r"(?P<DURATION>(w|h|q|e|s|t|f)(\.+|(t|3|5|7|9))*)"
    
    # Regex para identificar los lexemas
    # Con 4 claves es suficiente
    Mnote = r"(?P<MNOTE>^(((A|B|C|D|E|F|G)(#+|b+)*)(\-2|\-1|0|1|2|3|4|5|6|7|8)|(R))((w|h|q|e|s|t|f)(\.+|(t|3|5|7|9))?))" # A#e
    idVozInst = r"(?P<IDVOZINST>^[a-z]+)"  #right left letras minusculas
    py = r"(?P<PY>^\|)" # |
    comentarios = r"(?P<COMENTARIOS>^#.+)" # #Comentarios
    
    # Se define el patrón a reconocer tomando en cuenta cualquiera de las 4 claves.
    patron = re.compile("|".join([Mnote, idVozInst, py, comentarios]))
    
    grupos = patron.scanner(linea) # Se hace un escaneo o análisis de la linea.
    
    token = grupos.match() # Se identifica si hay una coincidencia
    
    # Si no se reconoce ningún lexema, manda mensaje de error
    if str(token) == "None":
        print("ERROR: Hay un lexema no válido.\nEl lexema no válido se encuentra justo después de este último que se imprimió.")
        raise SystemExit(" Repito - ERROR: Hay un lexema no válido.") # Se imprime un mensaje de error.
    
    print(token.lastgroup, token.group()) # Se imprime la coincidencia junto con su clave (tipo de lexema)
    
    tokenAInsertar = int(0) # Se define esta variale para saber cual valor de token insertar.
    
    # El token con valor de 1 representa Mnote
    if len(re.findall(Mnote, linea)) > 0: # Si hay al menos una coincidencia...
        tokenAInsertar = int(1) # Se asigna el valor del token
        coincidencia = re.search(Mnote, linea) # Se busca la primera coincidencia que encuentre
        if coincidencia.start() == 0: # Si la coincidencia está al principio de la linea...
            tokens.append(tokenAInsertar) # Se anexa el token a su lista correspondiente
            
    # El token con valor de 2 representa el identificador de voz o instrumento
    elif len(re.findall(idVozInst, linea)) > 0: # Si hay al menos una coincidencia...
        tokenAInsertar = int(2) # Se asigna el valor del token
        coincidencia = re.search(idVozInst, linea) # Se busca la primera coincidencia que encuentre
        if coincidencia.start() == 0: # Si la coincidencia está al principio de la linea...
            tokens.append(tokenAInsertar) # Se anexa el token a su lista correspondiente
            
    # El token con valor de 3 representa el py ( | )
    elif len(re.findall(py, linea)) > 0: # Si hay al menos una coincidencia...
        tokenAInsertar = int(3) # Se asigna el valor del token
        coincidencia = re.search(py, linea) # Se busca la primera coincidencia que encuentre
        if coincidencia.start() == 0: # Si la coincidencia está al principio de la linea...
            tokens.append(tokenAInsertar) # Se anexa el token a su lista correspondiente
            
    # Los comentarios no generan token.
        
    # Cualquier lexema que se reconoza a excepción de los comentarios, se guardan en la lista de lexemas.
    if len(re.findall(comentarios, linea)) == 0:
        lexemas.append(token.group())
    
# Arreglo: Token(1)
# Arreglo: C4e

# Parte 2: Analizador de Sintaxis

# Gramática BNF:
# <Lineas> ::= idVozInst <Notas> | <Lineas>
# <Notas> :: = Mnote (e | py | <Notas>)


# Las claves se usan en la sintaxis para reconocer el orden, si vienen el orden correcto.
def Parser(tokens): # Recibe a la lista de tokens
    for i in tokens: # Analiza cada token de la lista.
        Lineas(i) # Llama a la función.

# <Lineas> ::= idVozInst <Notas> | <Lineas>
def Lineas(token): # Recibe al token
    if token == 2: # Si es un identificador de voz o instrumento...
        sigToken = dameToken() # Pasa al siguiente token
        if sigToken == 0: # Si no hay más tokens por analizar...
                return # Termina la función.
        elif sigToken == 1: # Si es una nota...
            Notas(sigToken) # Llama a la función.
            
        # Si no es ninguna de las opciones anteriores marca error.
        else:
            print("ERROR: Se esperaba una nota en el texto")
            raise SystemExit("Repito - ERROR: Se esperaba una nota")
    # Si no empieza con un identificador de voz o instrumento manda mensaje de error.
    else:
        print("ERROR: Se esperaba un identificacor de Voz o Instrumento al inicio de una linea.")
        raise SystemExit("Repito - ERROR: Se esperaba un identificacor de Voz o Instrumento.")
        
# <Notas> :: = Mnote (e | py | <Notas>)
def Notas(token): # Recibe el token
    if token == 1: # Si es una nota...
        sigToken = dameToken() # Pasa al siguiente token
        if sigToken == 0: # Si no hay más tokens por analizar...
                return # Termina la función.
        Notas(sigToken) # Llama recursivamente a la función de Notas
    elif token == 3: # Si es un py ( | )...
        sigToken = dameToken() # Pasa al siguiente token
        if sigToken == 0: # Si no hay más tokens por analizar...
            return # Termina la función.
        Notas(sigToken) # Llama recursivamente a la función de Notas.
    elif token == 2: # Si es un identificador de voz o instrumento...
        Lineas(token) # Llama a la función de Líneas.
    # Si no es ninguna de las opciones anteriores manda mensaje de error.
    else:
        print("ERROR: Se esperaba una nota en el texto")
        raise SystemExit("Repito - ERROR:Se esperaba una nota")

#Parte 3: Ejecutor de Música

# La frecuencia son las vibraciones de la nota por segundo.
# La frecuencia determina si el sonido será grave o agudo.
def frec(nota: int, octava: int) -> int: # Para calcular la frecuencia se necesita de la nota y la octava.
    # Si el resultado de la resta es mayor, suena más agudo porque vibra con una frecuencia más alta la nota.
    expo = octava * 12 + (nota - 40) # Exponente
    # LA 440 se encuentra por encima del Do central del piano, vibrando a 440 Hz,
    # y ha sido universalmente aceptado como el tono según el cual deben afinarse todos los instrumentos para un concierto,
    # que es el mismo tono que usa el diapasón tradicional. 
    return int(440 * ((2 ** (1 / 12)) ** expo)) # Fórmula para conseguir la frecuencia de cada nota.

# Esta función reproduce sonidos tomando en cuenta la nota, octava, y duración.
def play(nota: int, octava: int, duracion: int)->None:
    # El framerate consiste en agarrar una onda (la cual tiene cierta cantidad de oscilaciones por segundo)
    # y partirla en partes iguales para obtener la altura (amplitud) de esa nota a esos instantes.
    framerate = 44100 # Esta es la cantidad de valores (o partes iguales) por segundo.
    # np.linspace para crear secuencias numéricas.
    t = np.linspace(0, duracion / 1000, int(framerate*duracion/1000)) # El tiempo que se va a reproducir cada nota. La nota dura 1000ms.
    frequency = frec(nota, octava) # Frecuencia.
    onda = np.sin(2 * np.pi * frequency * t) # El sonido que va a reproducir.
    sd.play(onda, framerate) # Reproduce el sonido.
    sd.wait()

# Conversión de las notas en MUT a números
def traduccionNota(lexemas): # Recibe a la lista de lexemas.
    for i in lexemas: # Se analiza cada lexema de la lista.
        # Primero se identifican a las notas en la lista de lexemas.
        if len(re.findall(r"(((A|B|C|D|E|F|G)(#+|b+)*)(\-2|\-1|0|1|2|3|4|5|6|7|8)|(R))((w|h|q|e|s|t|f)(\.+|(t|3|5|7|9))*)", str(i))) > 0:
            # En esta ocasión se analizarán solamente la parte de las notas (Do, Re, Mi, ...), es decir, las letras junto con sus sostenidos y bemoles.
            # La
            if len(re.findall(r"^A", i)) > 0:
                notas.append(int(10))
            # La sostenido / Si bemol
            elif len(re.findall(r"^(A#+|Bb+)", i)) > 0:
                notas.append(int(11))
            # Si / Do bemol
            elif len(re.findall(r"^(B|Cb+)", i)) > 0:
                notas.append(int(12))
            # Si sostenido / Do
            elif len(re.findall(r"^(B#+|C)", i)) > 0:
                notas.append(int(1))
            # Do sostenido / Re bemol
            elif len(re.findall(r"^(C#+|Db+)", i)) > 0:
                notas.append(int(2))
            # Re
            elif len(re.findall(r"^D", i)) > 0:
                notas.append(int(3))
            # Re sostenido / Mi bemol
            elif len(re.findall(r"^(D#+|Eb+)", i)) > 0:
                notas.append(int(4))
            # Mi / Fa bemol
            elif len(re.findall(r"^(E|Fb+)", i)) > 0:
                notas.append(int(5))
            # Mi sostenido / Fa
            elif len(re.findall(r"^(E#+|F)", i)) > 0:
                notas.append(int(6))
            # Fa sostenido / Sol bemol
            elif len(re.findall(r"^(F#+|Gb+)", i)) > 0:
                notas.append(int(7))
            # Sol
            elif len(re.findall(r"^G", i)) > 0:
                notas.append(int(8))
            # Sol sostenido / La bemol
            elif len(re.findall(r"^(G#+|Ab+)", i)) > 0:
                notas.append(int(9))
            # Silencio / Descanso
            elif len(re.findall(r"^R", i)) > 0:
                notas.append(int(-10000000))
                octavas.append(int(-10000000))
            # Los valores se añaden en una nueva lista.

# Conversión de las octavas en MUT a números
def traduccionOctava(lexemas): # Recibe a la lista de lexemas
    for i in lexemas: # Se analiza cada lexema de la lista.
        # Primero se identifican a las notas en la lista de lexemas.
        if len(re.findall(r"(((A|B|C|D|E|F|G)(#+|b+)*)(\-2|\-1|0|1|2|3|4|5|6|7|8)|(R))((w|h|q|e|s|t|f)(\.+|(t|3|5|7|9))*)", str(i))) > 0:
            # En esta ocasión se analizarán solamente la parte de las octavas, es decir los números.
            # -2
            if len(re.findall(r"\-2(w|h|q|e|s|t|f)$", i)) > 0:
                octavas.append(int(-2))
            # -1
            elif len(re.findall(r"\-1(w|h|q|e|s|t|f)$", i)) > 0:
                octavas.append(int(-1))
            # 0
            elif len(re.findall(r"0(w|h|q|e|s|t|f)$", i)) > 0:
                octavas.append(int(0))
            # 1
            elif len(re.findall(r"1(w|h|q|e|s|t|f)$", i)) > 0:
                octavas.append(int(1))
            # 2
            elif len(re.findall(r"2(w|h|q|e|s|t|f)$", i)) > 0:
                octavas.append(int(2))
            # 3
            elif len(re.findall(r"3(w|h|q|e|s|t|f)$", i)) > 0:
                octavas.append(int(3))
            # 4
            elif len(re.findall(r"4(w|h|q|e|s|t|f)$", i)) > 0:
                octavas.append(int(4))
            # 5
            elif len(re.findall(r"5(w|h|q|e|s|t|f)$", i)) > 0:
                octavas.append(int(5))
            # 6
            elif len(re.findall(r"6(w|h|q|e|s|t|f)$", i)) > 0:
                octavas.append(int(6))
            # 7
            elif len(re.findall(r"7(w|h|q|e|s|t|f)$", i)) > 0:
                octavas.append(int(7))
            # 8
            elif len(re.findall(r"8(w|h|q|e|s|t|f)$", i)) > 0:
                octavas.append(int(8))
            # Los valores se añaden en una nueva lista.

# Conversión de las duraciones en MUT a números
def traduccionDuracion(lexemas): # Recibe a la lista de lexemas.
    whole = int(2000) # 2 segundos
    for i in lexemas: # Se analiza cada lexema de la lista.
        # Primero se identifican a las notas en la lista de lexemas.
        if len(re.findall(r"(((A|B|C|D|E|F|G)(#+|b+)*)(\-2|\-1|0|1|2|3|4|5|6|7|8)|(R))((w|h|q|e|s|t|f)(\.+|(t|3|5|7|9))*)", str(i))) > 0:
             # En esta ocasión se analizarán solamente la parte de las duraciones, es decir las letras minúsculas.
            # 1
            if len(re.findall(r"w$", i)) > 0:
                duraciones.append(whole)
            # 1/2
            elif len(re.findall(r"h$", i)) > 0:
                duraciones.append(int(whole/2))
            # 1/4
            elif len(re.findall(r"q$", i)) > 0:
                duraciones.append(int(whole/4))
            # 1/8
            elif len(re.findall(r"e$", i)) > 0:
                duraciones.append(int(whole/8))
            # 1/16
            elif len(re.findall(r"s$", i)) > 0:
                duraciones.append(int(whole/16))
            # Los valores se añaden en una nueva lista.

#notas = ["C"]
#octavas = [4, 4]
#duraciones = [1000, 500]


tokens = [] # Se almacenan los tokens
lexemas = [] # Se almacenan los lexemas

tokensCopia = tokens # Se hace una copia de lista de tokens para poder realizar el analizador de sintaxis (parser).

# Función que pasa al siguiente token de la lista
def dameToken():
    # Cuando ya no haya más tokens por analizar se regresa el valor de 0 para que el parser sepa que ya se terminó el análisis.
    if len(tokensCopia) == 1:
        print("\nLa sintaxis es correcta.")
        return int(0)
    else: # En caso contrario...
        print(tokensCopia[0])
        #print("Cuantos quedan: " + str(len(tokensCopia)))
        tokensCopia.pop(0) # Se elimina el primer elemento de la lista de tokens.
        return tokensCopia[0] # Regresa el primer valor de la lista.


notas = [] # Se almacenan las notas.
octavas = [] # Se almacenan las octavas.
duraciones = [] # Se almacenan las duraciones.

# El usuario inserta el nombre del archivo
print("Inserte el nombre del archivo de texto: ")
nombreTxt = input()

# Lectura del archivo
with open(nombreTxt) as archivo:
    for linea in archivo: # Se lee cada linea
        lineaAct = linea # Se define una nueva variable para actualizar la linea.
        # Se elminan los espacios o tabluaciones que están al inicio de la línea.
        patron = "^( |\t)+"
        lineaAct = re.sub(patron, '', lineaAct)
        # Se elminan los espacios o tabluaciones que están al final de la línea.
        patron = "( |\t)+$"
        lineaAct = re.sub(patron, '', lineaAct)
        # Si no hay comentarios al inicio de la linea se empieza a buscar por los demás lexemas.
        if len(re.findall(r"^#.+", lineaAct)) == 0:
            cantEspacio = linea.count(' ') + linea.count('\t') # Se cuentan los espacios y tabluaciones para saber cuantas veces habrá que analizar la linea.
            for i in range(cantEspacio + 1):
                # Al analizar la linea se van buscando por lexemas y elminando los espacios para que el analizador de léxico (scanner) no tenga problemas.
                token = Tokenizador(lineaAct) # Se llama al tokenizador.
                patron = "^\S+( |\t)+"
                lineaAct = re.sub(patron, '', lineaAct)
                #print(lineaAct)
        # En caso contrario solamente se busca por el comentario sin eliminar espacios ni tabulaciones que se encuentren en el resto de la linea.
        else:
            token = Tokenizador(lineaAct) # Se llama al tokenizador.


# Se imprime la lista de tokens y lexemas.
print(*tokens)
print(*lexemas)

print("\nLos lexemas son correctos.")

Parser(tokens) # Se llama al analizador de sintaxis.


# Llamados para traducir o converitr las notas de MUT a números para que los pueda leer la librería de sounddevice.
traduccionNota(lexemas)
traduccionOctava(lexemas)
traduccionDuracion(lexemas)

# Imprime las listas.
print(*notas)
print(*octavas)
print(*duraciones)

# Reproducelas notas ya parametrizadas para que la librería de sounddevice las reconozca.
for n, o, d in zip(notas, octavas, duraciones):
    play(n, o, d)