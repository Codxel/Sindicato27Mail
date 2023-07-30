import correo
import consulta

def procesar_correo(tabla, lista_valores, remitente):
    # Obtener todos los nombres de columna de la tabla
    nombres_columnas = [columna[0] for columna in consulta.ejecutar_consulta("SELECT column_name FROM information_schema.columns WHERE table_name = %s", [tabla.lower()])]

    # Filtrar las columnas no deseadas (created_at, updated_at) si es necesario
    columnas_modificables = [columna for columna in nombres_columnas if columna not in ['created_at', 'updated_at']]

    # Obtener el valor del ID de la lista de valores
    valores = {}
    id_valor = int(lista_valores.split(',')[0].strip())

    # Verificar si el id_valor existe en la base de datos
    consulta_existe = f"SELECT id FROM {tabla} WHERE id = %s"
    id_existe = consulta.ejecutar_consulta(consulta_existe, [id_valor])
    if not id_existe:
        error = f"El ID {id_valor} no existe en la tabla {tabla}"
        correo.enviar_correo(tabla + "_ACTUALIZAR - Error al actualizar registros: '" + lista_valores + "'", error, remitente)
        return
    
    # Verificar si el número de columnas en lista_valores coincide con el número de columnas modificables en la tabla
    columnas_valores = lista_valores.split(',')[1:]
    for columna_valor in columnas_valores:
        columna, valor = columna_valor.split('=')
        columna = columna.replace(' ', '').lower()
        if columna in columnas_modificables:
            valores[columna] = valor

    # Verificar si se encontraron columnas válidas para actualizar
    if not valores:
        error = f"No se encontraron columnas válidas para actualizar en la tabla {tabla}"
        correo.enviar_correo(tabla + "_ACTUALIZAR - Error al actualizar registros: '" + lista_valores + "'", error, remitente)
        return

    # Construir la lista de pares columna-valor para actualizar
    actualizaciones = [f"{columna} = %s" for columna in valores]

    # Construir la consulta SQL de actualización
    consulta_actualizacion = f"UPDATE {tabla} SET {', '.join(actualizaciones)}, updated_at = NOW() WHERE id = %s RETURNING *"

    try:
        # Ejecutar la transacción de actualización
        datos_actualizados=consulta.ejecutar_consulta(consulta_actualizacion, list(valores.values()) + [id_valor])
        
        # Crear una tabla HTML con los datos actualizados
        tabla_resultado = '<p>Datos actualizados</p><table border="1"><tr>' + ''.join(f'<th>{col}</th>' for col in nombres_columnas) + '</tr>'
        for fila in datos_actualizados:
            tabla_resultado += '<tr>' + ''.join(f'<td>{col}</td>' for col in fila) + '</tr>'
        tabla_resultado += '</table>'

        # Enviar correo con los datos actualizados en formato de tabla HTML
        correo.enviar_correo(tabla + "_ACTUALIZAR - Se actualizaron exitosamente los datos: '" + lista_valores + "'", ''.join(tabla_resultado), remitente)
    except Exception as e:
        error = f"Error al actualizar registros: {str(e)}"
        correo.enviar_correo(tabla + "_ACTUALIZAR - Error al actualizar registros: '" + lista_valores + "'", error, remitente)
