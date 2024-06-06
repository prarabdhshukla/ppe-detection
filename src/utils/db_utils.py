import psycopg2
import os

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        dbname=os.getenv('DB_NAME')
    )

def save_detection_to_db(camera_id, frame, has_ppe, details):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO detections (camera_id, frame, has_ppe, details) VALUES (%s, %s, %s, %s)",
        (camera_id, psycopg2.Binary(frame), has_ppe, json.dumps(details))
    )
    conn.commit()
    cursor.close()
    conn.close()
