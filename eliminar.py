import re
import correo
import consulta

def procesar_correo(tabla, eliminar_id, remitente):
    # Verificar si el ID contiene solo números
    if not re.fullmatch(r'^\d+$', eliminar_id):
        correo.enviar_correo(tabla + "_ELIMINAR - Error al Eliminar: '" + eliminar_id + "'", 'El ID solo debe contener números', remitente)
    else:
        # Construir la consulta SQL de eliminación
        consulta_eliminar = "DELETE FROM " + tabla + " WHERE id = %s"

        try:
            # Ejecutar la consulta de eliminación
            consulta.ejecutar_consulta(consulta_eliminar, [eliminar_id])
            correo.enviar_correo(tabla + "_ELIMINAR - Eliminación exitosa: '" + eliminar_id + "'", "Se eliminó exitosamente el registro con ID: " + eliminar_id, remitente)
        except Exception as e:
            # En caso de error, enviar un correo de error con el mensaje de la excepción
            correo.enviar_correo(tabla + "_ELIMINAR - Error al eliminar: '" + eliminar_id + "'", f'Ocurrió un error al eliminar el registro: {str(e)}', remitente)
