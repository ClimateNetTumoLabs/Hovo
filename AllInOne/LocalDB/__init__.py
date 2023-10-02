import psycopg2
import logging
from LocalDB.config import HOST, USERNAME, PASSWORD, DB_NAME
from logger_config import *


class LocalDatabase:
    def __init__(self) -> None:
        self.connect_to_db()

    def connect_to_db(self):
        try:
            connection = psycopg2.connect(
                host=HOST,
                user=USERNAME,
                password=PASSWORD,
                database=DB_NAME
            )

            cursor = connection.cursor()

            self.conn, self.cursor = connection, cursor

            logging.info("Successfully connected to db")

        except Exception as e:
            logging.error(f"Error occurred during connection to db: {str(e)}", exc_info=True)
            raise

    def create_table(self, device_id):
        try:
            self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {device_id} (
                    id SERIAL PRIMARY KEY,
                    time TIMESTAMP,
                    light REAL,
                    temperature REAL,
                    pressure REAL,
                    humidity REAL,
                    PM1 REAL,
                    PM2_5 REAL,
                    PM10 REAL,
                    CO2 REAL,
                    speed REAL,
                    rain REAL,
                    direction TEXT
                );
                """)

            self.conn.commit()

            logging.info(f"Successfully created table {device_id}")
        except Exception as e:
            logging.error(f"Error occurred during creating table weather_data: {str(e)}", exc_info=True)
            raise

    def drop_table(self, device):
        try:
            self.cursor.execute(f"DROP TABLE {device}")
            self.conn.commit()
        except Exception as e:
            logging.error(f"Error occurred during creating table weather_data: {str(e)}", exc_info=True)
            raise
    
    def get_data(self, device):
        self.cursor.execute(f"SELECT (time, light, temperature, pressure, humidity, PM1, PM2_5, PM10, CO2, speed, rain, direction) FROM {device};")

        result = self.cursor.fetchall()

        return result

    def insert_data(self, device, data):
        try:
            self.create_table(device)
            
            query_data = ', '.join([f"'{elem}'" if elem is not None else "NULL" for elem in data])
            self.cursor.execute(f"INSERT INTO {device} (time, light, temperature, pressure, humidity, PM1, PM2_5, PM10, CO2, speed, rain, direction) VALUES ({query_data})")
            self.conn.commit()

            logging.info("Successfully inserted data into the database")
        except Exception as e:
            logging.error(f"Error occurred during creating table weather_data: {str(e)}", exc_info=True)
            raise