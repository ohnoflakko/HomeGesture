int ledPin = D4; // Pin donde está conectado el LED en la ESP8266

void setup() {
  Serial.begin(9600); // Iniciar la comunicación serial a 9600 baudios
  pinMode(ledPin, OUTPUT); // Configurar el pin del LED como salida
}

void loop() {
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n'); // Leer el comando desde Python
    comando.trim(); // Eliminar espacios en blanco al inicio y al final del comando

    if (comando.equals("encender_led")) {
      digitalWrite(ledPin, HIGH); // Encender el LED
      Serial.println("LED encendido");
    } else if (comando.equals("apagar_led")) {
      digitalWrite(ledPin, LOW); // Apagar el LED
      Serial.println("LED apagado");
    }
  }
}
