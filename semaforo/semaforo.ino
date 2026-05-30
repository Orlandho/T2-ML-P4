// Pines para los LEDs
const int PIN_VERDE = 8;
const int PIN_ROJO = 9;

// Tiempos por defecto (en milisegundos)
unsigned long tiempoVerde = 3000;
unsigned long tiempoRojo = 3000;

// Variables para el control de tiempo no bloqueante
unsigned long tiempoAnterior = 0;

// Estados: 0 = Verde, 1 = Rojo
int estadoActual = 0;

void setup() {
  pinMode(PIN_VERDE, OUTPUT);
  pinMode(PIN_ROJO, OUTPUT);

  // Iniciar comunicación serie
  Serial.begin(9600);

  // Estado inicial
  digitalWrite(PIN_VERDE, HIGH);
  digitalWrite(PIN_ROJO, LOW);
}

void loop() {
  // 1. Leer datos del puerto serie si están disponibles
  // Formato esperado: "G,R\n" (ej. "3,5\n")
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    data.trim(); // Eliminar espacios, \r u otros caracteres ocultos

    int separatorIndex = data.indexOf(',');

    if (separatorIndex != -1) {
      String greenStr = data.substring(0, separatorIndex);
      String redStr = data.substring(separatorIndex + 1);

      greenStr.trim();
      redStr.trim();

      long greenSec = greenStr.toInt();
      long redSec = redStr.toInt();

      if (greenSec > 0 && redSec > 0) {
        tiempoVerde = greenSec * 1000UL;
        tiempoRojo = redSec * 1000UL;
      }
    }
  }

  // 2. Controlar los LEDs usando millis() (no bloqueante)
  unsigned long tiempoActual = millis();

  if (estadoActual == 0) { // Estado Verde
    if (tiempoActual - tiempoAnterior >= tiempoVerde) {
      // Cambiar a Rojo
      tiempoAnterior = tiempoActual;
      estadoActual = 1;
      digitalWrite(PIN_VERDE, LOW);
      digitalWrite(PIN_ROJO, HIGH);
    }
  } else { // Estado Rojo
    if (tiempoActual - tiempoAnterior >= tiempoRojo) {
      // Cambiar a Verde
      tiempoAnterior = tiempoActual;
      estadoActual = 0;
      digitalWrite(PIN_ROJO, LOW);
      digitalWrite(PIN_VERDE, HIGH);
    }
  }
}
