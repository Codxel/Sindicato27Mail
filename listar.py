import re
import correo
import consulta

def procesar_correo(tabla, patron, remitente):
    # Verificar si el patrón es "*", en cuyo caso se seleccionan todos los registros de la tabla
    if patron == '*':
        consulta_listar = f"SELECT * FROM {tabla}"
    else:
        # Verificar si el patrón es válido
        columna, valor = patron.split("=")
        if not re.fullmatch(r'[a-zA-Z0-9 ]+', valor) or len(valor) < 2:
            # Si el patrón contiene caracteres no válidos, se envía un correo de error
            correo.enviar_correo(tabla + "_LISTAR - Error de Búsqueda: '" + patron + "'", 'El patrón de búsqueda es inválido', remitente)
            return

        # Construir la consulta SQL con la columna y el patrón especificados
        consulta_listar = f"SELECT * FROM {tabla} WHERE lower({columna}) ILIKE %s"
        valor = '%' + valor.lower() + '%'

    try:
        # Ejecutar la consulta y obtener los resultados
        resultados = consulta.ejecutar_consulta(consulta_listar, [valor])

        if resultados:
            # Si se encontraron resultados, construir una tabla HTML con los resultados y enviarla por correo
            nombres_columnas = [columna[0] for columna in consulta.ejecutar_consulta(f"SELECT column_name FROM information_schema.columns WHERE table_name = %s", [tabla.lower()])]
            tabla_resultado = '<table border="1"><tr>' + ''.join(f'<th>{col}</th>' for col in nombres_columnas) + '</tr>'
            for fila in resultados:
                tabla_resultado += '<tr>' + ''.join(f'<td>{col}</td>' for col in fila) + '</tr>'
            tabla_resultado += '</table>'
            correo.enviar_correo(tabla + "_LISTAR - Resultado de su búsqueda: '" + patron + "'", tabla_resultado.replace("  ", ""), remitente)
        else:
            # Si no se encontraron resultados, enviar un correo informando que no se encontraron resultados
            correo.enviar_correo(tabla + "_LISTAR - Resultado de su búsqueda: '" + patron + "'", 'No se encontraron resultados para el patrón de búsqueda especificado', remitente)

    except Exception as e:
        # Manejar cualquier excepción que ocurra durante la ejecución de la consulta
        error = f"Error al ejecutar la consulta: {str(e)}"
        correo.enviar_correo(tabla + "_LISTAR - Error al procesar consulta", error, remitente)
