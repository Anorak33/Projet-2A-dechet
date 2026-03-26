import time
from telemetrix import telemetrix


board = telemetrix.Telemetrix()
# Adresse I2C par défaut du TF-Luna
TF_LUNA_ADDR = 0x10 

# 1. Configurer le port I2C
board.set_pin_mode_i2c()


def i2c_callback(data):
    # Le TF-Luna renvoie généralement la distance en cm sur les 2 premiers octets
    # data[0] = nombre d'octets, data[1] = registre, data[2] = Low Byte, data[3] = High Byte
    if len(data) >= 4:
        distance = data[2] + (data[3] << 8)
        print(f"Distance mesurée : {distance} cm")

# 2. Demander une lecture continue (dépend du registre de mesure du TF-Luna)
# Ici on lit 2 octets à partir du registre 0x00
while True:
    try:
        board.i2c_read(TF_LUNA_ADDR, 0x00, 2, i2c_callback)
        time.sleep(0.1)  # Fréquence de 10Hz
    except KeyboardInterrupt:
        board.shutdown()
        break