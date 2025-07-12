# Calculadora de Promedios - Nivel Medio

print("Ingrese las notas de los estudiantes.")
print("Escriba 'fin' para terminar el ingreso.\n")

suma_notas = 0
cantidad_estudiantes = 0
aprobados = 0
reprobados = 0

while True:
    entrada = input("Ingrese una nota o escriba 'fin': ")
    if entrada.lower() == "fin":
        break

    try:
        nota = float(entrada)
        if nota < 0 or nota > 10:
            print("La nota debe estar entre 0 y 10. Intente nuevamente.")
            continue

        suma_notas += nota
        cantidad_estudiantes += 1

        if nota >= 6.0:
            aprobados += 1
        else:
            reprobados += 1

    except ValueError:
        print("Entrada no válida. Ingrese un número o 'fin'.")

# Mostrar resultados solo si se ingresaron notas
if cantidad_estudiantes > 0:
    promedio = suma_notas / cantidad_estudiantes
    
    print("\nResultados:")
    print(f"Promedio general: {promedio:.2f}")
    print(f"Estudiantes aprobados: {aprobados}")
    print(f"Estudiantes reprobados: {reprobados}")
    print(f"Total de estudiantes: {cantidad_estudiantes}")
else:
    print("\nNo se ingresaron notas.")
