# Instrucciones para la Simulación del Semáforo en Proteus

Para simular la comunicación entre la interfaz de Python y el Arduino en Proteus, sigue estos pasos cuidadosamente.

## 1. Configurar los Puertos Seriales Virtuales con Free Virtual Serial Ports

Ya que estás utilizando **Free Virtual Serial Ports** de HHD Software, necesitamos crear un puente ("Local Bridge") que una dos puertos COM virtuales.

1. Abre **Free Virtual Serial Ports**.
2. En el panel principal, selecciona la opción para crear un nuevo **Local Bridge** (Puente Local).
3. Aparecerá una ventana para configurar el puente.
4. En el primer puerto (Port 1), selecciona o escribe **COM3**.
5. En el segundo puerto (Port 2), selecciona o escribe **COM4**.
6. Haz clic en el botón para crear o iniciar el puente.
7. Asegúrate de que el estado indique que el puente está activo y funcionando.

*Nota: A partir de este momento, todo lo que envíes por el COM3 aparecerá en el COM4 y viceversa.*

## 2. Preparar el circuito en Proteus

1. Abre Proteus y crea un nuevo diseño.
2. Agrega los siguientes componentes:
   - **Simulino UNO** (o cualquier Arduino UNO disponible en tus librerías).
   - **COMPIM** (Este componente simula el puerto serie del PC, permitiendo conectar el puerto virtual con el Arduino).
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

Haz doble clic en el componente **COMPIM** en tu diseño y configúralo de la siguiente manera, para asegurar la comunicación correcta con el puerto virtual:
- **Physical Port**: `COM4` (Asumiendo que conectaremos Python al COM3).
- **Physical Baud Rate**: `9600`.
- **Virtual Baud Rate**: `9600`.
- Los demás parámetros déjalos por defecto:
  - **Data bits**: `8`
  - **Parity**: `None`
  - **Stop bits**: `1`
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
3. En la ventana de Python, en **Puerto COM**, asegúrate de que esté seleccionado `COM3` (puedes escribirlo manualmente si la lista desplegable no lo muestra, o seleccionar el que creaste en Free Virtual Serial Ports).
4. Ingresa el tiempo en segundos para Verde (ej. 5) y para Rojo (ej. 2).
5. Haz clic en **Enviar Tiempos**.
6. Observa en Proteus cómo los LEDs cambian sus tiempos de parpadeo según lo que acabas de enviar.
