import correo
import consulta

def procesar_correo(tabla, valores, remitente):
    # Obtener los nombres de las columnas de la tabla especificada
    consulta_columnas = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{tabla.lower()}'"
    nombres_columnas = consulta.ejecutar_consulta(consulta_columnas, [])
    columnas_modificables = [columna[0] for columna in nombres_columnas if columna[0] not in ['id', 'created_at', 'updated_at']]

    # Verificar si el número de datos en valores coincide con el número de columnas modificables en la tabla
    lista_valores = valores.split(',')
    if len(lista_valores) != len(columnas_modificables):
        error = f"El número de datos no coincide con el número de columnas modificables de la tabla {tabla} ({', '.join(columnas_modificables)})\nTome en cuenta que si lleva espacios debe colocar el dato entre comillas, ejemplo: 'dato con espacio'"
        correo.enviar_correo(tabla + "_INSERTAR - Error al insertar registros: '" + valores + "'", error, remitente)
    else:
        try:
            # Construir la consulta SQL de inserción con RETURNING todas las columnas
            consulta_insercion = f"INSERT INTO {tabla} ({', '.join(columnas_modificables)}, created_at, updated_at) VALUES ({', '.join(['%s' for _ in lista_valores])}, NOW(), NOW()) RETURNING *"

            # Ejecutar la consulta de inserción y obtener los datos insertados
            datos_insertados = consulta.ejecutar_consulta(consulta_insercion, lista_valores)

            # Crear una tabla HTML con los datos insertados
            tabla_resultado = '<p>Datos Insertados</p><table border="1"><tr>' + ''.join(f'<th>{col[0]}</th>' for col in nombres_columnas) + '</tr>'
            for fila in datos_insertados:
                tabla_resultado += '<tr>' + ''.join(f'<td>{col}</td>' for col in fila) + '</tr>'
            tabla_resultado += '</table>'

            # Enviar el correo con la tabla HTML
            correo.enviar_correo(tabla + "_INSERTAR - Datos insertados exitosamente", tabla_resultado, remitente)
        except Exception as e:
            # Manejar cualquier excepción que ocurra durante la ejecución de la consulta
            error = f"Error al ejecutar la consulta de inserción: {str(e)}"
            correo.enviar_correo(tabla + "_INSERTAR - Error al insertar registros: '" + valores + "'", error, remitente)
