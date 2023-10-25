import cv2
import tkinter as tk
from PIL import Image, ImageTk
import mediapipe as mp
import serial

# Inicializar la biblioteca de MediaPipe para la detección de manos
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Función para detectar la mano y determinar si está abierta o cerrada
def detectar_mano(frame, arduino):
    results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]  # Tomar la primera mano detectada
        dedos_abiertos = [False] * 5  # Inicializar lista de dedos abiertos (pulgar, índice, medio, anular, meñique)

        # Verificar si los dedos están abiertos
        for dedo, (punto_inicio, punto_fin) in enumerate([(4, 3), (8, 7), (12, 11), (16, 15), (20, 19)]):
            x_inicio, y_inicio = int(hand_landmarks.landmark[punto_inicio].x * frame.shape[1]), int(hand_landmarks.landmark[punto_inicio].y * frame.shape[0])
            x_fin, y_fin = int(hand_landmarks.landmark[punto_fin].x * frame.shape[1]), int(hand_landmarks.landmark[punto_fin].y * frame.shape[0])

            # Calcular la distancia entre los puntos de inicio y fin del dedo
            distancia = ((x_fin - x_inicio) ** 2 + (y_fin - y_inicio) ** 2) ** 0.5

            # Si la distancia es mayor que un umbral, considerar el dedo como abierto
            umbral = 30  # Ajusta este valor según tu preferencia
            if distancia > umbral:
                dedos_abiertos[dedo] = True

        # Enviar comandos a Arduino según el estado de los dedos
        if all(dedos_abiertos):
            enviar_datos_arduino(arduino, "encender_led\n")
        else:
            enviar_datos_arduino(arduino, "apagar_led\n")

    return frame

# Función para enviar datos a Arduino
def enviar_datos_arduino(arduino, datos):
    try:
        arduino.write(datos.encode())  # Enviar datos a Arduino como cadena de texto
    except Exception as e:
        print("Error al enviar datos a Arduino:", e)

# Función para capturar el video de la cámara y actualizar el lienzo
def actualizar_lienzo():
    ret, frame = cap.read()

    if ret:
        frame = cv2.flip(frame, 1)  # Voltear el marco horizontalmente
        frame = detectar_mano(frame, arduino)  # Detectar la mano y enviar comandos a Arduino
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (canvas_width, canvas_height))
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=img)
        panel.img = img
        panel.config(image=img)

    root.after(10, actualizar_lienzo)  # Llama a la función cada 10 milisegundos

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Detección de Mano y Control de LED")
canvas_width, canvas_height = 640, 480
panel = tk.Label(root)  # Usa un Label de Tkinter como contenedor de la imagen
panel.pack(padx=10, pady=10)

# Inicializar la cámara
cap = cv2.VideoCapture(0)

# Establecer conexión con Arduino (ajusta el puerto COM según tu configuración)
try:
    arduino = serial.Serial('COM5', 9600, timeout=1)  # Establecer conexión a 9600 baudios
except Exception as e:
    print("Error al establecer conexión serial:", e)
    arduino = None

# Iniciar la detección de manos y el envío de datos a Arduino
actualizar_lienzo()

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()

# Cerrar la conexión serial al finalizar
if arduino:
    arduino.close()
