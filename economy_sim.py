import random
import json

# Recursos y precios iniciales
recursos = {
    "energía": {"precio": 10, "stock": 100},
    "comida": {"precio": 5, "stock": 200},
    "agua": {"precio": 8, "stock": 150},
    "tecnología": {"precio": 20, "stock": 50},
}

historico_precios = {recurso: [] for recurso in recursos}

dinero = 100  # Créditos iniciales
inventario = {recurso: 0 for recurso in recursos}

roles = {
    "comerciante": {"descuento": 0.2},  # 20% de descuento para el comerciante
    "hacker": {"riesgo": 0.5},  # 50% de probabilidad de éxito para hackear
    "ciudadano": {"neutral": True},
}

rol = None  # El rol será asignado después de la selección

# Guardar y cargar estado del juego
def guardar_estado():
    estado = {
        "recursos": recursos,
        "dinero": dinero,
        "inventario": inventario,
        "historico_precios": historico_precios,
    }
    with open("estado_juego.json", "w") as archivo:
        json.dump(estado, archivo, indent=4)
    print("\nEstado del juego guardado.")

def cargar_estado():
    global recursos, dinero, inventario, historico_precios
    try:
        with open("estado_juego.json", "r") as archivo:
            estado = json.load(archivo)
            recursos = estado["recursos"]
            dinero = estado["dinero"]
            inventario = estado["inventario"]
            historico_precios = estado["historico_precios"]
        print("\nEstado del juego cargado.")
    except FileNotFoundError:
        print("\nNo se encontró un estado guardado. Comenzando un nuevo juego.")

# Mostrar estado del mercado en la terminal
def mostrar_estado():
    print("\n=== Estado del Mercado ===")
    for recurso, datos in recursos.items():
        print(f"{recurso.capitalize()}: {datos['precio']} créditos (Stock: {datos['stock']})")
    print(f"Dinero disponible: {dinero} créditos")
    print(f"Inventario: {inventario}")

# Generar un evento aleatorio (solo después de compra o venta)
def evento_mercado_avanzado():
    eventos = [
        {"nombre": "Descubrimiento de energía renovable", "impactos": {"energía": -3, "tecnología": 5}},
        {"nombre": "Sequía severa", "impactos": {"agua": 10, "comida": 7}},
        {"nombre": "Crisis económica", "impactos": {"energía": 5, "tecnología": -4, "agua": 3}},
        {"nombre": "Revolución tecnológica", "impactos": {"tecnología": -10, "energía": 7}},
        {"nombre": "Epidemia global", "impactos": {"comida": 15, "agua": 10}},
        {"nombre": "Conflicto regional", "impactos": {"energía": 8, "tecnología": 6}},
    ]
    evento = random.choice(eventos)
    print(f"\n¡Evento del mercado! {evento['nombre']}")
    for recurso, cambio in evento["impactos"].items():
        recursos[recurso]["precio"] = max(1, recursos[recurso]["precio"] + cambio)

# Probabilidad de evento
def probabilidad_evento():
    if random.random() <= 0.25:  # 25% de probabilidad
        evento_mercado_avanzado()  # Llamamos a la función del evento aleatorio

# Hackear precios (solo para el rol hacker)
def hackear_precio(recurso):
    global dinero
    if rol == "hacker":
        if dinero >= 2:  # Costo de 2 créditos para hackear
            exito = random.random() <= 0.5  # 50% de probabilidad de éxito
            if exito:
                cambio = random.randint(-5, 5)  # Cambiar el precio en un rango aleatorio entre -5 y 5
                recursos[recurso]["precio"] = max(1, recursos[recurso]["precio"] + cambio)  # El precio no puede ser menor que 1
                dinero -= 2  # Restamos 2 créditos por el hackeo
                print(f"¡Has hackeado el precio de {recurso} exitosamente! El precio cambió en {cambio} créditos.")
            else:
                dinero -= 2  # Restamos los 2 créditos aunque falle el hackeo
                print(f"El intento de hackeo de {recurso} falló. Has perdido 2 créditos.")
        else:
            print("No tienes suficiente dinero para hackear.")
    else:
        print("Solo los hackers pueden hackear precios.")

# Regatear precio (solo para el rol comerciante)
def regatear_precio(recurso):
    global dinero
    if rol == "comerciante":
        if dinero >= 2:  # Costo de 2 créditos para regatear
            exito = random.random() <= 0.6  # 60% de probabilidad de éxito
            if exito:
                descuento = random.uniform(0.1, 0.3)  # Descuento entre 10% y 30%
                nuevo_precio = recursos[recurso]["precio"] * (1 - descuento)
                recursos[recurso]["precio"] = max(1, nuevo_precio)  # El precio no puede ser menor que 1
                dinero -= 2  # Restamos los 2 créditos por el regateo
                print(f"¡Has regateado exitosamente el precio de {recurso}! Nuevo precio: {nuevo_precio:.2f} créditos.")
            else:
                dinero -= 2  # Restamos los 2 créditos aunque falle el regateo
                print(f"El intento de regateo de {recurso} falló. Has perdido 2 créditos.")
        else:
            print("No tienes suficiente dinero para regatear.")
    else:
        print("Solo los comerciantes pueden regatear precios.")

# Comprar un recurso
def comprar():
    global dinero
    mostrar_estado()
    recurso = input("\nSelecciona un recurso para comprar (energía, comida, agua, tecnología): ").lower()
    cantidad = int(input("Cantidad a comprar: "))
    
    if recurso in recursos:
        costo_unitario = recursos[recurso]["precio"]
        if rol == "comerciante":
            costo_unitario = regatear_precio(recurso)  # Intentamos regatear el precio
        costo = costo_unitario * cantidad
        if dinero >= costo and recursos[recurso]["stock"] >= cantidad:
            dinero -= costo
            inventario[recurso] += cantidad
            recursos[recurso]["stock"] -= cantidad
            probabilidad_evento()
            print(f"Has comprado {cantidad} unidades de {recurso} por {costo:.2f} créditos.")
            verificar_game_over()  # Verificar si se llega a 0 créditos
        else:
            print("No tienes suficiente dinero o no hay suficiente stock.")
    else:
        print("Recurso no válido.")

# Vender un recurso
def vender():
    global dinero
    mostrar_estado()
    recurso = input("\nSelecciona un recurso para vender (energía, comida, agua, tecnología): ").lower()
    cantidad = int(input("Cantidad a vender: "))
    
    if recurso in recursos:
        if inventario[recurso] >= cantidad:
            precio_unitario = recursos[recurso]["precio"]
            if rol == "comerciante":
                precio_unitario = regatear_precio(recurso)  # Intentamos regatear el precio
            ganancia = precio_unitario * cantidad
            dinero += ganancia
            inventario[recurso] -= cantidad
            recursos[recurso]["stock"] += cantidad
            probabilidad_evento()
            print(f"Has vendido {cantidad} unidades de {recurso} por {ganancia} créditos.")
            verificar_game_over()  # Verificar si se llega a 0 créditos
        else:
            print("No tienes suficiente cantidad para vender.")
    else:
        print("Recurso no válido.")

# Verificar si el jugador ha perdido
def verificar_game_over():
    if dinero <= 0:
        print("¡Has quedado sin dinero! El juego ha terminado.")
        exit()

# Función para cambiar el rol seleccionado
def cambiar_rol():
    global rol
    print("\nSelecciona tu rol:")
    print("1. Comerciante")
    print("2. Hacker")
    print("3. Ciudadano")
    opcion = input("Opción: ")

    if opcion == "1":
        rol = "comerciante"
    elif opcion == "2":
        rol = "hacker"
    elif opcion == "3":
        rol = "ciudadano"
    else:
        print("Rol no válido. Elige nuevamente.")
        cambiar_rol()

# Menú principal del juego
def menu():
    global rol
    cambiar_rol()
    while True:
        print("\n=== Menú ===")
        print("1. Mostrar Estado del Mercado")
        print("2. Comprar")
        print("3. Vender")
        print("4. Hackear Precio (solo para hacker)")
        print("5. Regatear Precio (solo para comerciante)")
        print("6. Guardar Estado")
        print("7. Cargar Estado")
        print("8. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            mostrar_estado()
        elif opcion == "2":
            comprar()
        elif opcion == "3":
            vender()
        elif opcion == "4" and rol == "hacker":
            recurso = input("¿Qué recurso quieres hackear? ")
            hackear_precio(recurso)
        elif opcion == "5" and rol == "comerciante":
            recurso = input("¿Qué recurso quieres regatear? ")
            regatear_precio(recurso)
        elif opcion == "6":
            guardar_estado()
        elif opcion == "7":
            cargar_estado()
        elif opcion == "8":
            print("Gracias por jugar. ¡Hasta pronto!")
            break
        else:
            print("Opción no válida.")

# Iniciar el juego
menu()
