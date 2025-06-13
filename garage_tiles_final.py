
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import random

st.set_page_config(layout="centered")
st.title("Garage Tile Designer Final")

# Unidad de medida
unidad = st.selectbox("Selecciona la unidad de medida", ["metros", "centímetros"], key="unidad")
factor = 1 if unidad == "metros" else 0.01
min_val = 1.0 if unidad == "metros" else 10.0

# Entradas de ancho y largo
ancho_input = st.number_input(f"Ancho del espacio ({unidad})", min_value=min_val, step=1.0,
                              value=4.0 if unidad == "metros" else 400.0, key="ancho")
largo_input = st.number_input(f"Largo del espacio ({unidad})", min_value=min_val, step=1.0,
                              value=6.0 if unidad == "metros" else 600.0, key="largo")

# Conversión y área
ancho_m = ancho_input * factor
largo_m = largo_input * factor
area_m2 = round(ancho_m * largo_m, 2)
st.markdown(f"**Área total:** {area_m2} m²")

# Opciones de bordillos y esquineros
incluir_bordillos = st.checkbox("Agregar bordillos", value=True, key="cb_bordillos")
incluir_esquineros = st.checkbox("Agregar esquineros", value=True, key="cb_esquineros")
pos_bord = st.multiselect("¿Dónde colocar bordillos?",
                          ["Arriba", "Abajo", "Izquierda", "Derecha"],
                          default=["Arriba", "Abajo", "Izquierda", "Derecha"], key="pos_bord")

# Colores disponibles
colores_palmetas = {
    "Negro": "#000000", "Gris": "#B0B0B0", "Gris Oscuro": "#4F4F4F",
    "Azul": "#0070C0", "Celeste": "#00B0F0", "Amarillo": "#FFFF00",
    "Verde": "#00B050", "Rojo": "#FF0000"
}
col_names = list(colores_palmetas.keys())

# Dimensiones en palmetas
cols = math.ceil(ancho_m / 0.4)
rows = math.ceil(largo_m / 0.4)

# Inicializar DataFrame en session state con columnas como strings
if 'df_grid' not in st.session_state or st.session_state.get('shape') != (rows, cols):
    columns = [str(i) for i in range(cols)]
    df = pd.DataFrame([["Gris"] * cols for _ in range(rows)], columns=columns)
    st.session_state['df_grid'] = df
    st.session_state['shape'] = (rows, cols)

df = st.session_state['df_grid']

# Botones de diseños aleatorios
st.subheader("Diseños rápidos")
col1, col2, col3, col4 = st.columns(4)
if col1.button("Diseño 1"):
    new = df.copy()
    for y in range(rows):
        for x in range(cols):
            new.iat[y, x] = random.choice(["Negro", "Gris"])
    df = new
if col2.button("Diseño 2"):
    new = df.copy()
    for y in range(rows):
        for x in range(cols):
            if y in [0, rows-1] or x in [0, cols-1]:
                new.iat[y, x] = "Rojo"
            else:
                new.iat[y, x] = "Gris Oscuro"
    df = new
if col3.button("Diseño 3"):
    new = df.copy()
    for y in range(rows):
        for x in range(cols):
            new.iat[y, x] = "Amarillo" if (x+y) % 2 == 0 else "Negro"
    df = new
if col4.button("Diseño 4"):
    new = df.copy()
    cx, cy = cols//2, rows//2
    for y in range(rows):
        for x in range(cols):
            new.iat[y, x] = "Celeste" if abs(x-cx)<=min(3, cols//4) and abs(y-cy)<=min(3, rows//4) else "Azul"
    df = new

# Guarda el df modificado
st.session_state['df_grid'] = df

# Editor de tabla para selección manual
st.subheader("Diseño personalizado")
column_config = {
    col: st.column_config.SelectboxColumn(
        label_visibility="hidden",
        options=col_names
    ) for col in df.columns
}
edited = st.data_editor(
    df,
    column_config=column_config,
    use_container_width=True,
    num_rows="fixed",
    key="editor"
)
st.session_state['df_grid'] = edited

# Renderizado gráfico
fig, ax = plt.subplots(figsize=(cols/2, rows/2))
for y in range(rows):
    for x, col in enumerate(df.columns):
        color_hex = colores_palmetas.get(st.session_state['df_grid'].iat[y, x], "#D9D9D9")
        ax.add_patch(plt.Rectangle((x, rows-1-y), 1, 1, facecolor=color_hex, edgecolor="black"))

# Bordillos delgados
if incluir_bordillos:
    if "Arriba" in pos_bord: ax.add_patch(plt.Rectangle((0, rows), cols, 0.15, facecolor="#000000"))
    if "Abajo" in pos_bord: ax.add_patch(plt.Rectangle((0, -0.15), cols, 0.15, facecolor="#000000"))
    if "Izquierda" in pos_bord: ax.add_patch(plt.Rectangle((-0.15, 0), 0.15, rows, facecolor="#000000"))
    if "Derecha" in pos_bord: ax.add_patch(plt.Rectangle((cols, 0), 0.15, rows, facecolor="#000000"))

# Esquineros
if incluir_esquineros:
    size = 0.15
    for (x, y) in [(0, 0), (0, rows), (cols, 0), (cols, rows)]:
        ax.add_patch(plt.Rectangle((x-size/2, y-size/2), size, size, facecolor="#000000"))

ax.set_xlim(-0.5, cols+0.5)
ax.set_ylim(-0.5, rows+0.5)
ax.set_aspect('equal')
ax.axis('off')
st.pyplot(fig)
