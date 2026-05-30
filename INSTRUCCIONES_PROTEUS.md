# Instrucciones para la Simulación del Semáforo en Proteus

Para simular la comunicación entre la interfaz de Python y el Arduino en Proteus, sigue estos pasos cuidadosamente.

## 1. Configurar los Puertos Seriales Virtuales con VSPE

Ya que estás utilizando **Virtual Serial Ports Emulator (VSPE)**, necesitamos crear un "cable" que una dos puertos COM virtuales.

1. Abre VSPE.
2. Haz clic en **Device** -> **Create...** (o el icono con la estrella roja).
3. En **Device type**, selecciona **Pair**. Haz clic en *Siguiente*.
4. En la configuración, elige **COM1** para el *Virtual port 1* y **COM2** para el *Virtual port 2*.
5. Haz clic en **Finish**.
6. Asegúrate de que el botón de **Play** verde esté activado para que la emulación esté corriendo.

*Nota: A partir de este momento, todo lo que envíes por el COM1 aparecerá en el COM2 y viceversa.*

## 2. Preparar el circuito en Proteus

1. Abre Proteus y crea un nuevo diseño.
2. Agrega los siguientes componentes:
   - **Simulino UNO** (o cualquier Arduino UNO disponible en tus librerías).
   - **COMPIM** (Este componente simula el puerto serie del PC).
   - **LED-GREEN** (LED Verde).
   - **LED-RED** (LED Rojo).
   - **RES** (2 Resistencias de 220 o 330 ohmios).
   - Terminal de **Ground** (Tierra).

### Conexiones de los LEDs:
- Conecta el Pin **8** del Arduino a la resistencia, y de ahí al ánodo del LED Verde. El cátodo a Ground.
- Conecta el Pin **9** del Arduino a la resistencia, y de ahí al ánodo del LED Rojo. El cátodo a Ground.

### Conexiones del COMPIM:
- Conecta el pin **TXD** del COMPIM al pin **RX (Pin 0)** del Arduino.
- Conecta el pin **RXD** del COMPIM al pin **TX (Pin 1)** del Arduino.

## 3. Configurar el COMPIM en Proteus

Haz doble clic en el componente **COMPIM** en tu diseño y configúralo de la siguiente manera:
- **Physical Port**: `COM2` (Asumiendo que conectaremos Python al COM1).
- **Physical Baud Rate**: `9600`.
- **Virtual Baud Rate**: `9600`.
- Los demás parámetros déjalos por defecto (Data bits: 8, Parity: None, Stop bits: 1).
- Haz clic en *OK*.

## 4. Compilar el código de Arduino

1. Abre el archivo `semaforo.ino` en tu **Arduino IDE**.
2. Ve a **Programa** -> **Exportar binarios compilados** (o presiona `Ctrl+Alt+S`).
3. Esto generará un archivo `.hex` en la misma carpeta donde guardaste tu `.ino`.
4. Vuelve a Proteus, haz doble clic en el **Arduino (Simulino)**.
5. En la propiedad **Program File**, busca y selecciona el archivo `.hex` que acabas de compilar.
6. Haz clic en *OK*.

## 5. Instalar la librería para Python

Antes de correr el código de Python, asegúrate de tener instalada la librería `pyserial`. Abre tu terminal o CMD e ingresa:

```bash
pip install pyserial
```

## 6. ¡Iniciar la Simulación!

1. En **Proteus**, haz clic en el botón de **Play** (abajo a la izquierda) para iniciar la simulación. El LED Verde debería encenderse.
2. Ejecuta el script de Python: `python semaforo_ui.py`.
3. En la ventana de Python, en **Puerto COM**, asegúrate de que esté seleccionado `COM1` (puedes escribirlo manualmente si la lista desplegable no lo muestra, o seleccionar el que creaste en VSPE).
4. Ingresa el tiempo en segundos para Verde (ej. 5) y para Rojo (ej. 2).
5. Haz clic en **Enviar Tiempos**.
6. Observa en Proteus cómo los LEDs cambian sus tiempos de parpadeo según lo que acabas de enviar.
