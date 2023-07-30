import smtplib
import tldextract
import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from config import SERVIDOR, PUERTO_SMTP, USUARIO


def enviar_correo(asunto, cuerpo_mensaje, destinatario):
    dominio = tldextract.extract(SERVIDOR).registered_domain
    mensaje_respuesta = MIMEMultipart()
    mensaje_respuesta['Subject'] = asunto
    mensaje_respuesta['From'] = f'{USUARIO}@{dominio}'
    mensaje_respuesta['To'] = destinatario

    # Adjuntar el cuerpo del mensaje como texto HTML
    mensaje_respuesta.attach(MIMEText(cuerpo_mensaje, 'html'))

    with smtplib.SMTP(SERVIDOR, PUERTO_SMTP) as smtp:
        smtp.send_message(mensaje_respuesta)


def enviar_correo_adjunto(asunto, cuerpo_mensaje, destinatario, archivo_adjunto):
    dominio = tldextract.extract(SERVIDOR).registered_domain
    mensaje_respuesta = MIMEMultipart()
    mensaje_respuesta['Subject'] = asunto
    mensaje_respuesta['From'] = f'{USUARIO}@{dominio}'
    mensaje_respuesta['To'] = destinatario

    # Adjuntar el cuerpo del mensaje como texto HTML
    mensaje_respuesta.attach(MIMEText(cuerpo_mensaje, 'html'))

    # Adjuntar la imagen al mensaje
    if os.path.exists(archivo_adjunto):
        with open(archivo_adjunto, 'rb') as archivo_imagen:
            imagen_adjunta = MIMEImage(archivo_imagen.read())
            nombre_adjunto = os.path.basename(archivo_adjunto)
            imagen_adjunta.add_header('Content-Disposition', 'attachment', filename=nombre_adjunto)
            mensaje_respuesta.attach(imagen_adjunta)

    with smtplib.SMTP(SERVIDOR, PUERTO_SMTP) as smtp:
        smtp.send_message(mensaje_respuesta)
