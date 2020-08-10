import calc
import sys

file1 = open(sys.argv[1], 'r')
file2 = open("salida.txt", 'w+') 
lines = file1.readlines()
al = "Etapa: Análisis Léxico: Completada correctamente"
asi = "Etapa: Análisis Sintactico: Completada correctamente"
ase = "Etapa: Análisis Semantico: Completada correctamente"
num_linea = 1
resultado = ""

for line in lines:
    if line:
        result = calc.run(line)

    if (not str(result).isdigit()) and (str(result) != "None"):
        
        if(str(result).find('Sintáctico') != -1):
            resultado = al + '\n'

        elif(str(result).find('Semantico') != -1):
            resultado = al + '\n' + asi + '\n'
        
        resultado += str(result)+", Error en la linea "+str(num_linea)
        file2.write(resultado)
        file2.write('\n')
        exit()


    if str(result) != "None" and str(result).isdigit() :
        resultado = al + '\n' + asi + '\n' + ase + '\n' + "Resultado de la operacion: " + str(result)
        file2.write(resultado)
        file2.write('\n')
    resultado = ""
    num_linea += 1


file1.close()
file2.close()
exit()
