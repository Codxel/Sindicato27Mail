import psycopg2
from config import NOMBRE_DB, USUARIO_DB, CONTRASEÑA_DB, HOST_DB

def ejecutar_consulta(query, params):
    try:
        conn = psycopg2.connect(host=HOST_DB, database=NOMBRE_DB, user=USUARIO_DB, password=CONTRASEÑA_DB)
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()  # Hace commit para aplicar los cambios
        if cur.description is not None:
            rows = cur.fetchall()
            cur.close()
            conn.close()
            return rows  # Devuelve los resultados de la consulta
        cur.close()
        conn.close()
        return
    except Exception as e:
        raise Exception(f'Ocurrió un error al ejecutar la consulta: {str(e)}')
