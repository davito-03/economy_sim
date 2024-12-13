import random
import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

# Mostrar estado del mercado en la GUI
def mostrar_estado_gui():
    estado_texto = "\n=== Estado del Mercado ===\n"
    for recurso, datos in recursos.items():
        estado_texto += f"{recurso.capitalize()}: {datos['precio']} créditos (Stock: {datos['stock']})\n"
    estado_texto += f"Dinero disponible: {dinero} créditos\n"
    estado_texto += f"Inventario: {inventario}\n"
    estado_label.config(text=estado_texto)

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
                messagebox.showinfo("Éxito", f"¡Has hackeado el precio de {recurso} exitosamente! El precio cambió en {cambio} créditos.")
            else:
                dinero -= 2  # Restamos los 2 créditos aunque falle el hackeo
                messagebox.showwarning("Fracaso", f"El intento de hackeo de {recurso} falló. Has perdido 2 créditos.")
        else:
            messagebox.showwarning("Fondos Insuficientes", "No tienes suficiente dinero para hackear.")
    else:
        messagebox.showwarning("Acción no permitida", "Solo los hackers pueden hackear precios.")

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
                messagebox.showinfo("Éxito", f"¡Has regateado exitosamente el precio de {recurso}!\nNuevo precio: {nuevo_precio:.2f} créditos.")
            else:
                dinero -= 2  # Restamos los 2 créditos aunque falle el regateo
                messagebox.showwarning("Fracaso", f"El intento de regateo de {recurso} falló. Has perdido 2 créditos.")
        else:
            messagebox.showwarning("Fondos Insuficientes", "No tienes suficiente dinero para regatear.")
    else:
        messagebox.showwarning("Acción no permitida", "Solo los comerciantes pueden regatear precios.")

# Comprar un recurso
def comprar_gui():
    global dinero, evento_activado  # Declarar global primero
    recurso = recurso_combobox.get().lower()
    cantidad = int(cantidad_entry.get())
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
            mostrar_estado_gui()
            ventana_principal.update_idletasks()  # Forzar la actualización de la interfaz
            evento_activado = True  # Permitir generar un evento después de la compra
            messagebox.showinfo("Compra Exitosa", f"Has comprado {cantidad} unidades de {recurso} por {costo:.2f} créditos.")
            verificar_game_over()  # Verificar si se llega a 0 créditos
        else:
            messagebox.showwarning("Compra Fallida", "No tienes suficiente dinero o no hay suficiente stock.")
    else:
        messagebox.showwarning("Recurso no válido", "Recurso no válido.")

# Vender un recurso
def vender_gui():
    global dinero, evento_activado  # Declarar global primero
    recurso = recurso_combobox.get().lower()
    cantidad = int(cantidad_entry.get())
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
            mostrar_estado_gui()
            ventana_principal.update_idletasks()  # Forzar la actualización de la interfaz
            evento_activado = True  # Permitir generar un evento después de la venta
            messagebox.showinfo("Venta Exitosa", f"Has vendido {cantidad} unidades de {recurso} por {ganancia} créditos.")
            verificar_game_over()  # Verificar si se llega a 0 créditos
        else:
            messagebox.showwarning("Venta Fallida", "No tienes suficiente cantidad para vender.")
    else:
        messagebox.showwarning("Recurso no válido", "Recurso no válido.")

# Verificar si el jugador ha perdido
def verificar_game_over():
    if dinero <= 0:
        messagebox.showerror("Game Over", "¡Has quedado sin dinero! El juego ha terminado.")
        ventana_principal.quit()

# Graficar precios
def graficar_precios_gui():
    for recurso in recursos:
        historico_precios[recurso].append(recursos[recurso]["precio"])

    fig, ax = plt.subplots(figsize=(10, 5))
    for recurso, precios in historico_precios.items():
        ax.plot(precios, label=recurso)
    ax.legend()
    ax.set_title("Fluctuaciones de precios en el mercado")
    ax.set_xlabel("Turnos")
    ax.set_ylabel("Precio")
    canvas = FigureCanvasTkAgg(fig, master=ventana_principal)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Función para cambiar el rol seleccionado
def cambiar_rol():
    global rol, ventana_principal, evento_activado  # Declarar global primero
    rol = rol_combobox.get()  # Obtener el rol seleccionado
    ventana_rol.withdraw()  # Ocultar la ventana de selección de rol
    evento_activado = False  # Iniciar con el evento desactivado

    # Ahora podemos crear la ventana principal después de seleccionar el rol
    ventana_principal = tk.Tk()
    ventana_principal.title("Simulación de Mercado")

    # Etiquetas de estado
    global estado_label
    estado_label = tk.Label(ventana_principal, text="")
    estado_label.pack()

    # Recurso y cantidad para la compra o venta
    global recurso_combobox, cantidad_entry
    recurso_combobox = ttk.Combobox(ventana_principal, values=list(recursos.keys()))
    recurso_combobox.set("energía")  # Valor predeterminado
    recurso_combobox.pack()

    cantidad_entry = tk.Entry(ventana_principal)
    cantidad_entry.pack()

    # Botones de compra y venta
    comprar_button = tk.Button(ventana_principal, text="Comprar", command=comprar_gui)
    comprar_button.pack()

    vender_button = tk.Button(ventana_principal, text="Vender", command=vender_gui)
    vender_button.pack()

    # Graficar precios
    graficar_button = tk.Button(ventana_principal, text="Ver Precios", command=graficar_precios_gui)
    graficar_button.pack()

    # Botón para evento aleatorio (solo después de compra o venta)
    evento_button = tk.Button(ventana_principal, text="Generar Evento Aleatorio", command=evento_mercado_avanzado)
    evento_button.pack()

    # Botón para hackeo (solo para hacker)
    if rol == "hacker":
        hackear_button = tk.Button(ventana_principal, text="Hackear Precio", command=lambda: hackear_precio(recurso_combobox.get().lower()))
        hackear_button.pack()

    # Botón para regateo (solo para comerciante)
    if rol == "comerciante":
        comerciar_button = tk.Button(ventana_principal, text="Regatear Precio", command=lambda: regatear_precio(recurso_combobox.get().lower()))
        comerciar_button.pack()

    # Iniciar la interfaz
    mostrar_estado_gui()
    ventana_principal.mainloop()

# Crear ventana de selección de rol
ventana_rol = tk.Tk()
ventana_rol.title("Seleccionar Rol")

rol_label = tk.Label(ventana_rol, text="Selecciona tu rol:")
rol_label.pack()

rol_combobox = ttk.Combobox(ventana_rol, values=["comerciante", "hacker", "ciudadano"])
rol_combobox.set("ciudadano")  # Valor predeterminado
rol_combobox.pack()

cambiar_rol_button = tk.Button(ventana_rol, text="Seleccionar Rol", command=cambiar_rol)
cambiar_rol_button.pack()

ventana_rol.mainloop()
