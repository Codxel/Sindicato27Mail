import correo
import consulta
import matplotlib.pyplot as plt

def generar_grafica(datos, nombres):
    # Crear la gráfica utilizando la biblioteca Matplotlib
    etiquetas = [f'{nombres[i].replace("  ", "")}: {datos[i]}' for i in range(len(datos))]  # Construir las etiquetas de la gráfica con los nombres y los datos
    plt.pie(datos, labels=etiquetas, autopct='%1.1f%%')  # Utilizar las etiquetas en la gráfica
    plt.title('Gráfica')
    imagen_grafica = 'grafica.png'
    plt.savefig(imagen_grafica)
    plt.close()
    return imagen_grafica

def procesar_correo(tabla, columna, remitente):    
    # Verificar si la columna existe en la base de datos
    resultado = consulta.ejecutar_consulta(f"SELECT column_name FROM information_schema.columns WHERE table_name = %s", [tabla.lower()])# Ejecutar la consulta y obtener los resultados

    # Extraer los nombres de las columnas del resultado de la consulta
    columnas = [fila[0] for fila in resultado]
    
    if columna not in columnas:
        # La columna no existe en la base de datos
        correo.enviar_correo('ERROR - Columna no encontrada', f"La columna '{columna}' no existe en la tabla '{tabla}'", remitente)
        return  # Salir de la función
    
    consulta_estadisticas = f"SELECT {columna}, COUNT(*) FROM {tabla} GROUP BY {columna}"
    datos_estadisticas = consulta.ejecutar_consulta(consulta_estadisticas, [])  # Ejecutar la consulta y obtener los resultados

    # Obtener una lista de los nombres de los datos y una lista de los valores de los datos
    nombres = [valor for valor, _ in datos_estadisticas]
    datos = [cantidad for _, cantidad in datos_estadisticas]

    # Calcular el total de registros
    total_registros = sum(cantidad for _, cantidad in datos_estadisticas)

    # Construir el contenido del correo
    contenido_correo = f'<h2>Estadísticas de la columna {columna}</h2>'
    for valor, cantidad in datos_estadisticas:
        # Calcular el porcentaje de cada valor y agregarlo al contenido del correo
        porcentaje = (cantidad / total_registros) * 100
        contenido_correo += f'<p><b>{valor}</b>: {porcentaje:.1f}%</p>'

    # Generar la gráfica con los datos y los nombres
    imagen_grafica = generar_grafica(datos, nombres)

    # Enviar el correo adjuntando la gráfica
    correo.enviar_correo_adjunto(f"{tabla}_ESTADISTICAS - Resultado de las estadísticas", contenido_correo, remitente, imagen_grafica)
