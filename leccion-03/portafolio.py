# Función para evaluar si un estudiante aprueba o reprueba

def evaluar_estudiante(nombre, promedio):
    if promedio >= 6.0:
        print(f"\n{nombre} ha aprobado.")
        return True
    else:
        print(f"\n{nombre} ha reprobado.")
        return False

# Programa principal
print("Evaluación de Estudiantes")
print("----------------------------")

# Contadores
aprobados = 0
reprobados = 0
total = 0

while True:
    nombre = input("\nIngrese el nombre del estudiante (o escriba 'fin' para salir): ")
    if nombre.lower() == "fin":
        break
    try:
        promedio = float(input("Ingrese el promedio final: "))
        resultado = evaluar_estudiante(nombre, promedio)
        total += 1
        if resultado:
            aprobados += 1
        else:
            reprobados += 1
    except ValueError:
        print("Error: El promedio debe ser un número. Intente nuevamente.")

# Resumen final
print("\nResumen:")
print(f"Total evaluados: {total}")
print(f"Aprobados: {aprobados}")
print(f"Reprobados: {reprobados}")
