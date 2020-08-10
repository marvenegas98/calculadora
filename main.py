import calc
import sys

file1 = open(sys.argv[1], 'r')
file2 = open("salida.txt", 'w+') 
lines = file1.readlines()
num_linea = 1
resultado = ""

for line in lines:
    if line:
        result = calc.run(line)

    if (not str(result).isdigit()) and (str(result) != "None"):
        resultado += str(result)+", Error en la linea "+str(num_linea)
        file2.write(resultado)
        file2.write('\n')

    if str(result) != "None" and str(result).isdigit() :
        resultado = str(result)
        file2.write(resultado)
        file2.write('\n')
    resultado = ""
    num_linea += 1


file1.close()
file2.close()
exit()
