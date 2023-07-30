import re
import correo
import insertar, actualizar, eliminar, listar, estadisticas

db_tablas =[['SINDICATOS', 'PERSONAL', 'VEHICULOS', 'MANTENIMIENTOS', 'RUTAS', 'PROMOCIONES', 'TIPOPERSONAL', 'USERS'],
            ['SINDICATOS', 'PERSONAL', 'VEHICULOS', 'MANTENIMIENTOS', 'RUTAS', 'PROMOCIONES'],
            ['SINDICATOS', 'PERSONAL', 'VEHICULOS', 'MANTENIMIENTOS', 'RUTAS', 'PROMOCIONES'],
            ['SINDICATOS', 'PERSONAL', 'VEHICULOS', 'RUTAS', 'PROMOCIONES']]
db_permisos = [
    {
        'LISTAR': listar,
        'INSERTAR': insertar,
        'ACTUALIZAR': actualizar,
        'ELIMINAR': eliminar,
        'ESTADISTICAS': estadisticas
    },
    {
        'LISTAR': listar,
        'INSERTAR': insertar,
        'ACTUALIZAR': actualizar,
        'ESTADISTICAS': estadisticas    
    },
    {
        'LISTAR': listar,
        'ESTADISTICAS': estadisticas   
    },
    {
        'LISTAR': listar,
    }
]

def procesar_comando(asunto, remitente, id_tipopersonal):
    # Comando HELP: enviar un correo con una guía de comandos
    if asunto.upper() == 'HELP':
        mensaje = """
                <html>
                <body>
                <h2>Los comandos disponibles son:</h2>
                <h3>Tablas disponibles:</h3>
                <pre>{db_tablas}</pre>
                <h3>Comandos:</h3>
                <pre>{comandos}</pre>
                <h3>Ejemplos de asunto:</h3>
                <p>TABLA_LISTAR[*] para mostrar todos los registrados, o [Columna=Patrón de Busqueda] para buscar en una columna de la tabla</p>
                <p>TABLA_INSERTAR[Dato1, Dato2, ...] donde se debe colocar todos los datos</p>
                <p>TABLA_ACTUALIZAR[ID, columna=dato1, columna=dato2, ...] donde se debe colocar el ID del registro a modificar y las columnas a modificar con su nuevo valor</p>
                <p>TABLA_ELIMINAR[ID] Se eliminará el registro con el ID indicado</p>
                <p>TABLA_ESTADISTICAS[Nombre de la columna] para mostrar la estadística de la columna indicada</p>
                </body>
                </html>
                """.format(comandos="\n".join(db_permisos[id_tipopersonal].keys()), db_tablas="\n".join(db_tablas[id_tipopersonal]))
        correo.enviar_correo('GUÍA DE COMANDOS - SINDICATO 27 DE DICIEMBRE', mensaje, remitente)
        return

     # Otros comandos: procesar el comando según el formato especificado
    regex = r'^(.*?)_(.*?)\[(.*?)\]'
    comando = re.search(regex, asunto)
    if comando:
        tabla = comando.group(1)
        accion = comando.group(2)
        if tabla in db_tablas[0] and accion in db_permisos[0]:
            # Verificar si el tipo de personal tiene acceso a la tabla y acción
            if tabla in db_tablas[id_tipopersonal] and accion in db_permisos[id_tipopersonal]:
                # Ejecutar la acción correspondiente
                datos = comando.group(3)
                db_permisos[id_tipopersonal][accion].procesar_correo(tabla, datos, remitente)
            else:
                correo.enviar_correo('ACCESO DENEGADO', f"El tipo de personal no tiene acceso a la acción {accion} en la tabla {tabla}", remitente)
        else:
            correo.enviar_correo('COMANDO INVÁLIDO', 'La tabla o la accion especificada en el comando no es válida', remitente)
    else:
        correo.enviar_correo('COMANDO INVÁLIDO', 'El comando enviado en el ASUNTO no es válido', remitente)
