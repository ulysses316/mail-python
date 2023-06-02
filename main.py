import os
from datetime import date
import smtplib
from email.mime.text import MIMEText
import requests
from jinja2 import Environment, FileSystemLoader

response = requests.get("http://localhost:3000/api/usuarios").json()
usuarios = []
for objeto in response:
    usuarios.append(objeto["Nombre"])

data = {
    "usuarios": usuarios
}

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('template.html')
html_body = template.render(data)

def enviar_correo(destinatario, asunto):
    # Configurar los detalles del correo electrónico
    remitente = os.getenv("SMTP_USER")  # Dirección de correo electrónico del remitente
    clave = os.getenv("SMTP_PASS")  # Contraseña de la cuenta de correo electrónico del remitente

    # Crear el objeto del mensaje MIME
    msg = MIMEText(html_body, 'html')
    msg['Subject'] = asunto
    msg['From'] = remitente
    msg['To'] = destinatario

    try:
        # Establecer conexión con el servidor SMTP de tu proveedor de correo
        servidor_smtp = smtplib.SMTP_SSL(os.getenv("SMTP_HOST"), os.getenv("SMTP_PORT"))  # Ejemplo con Gmail, verifica los detalles del servidor para tu proveedor de correo
        
        servidor_smtp.login(remitente, clave)

        # Enviar el correo electrónico
        servidor_smtp.sendmail(remitente, destinatario, msg.as_string())

        # Cerrar la conexión con el servidor SMTP
        servidor_smtp.quit()
        print('Correo electrónico enviado con éxito')
    except Exception as e:
        print('Error al enviar el correo electrónico:', str(e))


enviar_correo("ulises.gonzalez@pico.love", f"Resumen del dia {date.today().strftime('%d-%m-%Y')} Pico Love.")