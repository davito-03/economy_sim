import random
import json
import matplotlib.pyplot as plt

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
    "comerciante": {"descuento": 0.9},
    "hacker": {"riesgo": 0.3},
    "ciudadano": {"neutral": True},
}

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

print("Elige tu rol:")
print("1. Comerciante (compra más barato)")
print("2. Hacker (puede manipular precios con riesgo)")
print("3. Ciudadano (sin ventajas ni desventajas)")
opcion_rol = input("Selecciona 1, 2 o 3: ")
if opcion_rol == "1":
    rol = "comerciante"
elif opcion_rol == "2":
    rol = "hacker"
else:
    rol = "ciudadano"

# Mostrar estado del mercado
def mostrar_estado():
    print("\n=== Estado del Mercado ===")
    for recurso, datos in recursos.items():
        print(f"{recurso.capitalize()}: {datos['precio']} créditos (Stock: {datos['stock']})")
    print(f"Dinero disponible: {dinero} créditos")
    print(f"Inventario: {inventario}")

# Generar un evento aleatorio
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

# Comprar un recurso
def comprar(recurso, cantidad):
    global dinero
    costo_unitario = recursos[recurso]["precio"]
    if rol == "comerciante":
        costo_unitario *= roles[rol]["descuento"]
    costo = costo_unitario * cantidad

    if dinero >= costo and recursos[recurso]["stock"] >= cantidad:
        dinero -= costo
        inventario[recurso] += cantidad
        recursos[recurso]["stock"] -= cantidad
        print(f"\nHas comprado {cantidad} unidades de {recurso} por {costo:.2f} créditos.")
    else:
        print("\nNo tienes suficiente dinero o no hay suficiente stock para comprar eso.")

# Vender un recurso
def vender(recurso, cantidad):
    global dinero
    if inventario[recurso] >= cantidad:
        ganancia = recursos[recurso]["precio"] * cantidad
        dinero += ganancia
        inventario[recurso] -= cantidad
        recursos[recurso]["stock"] += cantidad
        print(f"\nHas vendido {cantidad} unidades de {recurso} por {ganancia} créditos.")
    else:
        print("\nNo tienes suficiente cantidad para vender.")

# Hackear precios (solo para hackers)
def hackear():
    if rol != "hacker":
        print("\nSolo los hackers pueden intentar manipular los precios.")
        return

    recurso = input("¿Qué recurso quieres hackear? (energía/comida/agua/tecnología): ").lower()
    if recurso in recursos:
        exito = random.random() > roles[rol]["riesgo"]
        if exito:
            cambio = random.randint(-10, 10)
            recursos[recurso]["precio"] = max(1, recursos[recurso]["precio"] + cambio)
            print(f"\n¡Hackeo exitoso! El precio de {recurso} cambió en {cambio} créditos.")
        else:
            print("\nEl hackeo falló y perdiste 10 créditos.")
            global dinero
            dinero = max(0, dinero - 10)
    else:
        print("Recurso no válido.")

# Graficar precios
def graficar_precios():
    for recurso in recursos:
        historico_precios[recurso].append(recursos[recurso]["precio"])

    plt.figure(figsize=(10, 5))
    for recurso, precios in historico_precios.items():
        plt.plot(precios, label=recurso)
    plt.legend()
    plt.title("Fluctuaciones de precios en el mercado")
    plt.xlabel("Turnos")
    plt.ylabel("Precio")
    plt.show()

# Simulación
cargar_estado()
while True:
    mostrar_estado()
    accion = input("\n¿Qué quieres hacer? (comprar/vender/evento/hackear/graficar/guardar/salir): ").lower()
    if accion == "salir":
        print("¡Gracias por jugar!")
        break
    elif accion == "evento":
        evento_mercado_avanzado()
    elif accion == "comprar":
        recurso = input("¿Qué recurso? (energía/comida/agua/tecnología): ").lower()
        if recurso in recursos:
            cantidad = int(input("¿Cuántas unidades?: "))
            comprar(recurso, cantidad)
        else:
            print("Recurso no válido.")
    elif accion == "vender":
        recurso = input("¿Qué recurso? (energía/comida/agua/tecnología): ").lower()
        if recurso in recursos:
            cantidad = int(input("¿Cuántas unidades?: "))
            vender(recurso, cantidad)
        else:
            print("Recurso no válido.")
    elif accion == "hackear":
        hackear()
    elif accion == "graficar":
        graficar_precios()
    elif accion == "guardar":
        guardar_estado()
    else:
        print("Acción no válida.")
