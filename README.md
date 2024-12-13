# Simulador de Economía Futurista

## Descripción
Este proyecto es un simulador de economía futurista escrito en Python. Permite a los jugadores asumir roles en un mercado dinámico donde pueden comprar, vender, hackear precios, enfrentar eventos aleatorios y visualizar la evolución de los precios en gráficos.

El objetivo es gestionar tus recursos y dinero de manera eficiente para adaptarte a los cambios del mercado y los eventos inesperados.

---

## Características
- **Roles Jugables:**
  - Comerciante: Compra recursos con descuento.
  - Hacker: Manipula precios con riesgo de penalización.
  - Ciudadano: Neutral, sin ventajas ni desventajas.
- **Eventos Aleatorios:** Cambios significativos en los precios debido a eventos como crisis económicas, sequías, descubrimientos tecnológicos, etc.
- **Gestión de Inventario:** Compra y vende recursos según las oportunidades del mercado.
- **Hackeo de Precios:** Disponible para jugadores con el rol de hacker.
- **Gráficos de Precios:** Visualiza la evolución de los precios de los recursos con gráficos interactivos.
- **Guardado y Carga:** Guarda tu progreso en un archivo JSON y reanúdalo cuando quieras.

---

## Requisitos

### Instalación de Dependencias
Este programa requiere Python 3.7 o superior y las siguientes librerías:
- `matplotlib`

Para instalar las dependencias, ejecuta el siguiente comando:
```bash
pip install matplotlib
```

---

## Instrucciones de Uso
1. Clona este repositorio o descarga los archivos del proyecto.
2. Asegúrate de tener Python instalado en tu sistema.
3. Ejecuta el programa:
   ```bash
   python economy_sim.py
   ```
4. Selecciona tu rol al inicio del juego.
5. Usa las opciones disponibles para interactuar con el mercado:
   - Comprar recursos.
   - Vender recursos.
   - Hackear precios.
   - Disparar eventos de mercado.
   - Graficar los precios.
   - Guardar tu progreso.
6. Cuando quieras salir, simplemente escribe `salir`.

---

## Estructura del Proyecto
- **`economy_sim.py`:** Archivo principal del programa.
- **`estado_juego.json`:** Archivo generado automáticamente al guardar el progreso.
- **`README.md`:** Instrucciones y detalles del proyecto.

---

## Ejemplo de Juego
```
=== Estado del Mercado ===
Energía: 10 créditos (Stock: 100)
Comida: 5 créditos (Stock: 200)
Agua: 8 créditos (Stock: 150)
Tecnología: 20 créditos (Stock: 50)
Dinero disponible: 100 créditos
Inventario: {'energía': 0, 'comida': 0, 'agua': 0, 'tecnología': 0}

¿Qué quieres hacer? (comprar/vender/evento/hackear/graficar/guardar/salir):
```

---

## Notas
- El archivo `estado_juego.json` se genera automáticamente si no existe al guardar el progreso.
- Asegúrate de que tienes permisos de escritura en el directorio donde ejecutas el programa.

---

## Contribuciones
Las contribuciones son bienvenidas. Si deseas agregar nuevas características o corregir errores, realiza un *fork* del repositorio y envía un *pull request*.

---

## Licencia
Este proyecto está bajo la Licencia MIT. Puedes ver los detalles en el archivo `LICENSE`.
