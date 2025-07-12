# Diccionario para almacenar los datos de los estudiantes
estudiantes = {}

print("Registro de Estudiantes")
print("Escriba 'fin' para finalizar el ingreso.\n")

# Entrada de datos
while True:
    nombre = input("Ingrese el nombre del estudiante (o 'fin' para terminar): ")
    if nombre.lower() == "fin":
        break
    try:
        nota = float(input("Ingrese la nota final: "))
        if nota < 0 or nota > 10:
            print("La nota debe estar entre 0 y 10.")
            continue
        estudiantes[nombre] = nota
    except ValueError:
        print("Entrada inválida. La nota debe ser un número.")

# Procesamiento
total = len(estudiantes)
aprobados = []
reprobados = []
suma_notas = 0

for nombre, nota in estudiantes.items():
    suma_notas += nota
    if nota >= 6.0:
        aprobados.append(nombre)
    else:
        reprobados.append(nombre)

# Resultados
if total > 0:
    promedio = suma_notas / total
    print("\nResultados:")
    print(f"Total estudiantes: {total}")
    print(f"Aprobados: {len(aprobados)}")
    print(f"Reprobados: {len(reprobados)}")
    print(f"Promedio general: {promedio:.2f}")
else:
    print("\nNo se ingresaron datos.")
