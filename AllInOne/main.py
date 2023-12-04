from datetime import datetime
from Sensors import ReadSensors
from Data import DataHandler
from logger_config import *
from Scripts import update_time_from_ntp, chmod_tty


def main():
    sensor_reader = ReadSensors()
    dataHandler = DataHandler()

    while True:
        try:
            data = sensor_reader.collect_data()
            
            logging.info("Data collection completed.")
            logging.info(f"Collected data -> {data}")

            data['time'] = datetime.now().isoformat()

            dataHandler.save(data)
        except Exception as e:
            logging.error(f"Error occurred during execution: {str(e)}", exc_info=True)


if __name__ == "__main__":
    update_time_from_ntp()
    chmod_tty()
    logging.info("Program started")
    main()
