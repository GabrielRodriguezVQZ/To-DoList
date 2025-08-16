import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="To-Do List", page_icon="📝")
st.title("To-Do list en python ")

# Separador visual (línea) para organizar mejor la presentación de la app
# Se agrega una línea horizontal entre los diferentes bloques de la interfaz
st.markdown("---")


# Función para obtener las tareas desde la API (FastAPI)
# Intenta hacer una solicitud GET a la API para obtener las tareas
def obtener_tareas():
    try:
        response = requests.get(API_URL + "/")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"❌ No se pudo conectar con la API: {e}")
        return []

# Llamamos a la función para obtener las tareas de la API
tasks = obtener_tareas()

mensaje_exito = None
mensaje_error = None

# Si hay tareas en la lista, las mostramos en la interfaz
if tasks:
    st.subheader("📋 Tareas pendientes")
    for i, task in enumerate(tasks):
        # Creamos tres columnas para mostrar cada parte de la tarea:
        # 1. Una para el checkbox (si está marcada o no)
        # 2. Una para el nombre de la tarea
        # 3. Una para el botón de eliminar
        col1, col2, col3 = st.columns([0.05, 0.75, 0.2])

        with col1:
            done = st.checkbox("", value=task.get("done", False), key=f"done_{i}")
        with col2:
            # Si la tarea está completada, se muestra tachada
            st.markdown(f"{'~~' + task['task'] + '~~' if task.get('done') else task['task']}")
        with col3:
            if st.button("❌ Eliminar", key=f"del_{i}"):
                try:
                    # Hacemos una solicitud DELETE a la API para eliminar la tarea
                    response = requests.delete(f"{API_URL}/{i}")
                    response.raise_for_status()
                    mensaje_exito = "Tarea eliminada 🗑️"
                except Exception as e:
                    mensaje_error = f"No se pudo eliminar la tarea: {e}"

        # Si el estado de la tarea cambia (checkbox marcado o desmarcado), actualizamos la tarea
        if done != task.get("done", False):
            task["done"] = done
            try:
                response = requests.put(f"{API_URL}/{i}", json=task)
                response.raise_for_status()
                mensaje_exito = "Tarea actualizada ✔️"
            except Exception as e:
                mensaje_error = f"No se pudo actualizar la tarea: {e}"

else:
    st.info("📭 No hay tareas por ahora.")

if mensaje_exito:
    st.success(mensaje_exito)
if mensaje_error:
    st.error(mensaje_error)

# Botón para recargar manualmente la página (refresca la app)
if st.button("🔄 Recargar lista", key="recargar_1"):
    st.write("Recarga la página manualmente (F5 o botón del navegador)")

st.markdown("---")

# Subtítulo para la sección de agregar tarea
st.subheader("➕ Agregar tarea")

# Campo de texto para que el usuario ingrese una nueva tarea
nueva_tarea = st.text_input("✍️ Escribe tu tarea")


# Botón para agregar la nueva tarea
if st.button("Agregar tarea", key="agregar"):
    if nueva_tarea.strip(): # Si la tarea no está vacía
        # Creamos un diccionario con la nueva tarea
        tarea = {"task": nueva_tarea.strip(), "done": False}
        try:
            # Hacemos una solicitud POST para agregar la tarea a la API
            response = requests.post(API_URL + "/", json=tarea)
            response.raise_for_status()
            mensaje_exito = "✅ Tarea agregada"
        except Exception as e:
            mensaje_error = f"No se pudo agregar la tarea: {e}"
    else:
        mensaje_error = "⚠️ Escribe algo para agregar."

if mensaje_exito:
    st.success(mensaje_exito)
if mensaje_error:
    st.error(mensaje_error)

st.markdown("---")

st.subheader("🗑️ Eliminar todas las tareas")

# Checkbox para confirmar que el usuario está seguro de eliminar todas las tareas
confirmar = st.checkbox("Estoy seguro que quiero eliminar todas las tareas", key="confirmar_eliminar_todo")

# Si el usuario ha confirmado, mostramos un botón para eliminar todas las tareas
if confirmar:
    if st.button("Eliminar todo", key="eliminar_todo"):
        try:
            # Iteramos sobre las tareas de atrás hacia adelante (para evitar errores de índice)
            for i in reversed(range(len(tasks))):
                # Hacemos una solicitud DELETE para eliminar cada tarea
                response = requests.delete(f"{API_URL}/{i}")
                response.raise_for_status()
            # Si todas las tareas se eliminan con éxito, mostramos un mensaje
            mensaje_exito = "✅ Todas las tareas han sido eliminadas."
        except Exception as e:
            # Si hay un error al eliminar todas las tareas, mostramos un mensaje de error
            mensaje_error = f"No se pudieron eliminar todas las tareas: {e}"

# Mostramos los mensajes de éxito o error
if mensaje_exito:
    st.success(mensaje_exito)
if mensaje_error:
    st.error(mensaje_error)

# Botón para recargar la lista de tareas manualmente
if st.button("🔄 Recargar lista", key="recargar_2"):
    st.write("Recarga la página manualmente (F5 o botón del navegador)")