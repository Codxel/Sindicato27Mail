import poplib
import email
import time
import re
import tablas, consulta, correo
from config import SERVIDOR, PUERTO_POP, USUARIO, CONTRASEÑA

print("Iniciando Sindicato27Mail...")

# Conectar al servidor de correo utilizando POP3
correo_pop3 = poplib.POP3(SERVIDOR, PUERTO_POP)
correo_pop3.user(USUARIO)
correo_pop3.pass_(CONTRASEÑA)

# Obtener la lista de mensajes
num_mensajes = len(correo_pop3.list()[1])

print("CONEXIÓN EXITOSA, ESPERANDO CORREOS.")

# Procesar los mensajes nuevos
while True:
    # Esperar un período de tiempo antes de verificar si hay mensajes nuevos
    # time.sleep(2)

    # Establecer una nueva conexión con el servidor de correo
    correo_pop3 = poplib.POP3(SERVIDOR, PUERTO_POP)
    correo_pop3.user(USUARIO)
    correo_pop3.pass_(CONTRASEÑA)
    
    # Obtener la lista de mensajes nuevamente y comprobar si hay mensajes nuevos
    nuevo_num_mensajes = len(correo_pop3.list()[1]) - num_mensajes
    if nuevo_num_mensajes == 0:
        correo_pop3.quit()
        continue
    
    # Procesar los mensajes nuevos
    for i in range(num_mensajes + 1, num_mensajes + nuevo_num_mensajes + 1):
        respuesta = correo_pop3.retr(i)
        mensaje = email.message_from_bytes(b'\r\n'.join(respuesta[1]))

        # Consultar si el remitente está registrado en la tabla "users"
        id_personal = consulta.ejecutar_consulta("SELECT id_personal FROM users WHERE email = %s", [re.search(r'<(.*?)>', mensaje['From']).group(1)])
        if id_personal:
            id_tipopersonal = consulta.ejecutar_consulta("SELECT id_tipopersonal FROM personal WHERE id = %s", [id_personal[0][0]])
            asunto = mensaje['Subject']
            asunto = asunto.replace('\r', '').replace('\n', '')
            # Procesar el mensaje utilizando la función procesar_comando
            print("NUEVO MENSAJE: " + asunto)
            tablas.procesar_comando(asunto, mensaje['From'], id_tipopersonal[0][0]-1)
            
        else:
            correo.enviar_correo('REMITENTE NO REGISTRADO', 'El remitente no está registrado en la base de datos, comuniquese con el administrador.', mensaje['From'])
        
        print("MENSAJE PROCESADO")

    # Actualizar el número de mensajes
    num_mensajes += nuevo_num_mensajes

    # Cerrar la conexión con el servidor de correo
    correo_pop3.quit()