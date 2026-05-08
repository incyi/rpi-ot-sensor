"""
Main.py for Raspberry Pi OT Sensor app.
"""

import time
import RPi.GPIO as GPIO
from pymodbus.client import ModbusTcpClient

# --- GPIO SETUP ---
SENSOR_PIN = 17  # BCM numbering

GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

# --- MODBUS SETUP ---
MODBUS_SERVER_IP = "192.168.1.100"
MODBUS_PORT = 502
REGISTER_ADDRESS = 0  # Holding register

client = ModbusTcpClient(MODBUS_SERVER_IP, port=MODBUS_PORT)

def read_sensor():
    return GPIO.input(SENSOR_PIN)

def main():
    """ Main function. """    
    if not client.connect():
        print("Failed to connect to Modbus server")
        return

    try:
        while True:
            sensor_value = read_sensor()

            # Convert to int (0 or 1)
            value = int(sensor_value)

            print(f"Sensor value: {value}")

            # Write to holding register
            client.write_register(REGISTER_ADDRESS, value)

            time.sleep(1)

    except KeyboardInterrupt:
        print("Stopping...")

    finally:
        client.close()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
