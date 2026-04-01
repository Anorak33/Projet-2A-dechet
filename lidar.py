import time
from telemetrix import telemetrix

# --- CONFIGURATION ---
TX_PIN = 2
RX_PIN = 3
BAUD_RATE = 115200
SEUIL = 2 

board = telemetrix.Telemetrix()
distance_calibree = 0
buffer = []

def callback(data):
    global buffer
    # data[2] est l'octet reçu
    # On utilise un masque pour ne garder que les 8 bits (0-255)
    byte = data[2] & 0xFF
    buffer.append(byte)
    print(buffer)
def process_buffer():
    global buffer, distance_calibree
    
    # On cherche la séquence 0x59, 0x59 (89, 89 en décimal)
    while len(buffer) >= 9:
        if buffer[0] == 0x59 and buffer[1] == 0x59:
            # Extraction de la distance
            low = buffer[2]
            high = buffer[3]
            dist = low + (high << 8)
            
            if 10 < dist < 5000:
                if distance_calibree == 0:
                    distance_calibree = dist
                    print(f"\n--- CALIBRATION OK : {distance_calibree} cm ---")
                
                diff = distance_calibree - dist
                print(f"Dist: {dist}cm | Ref: {distance_calibree}cm | Diff: {diff}cm", end='\r')
                
                if diff >= SEUIL:
                    print(f"\n!!!!! DECHET DETECTE (Diff: {diff}) !!!!!")
            
            # On retire la trame traitée
            buffer = buffer[9:]
        else:
            # On décale d'un octet si on n'est pas sur le header 0x59
            buffer.pop(0)

try:
    print("Initialisation Software Serial...")
    # On active le mode software serial
    board.set_pin_mode_(TX_PIN, RX_PIN, callback)
    
    time.sleep(2)
    print("Lecture en cours... (Ctrl+C pour arrêter)")

    while True:
        # On traite les données accumulées dans le buffer
        if len(buffer) > 0:
            process_buffer()
        
        # Petite pause pour ne pas saturer le CPU, 
        # mais assez courte pour vider le buffer série
        time.sleep(0.01)

except KeyboardInterrupt:
    board.shutdown()
    print("\nArrêt du programme.")